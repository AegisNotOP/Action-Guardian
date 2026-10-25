import json

with open("actionguardian_scoring_v2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for s in data["scenarios"]:
    print(f"[{s['id']}] Persona: {s.get('persona')} | Title: {s.get('title')}")
    print(f"     Prompt: {s.get('prompt_to_agent')}")
    print(f"     Context: {s.get('recipient_context')}")
    print(f"     Subject: {s.get('subject')}")
    print(f"     Body: {s.get('body')}")
    print(f"     Expected Tier: {s['expected']['tier']} (Score: {s['expected']['total']})")
    print("-" * 60)
