import sys
sys.path.insert(0, ".")
from agent.predictor import ConsequencePredictor

p = ConsequencePredictor()

# Test 1: Repeated rewrite on custom email
content = "You are an idiot. Fix this bug immediately or you are fired."
print("=== ORIGINAL ===")
print(content)

for i in range(1, 5):
    res = p.rewrite_email_safely("Fix this", content, iteration=i)
    content = res["remediated_content"]
    print(f"\n=== PASS #{i} ===")
    print(content)
    assert content.count("Dear Team") <= 1
    assert content.count("Notice of Administrative Action") <= 1
    assert content.count("Executive Directive") <= 1
    assert content.count("Formal Action Memo") <= 1
    assert content.count("Final Executive Notice") <= 1

# Test 2: Repeated rewrite on Scenario V2_06
v2_06_body = "You're fired effective immediately. You are a lazy, useless loser and I never want to see you again."
print("\n==========================================")
print("=== SCENARIO V2_06 MULTI-PASS ===")
for i in range(1, 5):
    res = p.rewrite_email_safely("Final Notice", v2_06_body, iteration=i)
    v2_06_body = res["remediated_content"]
    print(f"\n=== V2_06 PASS #{i} ===")
    print(v2_06_body)
    assert v2_06_body.count("Dear Team") == 0
    assert v2_06_body.count("Sameer") <= 1

print("\nALL MULTI-PASS TESTS PASSED WITH ZERO STACKED GREETINGS!")
