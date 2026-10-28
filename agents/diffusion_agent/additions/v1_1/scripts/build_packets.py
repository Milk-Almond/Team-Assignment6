#!/usr/bin/env python3
"""Build fixed-evidence packets with the unchanged frozen course builder."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXTENSION = Path(__file__).resolve().parents[1]
ROOT = EXTENSION.parents[3]
SOURCE = ROOT / 'agents/diffusion_agent/records/evidence_register.md'
CASES = ('primary', 'contrast_conservative', 'contrast_aggressive')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(out):
    register = SOURCE.read_text()
    if not register.strip():
        raise ValueError('Evidence register is empty; refusing an evidence-free packet.')
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        'version': '1.1-proposed',
        'status': 'packets generated; no model invocation or team approval asserted',
        'evidence_register_path': SOURCE.relative_to(ROOT).as_posix(),
        'evidence_register_sha256': sha(SOURCE),
        'source_register_date': '2026-10-27; refresh before a later decision',
        'inputs': {
            'specialist_sha256': sha(EXTENSION / 'specialist_instructions.md'),
            'metadata_sha256': sha(EXTENSION / 'agent_metadata.json'),
            'common_sha256': sha(ROOT / 'core/common_instructions.md'),
            'schema_sha256': sha(ROOT / 'core/output_schema.json'),
            'builder_sha256': sha(ROOT / 'tools/build_prompt.py'),
        },
        'cases': [],
    }
    for name in CASES:
        source_case = EXTENSION / f'cases/{name}.json'
        case = json.loads(source_case.read_text())
        case['additional_context'] += (
            '\n\nUse only this fixed-source register during the comparison. '
            'Its claims were reviewed separately as recorded by the source author; '
            'do not claim you independently reopened the sources. '
            'Differentiate dated reach observations from unknown exact-workflow diffusion. '
            'No extra organizational permissions or resources are supplied.\n\n'
            '# SUPPLIED DATED EVIDENCE REGISTER\n' + register
        )
        enriched = out / f'{name}_case_with_evidence.json'
        enriched.write_text(json.dumps(case, indent=2) + '\n')
        packet = out / f'{name}_prompt.txt'
        subprocess.run([
            sys.executable, str(ROOT / 'tools/build_prompt.py'),
            '--agent', str(EXTENSION), '--case', str(enriched), '--out', str(packet),
        ], check=True, capture_output=True, text=True)
        # Hash-only manifest keeps generated artifacts portable across computers.
        manifest['cases'].append({
            'case': name,
            'source_case_sha256': sha(source_case),
            'enriched_case_file': enriched.name,
            'enriched_case_sha256': sha(enriched),
            'prompt_file': packet.name,
            'prompt_sha256': sha(packet),
        })
    (out / 'packet_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'work/diffusion_v1_1')
    args = parser.parse_args()
    manifest = build(args.out)
    print(f'Built {len(manifest["cases"])} fixed-evidence packets; no model was called.')
