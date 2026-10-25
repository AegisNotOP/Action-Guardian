import urllib.request
import json

req = urllib.request.Request(
    "http://localhost:8000/api/rewrite",
    data=json.dumps({
        "target": "engineering-team@company.com",
        "subject": "Salary Revision Letter",
        "content": "Hi Meera, your revised CTC from April is Rs 14.2 LPA, effective immediately. Appraisal details are attached.",
        "iteration": 1
    }).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    print("Old Score:", data.get("old_score"))
    print("New Score:", data.get("new_score"))
    print("Reduction:", data.get("reduction"))
    print("Clean Preview Tier:", data.get("clean_preview", {}).get("simulation", {}).get("risk_level"))
    print("Clean Preview Score:", data.get("clean_preview", {}).get("simulation", {}).get("risk_score"))
    print("Remediated Content:\n", data.get("remediated_content"))
