# Team Lab 6 Emerging Technology Diffusion Agent

This working integration package applies Rogers diffusion reasoning to ChatGPT for human-reviewed internal drafting in a **hypothetical** professional-services firm. Start with [the Agent Record](agents/diffusion_agent/records/agent_record.md), [candidate comparison](agents/diffusion_agent/records/candidate_comparison.md) and [evidence register](agents/diffusion_agent/records/evidence_register.md).

The shared course scaffold in `core/` and its tooling are copied unchanged from the individual frozen scaffold. `FROZEN_CORE_SHA256.txt` checks the included files. All team members approved the integrated SubAgent 4 Diffusion Agent, Agent Record, tests, and Adoption Agent handoff on October 27, 2026. The approved specialist version is `1.0-team-synthesis`. Three fresh ChatGPT conversations using the same primary prompt are preserved in the response folder.

Reproduce the recorded checks from the repository root with `python3 tools/check_frozen_core.py`, `python3 tools/build_prompt.py --agent agents/diffusion_agent --case agents/diffusion_agent/cases/primary.json --out /tmp/diffusion_primary_prompt.txt`, `python3 tools/validate_response.py agents/diffusion_agent/responses/primary.json` (and both contrasts), and `python3 agents/diffusion_agent/tests/check_contrast.py`. The saved JSON analyses are authored reference artifacts. These commands do not query a model or measure real organizational adoption.

## Proposed evidence and testing addition

See [version 1.1-proposed](agents/diffusion_agent/additions/v1_1/README.md) for self-contained evidence-bearing prompts, posture-only cases and one manual format-retry path. This addition has local regression coverage; fresh model runs and team acceptance remain pending. The existing Word report and approval statements above describe v1.0.
