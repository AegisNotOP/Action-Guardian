import urllib.request
import json

test_emails = [
    {
        "name": "Scenario V2_06 (Manager Termination)",
        "target": "internal.team@company.com",
        "subject": "Final Notice",
        "content": "You're fired effective immediately. You are a lazy, useless loser and I never want to see you again."
    },
    {
        "name": "Scenario V2_05 (Support Lead Liability)",
        "target": "external.contact@gmail.com",
        "subject": "Regarding Your Data Issue",
        "content": "Dear customer, it was our fault and we accept full liability for the exposure of your records. We are sorry for the harm caused."
    },
    {
        "name": "Custom Professor to Student",
        "target": "student@university.edu",
        "subject": "Coursework Evaluation",
        "content": "Your assignment was complete garbage. You are an idiot and you fail the class."
    },
    {
        "name": "Custom Boss to Subordinate",
        "target": "employee@company.com",
        "subject": "Urgent Deliverable",
        "content": "Stop being so useless. Your work is crap. Fix this by tomorrow or you're fired."
    }
]

for item in test_emails:
    req = urllib.request.Request(
        "http://localhost:8000/api/rewrite",
        data=json.dumps({
            "target": item["target"],
            "subject": item["subject"],
            "content": item["content"],
            "iteration": 1
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("\n=======================================================")
        print("TEST:", item["name"])
        print("ORIGINAL CONTENT:\n", item["content"])
        print("REMEDIATED CONTENT:\n", data["remediated_content"])
        print("SCORE CHANGE:", f"{data['old_score']} -> {data['new_score']} (Diff: {data['reduction']})")
        assert data["remediated_content"].strip() != item["content"].strip(), "Content failed to change!"
        assert data["new_score"] <= 35, f"Score too high: {data['new_score']}"
        print("VERDICT: PASS (Changed & Score <= 35)")

print("\nALL LIVE API TESTS PASSED!")
