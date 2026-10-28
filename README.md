# Team Lab 6 Emerging Technology Diffusion Agent

This working integration package applies Rogers diffusion reasoning to ChatGPT for human-reviewed internal drafting in a **hypothetical** professional-services firm. Start with [the Agent Record](agents/diffusion_agent/records/agent_record.md), [candidate comparison](agents/diffusion_agent/records/candidate_comparison.md) and [evidence register](agents/diffusion_agent/records/evidence_register.md).

The shared course scaffold in `core/` and its tooling are copied unchanged from the individual frozen scaffold. `FROZEN_CORE_SHA256.txt` checks the included files. The team specialist is version `1.0-team-synthesis`. The present status is prepared for team workshop review; no unobserved vote, attendance or member sign-off is asserted.

Reproduce the recorded checks from the repository root with `python3 tools/check_frozen_core.py`, `python3 tools/build_prompt.py --agent agents/diffusion_agent --case agents/diffusion_agent/cases/primary.json --out /tmp/diffusion_primary_prompt.txt`, `python3 tools/validate_response.py agents/diffusion_agent/responses/primary.json` (and both contrasts), and `python3 agents/diffusion_agent/tests/check_contrast.py`. The saved JSON analyses are authored reference artifacts. These commands do not query a model or measure real organizational adoption.
