#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, json, re

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description='Create a student specialist-agent folder from the frozen template.')
p.add_argument('slug', help='Folder name, e.g. diffusion_agent')
p.add_argument('display_name', help='Agent display name')
p.add_argument('--specialty', default='REPLACE WITH SPECIALIST DIMENSION')
a = p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_-]+', a.slug):
    raise SystemExit('Slug may contain only letters, numbers, underscore, and hyphen.')
src = root/'agents'/'_template'; dst=root/'agents'/a.slug
if dst.exists(): raise SystemExit(f'{dst} already exists')
shutil.copytree(src,dst)
meta_path=dst/'agent_metadata.json'; meta=json.loads(meta_path.read_text())
meta['name']=a.display_name; meta['specialty']=a.specialty
meta_path.write_text(json.dumps(meta,indent=2))
print(f'Created {dst}')
print('Next: edit specialist_instructions.md and the case JSON files.')
