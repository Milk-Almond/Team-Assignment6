#!/usr/bin/env python3
import json, sys
from pathlib import Path
r=Path(__file__).resolve().parents[1]
responses=Path(sys.argv[1]) if len(sys.argv)>1 else r/'responses'
a=[json.loads((responses/f'{n}.json').read_text()) for n in ['primary','contrast_conservative','contrast_aggressive']]
for item in a:
 for factor in ['relative advantage','compatibility','complexity','trialability','observability']:
  assert factor in item['application_finding'].lower(),factor
 assert 'indeterminate' in item['application_finding'].lower()
 assert 'adoption agent retains' in item['recommendation_management_implication'].lower()
 assert 'early majority for' not in item['application_finding'].lower()
for item in a[1:]:
 for field in ['general_et_finding','application_finding','evidence']:
  assert item[field]==a[0][field],f'{field} changed with posture'
assert len({item['organization_specific_finding'] for item in a})==3
print('CONTRAST PASSED: 3 contexts; external evidence and five factors stable; timing differs; adoption boundary retained')
