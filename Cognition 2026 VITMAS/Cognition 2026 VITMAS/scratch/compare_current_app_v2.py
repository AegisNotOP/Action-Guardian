import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from agent.guardian import ActionGuardian
from agent.models import ActionCandidate, DomainType

json_path = 'C:/Users/samya/.gemini/antigravity/brain/85c41e0f-b9c8-41ad-b55a-19357d8417bd/unzipped_spec/actionguardian_scoring_v2.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

guardian = ActionGuardian()

print(f"{'ID':<7} | {'TITLE':<38} | {'CURRENT':<8} | {'V2 EXP':<8} | {'CURRENT TIER':<13} | {'V2 TIER':<9} | STATUS")
print("-" * 105)

mismatches = []
for sc in data['scenarios']:
    # Use recipient hint or dummy external/internal context
    target = "colleague@gmail.com"
    if "external" in sc.get("recipient_context", "").lower() or "journalist" in sc.get("recipient_context", "").lower():
        target = "external.analyst@gmail.com"
    elif "internal" in sc.get("recipient_context", "").lower():
        target = "team@company.com"
    if "all@" in sc.get("recipient_context", "").lower() or "300 people" in sc.get("recipient_context", "").lower():
        target = "all@company.com"

    cand = ActionCandidate(
        domain=DomainType.EMAIL,
        target=target,
        action_type="SEND_EMAIL",
        content=sc["body"],
        parameters={"subject": sc["subject"]}
    )
    sim = guardian.preview(cand)["simulation"]
    curr_score = sim["risk_score"]
    curr_tier = sim["risk_level"]
    v2_exp_score = sc["expected"]["total"]
    v2_exp_tier = sc["expected"]["tier"]

    is_match = (curr_score == v2_exp_score and curr_tier == v2_exp_tier)
    status = "MATCH" if is_match else "MISMATCH"
    if not is_match:
        mismatches.append({
            "id": sc["id"],
            "title": sc["title"],
            "current_score": curr_score,
            "v2_expected_score": v2_exp_score,
            "current_tier": curr_tier,
            "v2_expected_tier": v2_exp_tier,
            "content_rules": sc["inputs"]["content_rules"],
            "intent_type": sc["inputs"]["intent_type"]
        })
    print(f"{sc['id']:<7} | {sc['title'][:38]:<38} | {curr_score:<8} | {v2_exp_score:<8} | {curr_tier:<13} | {v2_exp_tier:<9} | {status}")

print("-" * 105)
print(f"Total scenarios: {len(data['scenarios'])}")
print(f"Current app vs V2 Expected Mismatches: {len(mismatches)}")
