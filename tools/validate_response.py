#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys

REQUIRED=['agent','analytical_question','general_et_finding','application_finding','organization_specific_finding','evidence','contrary_evidence_or_limitations','confidence_and_uncertainty','value_opportunity_implication','risk_governance_implication','recommendation_management_implication','change_monitoring_triggers','abstention_or_more_information_needed']
ARRAYS=['evidence','contrary_evidence_or_limitations','change_monitoring_triggers','abstention_or_more_information_needed']
STRINGS=['analytical_question','general_et_finding','application_finding','organization_specific_finding','confidence_and_uncertainty','value_opportunity_implication','risk_governance_implication','recommendation_management_implication']
p=argparse.ArgumentParser(description='Validate the basic MASY1800 specialist-agent response contract.')
p.add_argument('response')
a=p.parse_args(); path=Path(a.response)
try: data=json.loads(path.read_text())
except Exception as e: raise SystemExit(f'INVALID JSON: {e}')
errors=[]
if not isinstance(data,dict): errors.append('Top-level response must be an object.')
else:
    for k in REQUIRED:
        if k not in data: errors.append(f'Missing required field: {k}')
    for k in STRINGS:
        if k in data and not isinstance(data[k],str): errors.append(f'{k} must be a string')
    for k in ARRAYS:
        if k in data and not isinstance(data[k],list): errors.append(f'{k} must be an array')
    if 'agent' in data:
        if not isinstance(data['agent'],dict): errors.append('agent must be an object')
        else:
            for k in ['name','specialty','version']:
                if k not in data['agent'] or not isinstance(data['agent'][k],str): errors.append(f'agent.{k} must be a string')
    if isinstance(data.get('evidence'),list):
        for i,e in enumerate(data['evidence']):
            if not isinstance(e,dict): errors.append(f'evidence[{i}] must be an object'); continue
            for k in ['claim','source_or_reference','date_or_recency','evidence_type','notes']:
                if k not in e or not isinstance(e[k],str): errors.append(f'evidence[{i}].{k} must be a string')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-',e)
    sys.exit(1)
print('VALIDATION PASSED')
