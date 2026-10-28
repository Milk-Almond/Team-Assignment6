# Proposed evidence and testing addition

Version 1.1-proposed adds an evidence-bearing evaluation path to the existing 1.0 team synthesis. The original approved agent, saved responses, source register and Word report remain historical artifacts. Team approval of this proposed extension has not been asserted.

## What this fixes

The frozen prompt builder reads common instructions, agent metadata, specialist instructions and case JSON. It does not read the separate evidence register. The new wrapper embeds the full existing register into each case before calling that same unchanged builder. The output includes a hash manifest so reviewers can identify the exact source snapshot and packets.

The three new cases change only adoption_posture. They do not hide an approved sandbox or staffing inside posture. The original contrasts remain available as broader posture/capacity examples. Different evidence priorities can be justified, but the earliest feasible evaluation date may remain identical when controls and capacity are unresolved.

The original reference checker now verifies distinct recommendation text rather than printing that timing differs without checking that field. It explicitly states that different wording is not proof of a materially different decision or independent model behavior.

## Build and check from the repository root

```sh
python3 agents/diffusion_agent/additions/v1_1/scripts/build_packets.py
python3 agents/diffusion_agent/additions/v1_1/tests/test_additions.py
python3 tools/check_frozen_core.py
python3 agents/diffusion_agent/tests/check_contrast.py
python3 agents/diffusion_agent/tests/check_independent_runs.py
```

Generated files are in `work/diffusion_v1_1/`: three self-contained prompts, three evidence-enriched cases and `packet_manifest.json`. Keep the manifest with actual saved model outputs. Generation does not query a model. The source register retains its October 27, 2026 review date; no additional market research or new source verification is claimed by this addition. Refresh the register before a later live decision, then regenerate all comparison packets together.

## Run and evaluate

Use each prompt in a separate fresh conversation under the same recorded model/tool settings. Save the unedited result and record the case name, date, model shown, browsing setting, packet hash and response hash. Do not rename authored reference examples as new runs. Complete the review checklist in `records/evaluation_checklist.md`; retain failures and disagreements.

Validate a saved result using the full frozen schema:

```sh
python3 agents/diffusion_agent/additions/v1_1/scripts/review_response.py work/diffusion_v1_1/primary_raw.json
```

For an invalid initial response, prepare one manual format-repair request using its exact original packet. This does not edit the raw file or invoke a model:

```sh
python3 agents/diffusion_agent/additions/v1_1/scripts/review_response.py work/diffusion_v1_1/primary_raw.json --packet work/diffusion_v1_1/primary_prompt.txt --retry-out work/diffusion_v1_1/primary_format_retry.txt
```

Exit 1 indicates the initial response remains invalid even when a retry request was written. Send the retry request once, save the answer separately, then validate with `--attempt 1`. If it is still invalid, exit 2 requests human review. A format repair is part of the same run, not another independent replication. Passing schema validation does not certify factual or analytical quality.

## Status

Local packet-generation and regression checks have been executed; see `records/verification.md`. No fresh v1.1 model responses, successful model repair, new adoption evidence, organizational pilot or human team approval is claimed. The existing Word report describes v1.0; use the extension's record as an addendum until the team accepts this version and updates its submission.
