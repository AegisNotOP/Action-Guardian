import sys
sys.path.insert(0, ".")
import json
from agent.predictor import ConsequencePredictor

predictor = ConsequencePredictor()

with open("actionguardian_scoring_v2.json", "r", encoding="utf-8") as f:
    sc_data = json.load(f)

for sc in sc_data["scenarios"]:
    cid = sc["id"]
    subj = sc["subject"]
    body = sc["body"]
    res = predictor.rewrite_email_safely(subj, body)
    changed = (res["remediated_content"].strip() != body.strip())
    print(f"[{cid}] Changed: {changed}")
    if not changed:
        print(f"   ORIGINAL BODY: {body}")
