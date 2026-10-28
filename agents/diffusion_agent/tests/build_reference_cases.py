#!/usr/bin/env python3
"""Create transparent reference analyses for contract/contrast tests; no model call."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
base={
 'emerging_technology':'ChatGPT conversational generative AI',
 'intended_application':'Human-reviewed drafting of internal nonbinding documents from approved or synthetic inputs',
 'organization':'Hypothetical 120-person US professional-services firm',
 'industry_sector':'Professional services, unspecified specialization',
 'business_need':'Reduce first-draft effort while preserving accuracy and review',
 'users_stakeholders':'Analysts, reviewers, data owner and clients',
 'capabilities_constraints':'Document review workflow; no local baseline or approved data policy supplied',
 'risk_consequence_context':'Draft errors and confidential-data exposure could harm clients; no autonomous publication',
 'management_question':'What does diffusion evidence imply for the timing of evidence gathering, leaving adoption to the Adoption Agent?',
 'time_horizon':'Next six months from October 27, 2026'
}
postures={
 'primary':('Moderate fast follower','Clarify approved data and review requirements, establish baseline, then seek a bounded, permissioned evaluation within the six-month horizon.'),
 'contrast_conservative':('Conservative follower; unresolved confidentiality approval and limited reviewers','First resolve data authority and review capacity; use only synthetic examples for preparation until permission is granted.'),
 'contrast_aggressive':('Aggressive learner; approved isolated sandbox and staffed reviewers','Prepare a short isolated, permissioned comparison promptly; evaluate errors and reviewer burden before proposing expansion.')
}
evidence=[
 {'claim':'44% of US adults reported ever using ChatGPT in February 2026','source_or_reference':'https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/','date_or_recency':'Survey February 17–23, 2026; published June 17, 2026','evidence_type':'Original US adult survey','notes':'Ever-use, not regular workplace use or comparable firm deployment; 38% of employed adults reported work use of AI chatbots broadly.'},
 {'claim':'OpenAI reported more than one billion weekly users and 2.5 million businesses across products','source_or_reference':'https://openai.com/index/the-work-now-within-reach/','date_or_recency':'Published September 2026','evidence_type':'First-party company report','notes':'Global product reach and business count, not a firm-level application adoption denominator.'},
 {'claim':'OpenAI reported more than seven million ChatGPT for Work seats','source_or_reference':'https://openai.com/index/1-million-businesses-putting-ai-to-work/','date_or_recency':'Published November 5, 2025','evidence_type':'First-party company report','notes':'Seats are not active users; more than one million paying business customers also included API use.'}
]
mac='ChatGPT has broad observed individual reach, but the Rogers categories innovators, early adopters, early majority, late majority and laggards cannot be assigned to all firms from consumer counts. Population, geography and product usage differ.'
app=('Exact application and comparable professional-services peer stage: indeterminate. Rogers factors: relative advantage—possible draft speed, local quality-adjusted benefit unknown (inference); compatibility—approved inputs and human review are decisive (inference); complexity—verification and data handling add work (inference); trialability—bounded approved test is a proposed design, not observed diffusion; observability—accepted drafts, errors, rework and time could be measured, not yet observed. No standard, opinion leader or change agent was shown to cause peer spread.')
for name,(posture,timing) in postures.items():
 case=dict(base,adoption_posture=posture,additional_context='All external evidence and exact application are identical across the three cases; only organizational posture/capacity changes.')
 (root/'cases'/f'{name}.json').write_text(json.dumps(case,indent=2)+'\n')
 response={
  'agent':{'name':'Emerging Technology Diffusion Agent','specialty':'Rogers diffusion, peer position and timing evidence','version':'1.0-team-synthesis'},
  'analytical_question':'What has diffused at the general, exact-application and peer levels, and what information timing follows?',
  'general_et_finding':mac,'application_finding':app,
  'organization_specific_finding':f'{posture}: {timing} This is a context-specific timing interpretation, not a changed external prevalence estimate.',
  'evidence':evidence,'contrary_evidence_or_limitations':['Consumer ever-use and vendor customer/seat counts do not establish sustained human-reviewed drafting at comparable firms.','No organization-specific baseline, industry cohort or internal controls were supplied.'],
  'confidence_and_uncertainty':'Moderate for broad direction of spread; low for exact workflow, peer stage, causal Rogers factors and local value.',
  'value_opportunity_implication':'Measure quality-adjusted draft effort and accepted work before inferring benefit.',
  'risk_governance_implication':'Maintain human review and approved data handling; assess error and disclosure exposure.',
  'recommendation_management_implication':f'Diffusion timing only: {timing} Adoption Agent retains the final decision.',
  'change_monitoring_triggers':['Representative comparable-firm evidence of sustained use for the exact task','Local baseline, review-adjusted quality, time and incident measures','Approved data controls or changed policy'],
  'abstention_or_more_information_needed':['No numerical peer adoption rate or application Rogers category without a representative denominator','No final adoption approval or ROI claim']
 }
 (root/'responses'/f'{name}.json').write_text(json.dumps(response,indent=2)+'\n')
print('CREATED 3 case inputs and 3 authored reference analyses; no model call')
