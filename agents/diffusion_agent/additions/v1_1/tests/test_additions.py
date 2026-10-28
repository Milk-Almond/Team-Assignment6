#!/usr/bin/env python3
"""Regression checks for evidence delivery, isolated inputs, and format recovery."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

EXTENSION = Path(__file__).resolve().parents[1]
ROOT = EXTENSION.parents[3]
AGENT = ROOT / 'agents/diffusion_agent'


def module(name):
    spec = importlib.util.spec_from_file_location(name, EXTENSION / f'scripts/{name}.py')
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


packets = module('build_packets')
review = module('review_response')


class AdditionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)
        cls.manifest = packets.build(cls.out)
        cls.schema = json.loads((ROOT / 'core/output_schema.json').read_text())
        cls.good = json.loads((AGENT / 'responses/primary.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_frozen_files_unchanged(self):
        for line in (ROOT / 'FROZEN_CORE_SHA256.txt').read_text().splitlines():
            if line.strip():
                expected, rel = line.split('  ', 1)
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), expected, rel)

    def test_full_register_reaches_every_packet(self):
        register = packets.SOURCE.read_text()
        for entry in self.manifest['cases']:
            packet = (self.out / entry['prompt_file']).read_text()
            embedded = packet.split('# CASE CONTEXT\n', 1)[1].split('\n# REQUIRED OUTPUT SCHEMA', 1)[0]
            self.assertIn(register, json.loads(embedded)['additional_context'])
            self.assertIn('1.1-proposed', packet)
            self.assertIn('Do not infer an approved sandbox', packet)

    def test_only_posture_changes_after_evidence_injection(self):
        cases = [json.loads((self.out / e['enriched_case_file']).read_text()) for e in self.manifest['cases']]
        for case in cases[1:]:
            self.assertEqual([key for key in case if case[key] != cases[0][key]], ['adoption_posture'])
        self.assertNotIn('sandbox', cases[2]['adoption_posture'])

    def test_manifest_hashes_match_actual_artifacts(self):
        for entry in self.manifest['cases']:
            for label in ['enriched_case', 'prompt']:
                self.assertEqual(packets.sha(self.out / entry[label + '_file']), entry[label + '_sha256'])

    def test_valid_response_passes_full_contract(self):
        _, error = review.assess(json.dumps(self.good), self.schema)
        self.assertIsNone(error)

    def test_nested_type_and_extra_top_level_are_rejected(self):
        bad = copy.deepcopy(self.good)
        bad['evidence'][0]['claim'] = 42
        self.assertIsNotNone(review.assess(json.dumps(bad), self.schema)[1])
        bad = copy.deepcopy(self.good)
        bad['unsupported_extra_field'] = 'wrong contract'
        self.assertIsNotNone(review.assess(json.dumps(bad), self.schema)[1])

    def test_preserved_failed_run_prepares_retry_without_overwrite(self):
        raw_path = AGENT / 'responses/independent_run_1_raw.json'
        before = raw_path.read_bytes()
        retry = self.out / 'format_retry.txt'
        p = subprocess.run([sys.executable, str(EXTENSION / 'scripts/review_response.py'),
                            str(raw_path), '--packet', str(self.out / 'primary_prompt.txt'),
                            '--retry-out', str(retry)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn(raw_path.read_text(), retry.read_text())
        self.assertIn('NOT AN INDEPENDENT REPLICATION', retry.read_text())
        self.assertEqual(raw_path.read_bytes(), before)

    def test_retry_exhaustion_requests_human_review(self):
        p = subprocess.run([sys.executable, str(EXTENSION / 'scripts/review_response.py'),
                            str(AGENT / 'responses/independent_run_1_raw.json'), '--attempt', '1'],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn('human review', p.stdout)

    def test_retry_cannot_overwrite_raw_response(self):
        raw = AGENT / 'responses/independent_run_1_raw.json'
        before = raw.read_bytes()
        p = subprocess.run([sys.executable, str(EXTENSION / 'scripts/review_response.py'),
                            str(raw), '--packet', str(self.out / 'primary_prompt.txt'),
                            '--retry-out', str(raw)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertEqual(raw.read_bytes(), before)

    def test_identical_timing_fails_legacy_reference_checker(self):
        target = self.out / 'identical_timing'
        target.mkdir()
        for name in packets.CASES:
            d = json.loads((AGENT / f'responses/{name}.json').read_text())
            d['recommendation_management_implication'] = self.good['recommendation_management_implication']
            (target / f'{name}.json').write_text(json.dumps(d))
        p = subprocess.run([sys.executable, str(AGENT / 'tests/check_contrast.py'), str(target)],
                           capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('Timing text is identical', p.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
