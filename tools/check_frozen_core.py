#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
root=Path(__file__).resolve().parents[1]
manifest=root/'FROZEN_CORE_SHA256.txt'
errors=[]
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    expected, rel=line.split('  ',1)
    p=root/rel
    if not p.exists(): errors.append(f'MISSING: {rel}'); continue
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=expected: errors.append(f'CHANGED: {rel}')
if errors:
    print('FROZEN CORE CHECK FAILED')
    for e in errors: print('-',e)
    sys.exit(1)
print('FROZEN CORE INTACT')
