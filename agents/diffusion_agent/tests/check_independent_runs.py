#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = [root / "responses" / f"independent_run_{i}_raw.json" for i in (1, 2, 3)]

raw1 = files[0].read_text()
try:
    json.loads(raw1)
except json.JSONDecodeError:
    pass
else:
    raise AssertionError("Run 1 was expected to preserve its observed JSON syntax failure")

for path in files[1:]:
    data = json.loads(path.read_text())
    joined = " ".join(
        [
            data["general_et_finding"],
            data["application_finding"],
            data["organization_specific_finding"],
            data["recommendation_management_implication"],
        ]
    ).lower()
    for factor in ("relative advantage", "compatibility", "complexity", "trialability", "observability"):
        assert factor in joined, (path.name, factor)
    assert "indeterminate" in joined, path.name
    assert "adoption agent" in joined, path.name
    assert "stage is indeterminate" in joined or "stage assessment: indeterminate" in joined, path.name

# A repaired Run 1 copy, when supplied, must validate without overwriting raw evidence.
repaired = root / "responses" / "independent_run_1_repaired.json"
if repaired.exists():
    fixed = json.loads(repaired.read_text())
    assert fixed["agent"]["version"] == "1.0-team-synthesis"
    assert "indeterminate" in fixed["application_finding"].lower()
    assert "adoption agent" in fixed["recommendation_management_implication"].lower()

print("INDEPENDENT RUN CHECK PASSED: 3 conversations preserved; runs 2-3 valid; run 1 syntax failure retained; shared analytical boundary confirmed")
