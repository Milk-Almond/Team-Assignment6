#!/usr/bin/env python3
from pathlib import Path
import argparse, json

root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description='Build a ChatGPT-ready prompt packet for one specialist and one case.')
p.add_argument('--agent', required=True, help='Agent folder, e.g. agents/diffusion_agent')
p.add_argument('--case', required=True, help='Case JSON file')
p.add_argument('--out', help='Output .txt path; defaults to work/<agent>_<case>_prompt.txt')
a=p.parse_args()
agent=(root/a.agent).resolve() if not Path(a.agent).is_absolute() else Path(a.agent)
case=(root/a.case).resolve() if not Path(a.case).is_absolute() else Path(a.case)
common=(root/'core/common_instructions.md').read_text()
schema=json.loads((root/'core/output_schema.json').read_text())
meta=json.loads((agent/'agent_metadata.json').read_text())
specialist=(agent/'specialist_instructions.md').read_text()
case_data=json.loads(case.read_text())
packet=f'''MASY1-GC 1800 EMERGING TECHNOLOGIES - SPECIALIST AGENT RUN\n\n{common}\n\n# AGENT METADATA\n{json.dumps(meta,indent=2)}\n\n# SPECIALIST ANALYTICAL INSTRUCTIONS\n{specialist}\n\n# CASE CONTEXT\n{json.dumps(case_data,indent=2)}\n\n# REQUIRED OUTPUT SCHEMA\n{json.dumps(schema,indent=2)}\n\nReturn JSON only. Use the evidence discipline above. If current external evidence is required and you cannot verify it, state the limitation rather than inventing support.\n'''
out=Path(a.out) if a.out else root/'work'/f'{agent.name}_{case.stem}_prompt.txt'
out.parent.mkdir(parents=True,exist_ok=True); out.write_text(packet)
print(out)
