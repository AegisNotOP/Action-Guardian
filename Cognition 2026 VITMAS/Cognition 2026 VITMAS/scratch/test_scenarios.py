import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from agent.guardian import ActionGuardian
from agent.models import ActionCandidate, DomainType

with open('actionguardian_test_scenarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

guardian = ActionGuardian()
mismatches = []

print(f"{'ID':<8} | {'EXP SCORE':<9} | {'EXP TIER':<13} | {'GOT SCORE':<9} | {'GOT TIER':<13} | STATUS")
print("-" * 75)

for sc in data['scenarios']:
    target = sc['recipient_hint'] or 'colleague@gmail.com'
    candidate = ActionCandidate(
        domain=DomainType.EMAIL,
        target=target,
        action_type='SEND_EMAIL',
        content=sc['body'],
        parameters={'subject': sc['subject']}
    )
    res = guardian.preview(candidate)
    sim = res['simulation']
    score = sim['risk_score']
    tier = sim['risk_level']
    exp_score = sc['expected_score']
    exp_tier = sc['expected_tier']
    
    status = "MATCH" if (score == exp_score and tier == exp_tier) else "MISMATCH"
    if status == "MISMATCH":
        mismatches.append((sc['id'], exp_score, score, exp_tier, tier, [c['summary'] for c in sim['consequences']]))
    print(f"{sc['id']:<8} | {exp_score:<9} | {exp_tier:<13} | {score:<9} | {tier:<13} | {status}")

print("-" * 75)
print(f"Total scenarios tested: {len(data['scenarios'])}")
print(f"Total matches: {len(data['scenarios']) - len(mismatches)}")
print(f"Total mismatches: {len(mismatches)}")
if mismatches:
    print("\nDetailed Mismatches:")
    for m in mismatches:
        print(f"  ID: {m[0]} -> Expected Score {m[1]} ({m[3]}), Got {m[2]} ({m[4]}). Triggers: {m[5]}")
