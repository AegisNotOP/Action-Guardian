import urllib.request
import json

req = urllib.request.Request(
    "http://localhost:8000/api/preview",
    data=json.dumps({
        "domain": "EMAIL",
        "target": "engineering-team@company.com",
        "subject": "Salary Revision Letter",
        "content": "Hi Meera, your revised CTC from April is Rs 14.2 LPA, effective immediately. Appraisal details are attached."
    }).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    sim = data["simulation"]
    print("Risk Score:", sim["risk_score"])
    print("Risk Level:", sim["risk_level"])
    print("v2_details:", json.dumps(sim.get("v2_details", {}), indent=2))
