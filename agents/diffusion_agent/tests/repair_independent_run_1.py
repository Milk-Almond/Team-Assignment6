#!/usr/bin/env python3
"""Repair the known formatting defect in independent run 1 without altering raw evidence."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
raw = root / "responses" / "independent_run_1_raw.json"
out = root / "responses" / "independent_run_1_repaired.json"
old = 'should be represented as established before these measurements exist."\n},\n  "risk_governance_implication"'
new = 'should be represented as established before these measurements exist.",\n  "risk_governance_implication"'
source = raw.read_text()
if source.count(old) != 1:
    raise SystemExit("ABORT: expected unique defect not found; original unchanged")
repaired = source.replace(old, new)
data = json.loads(repaired)
required = {"agent", "analytical_question", "general_et_finding", "application_finding", "organization_specific_finding", "evidence", "contrary_evidence_or_limitations", "confidence_and_uncertainty", "value_opportunity_implication", "risk_governance_implication", "recommendation_management_implication", "change_monitoring_triggers", "abstention_or_more_information_needed"}
if not required.issubset(data):
    raise SystemExit("ABORT: repaired JSON lacks required fields")
out.write_text(repaired)
print(f"REPAIR PASSED: wrote {out}; original raw evidence unchanged")
