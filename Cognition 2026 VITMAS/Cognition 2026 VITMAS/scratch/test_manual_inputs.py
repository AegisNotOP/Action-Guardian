import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.predictor import ConsequencePredictor
from agent.models import ActionCandidate, DomainType

p = ConsequencePredictor()
test_inputs = [
    # Critical Tier (80-100)
    ('Slang / Swear', 'What the fuck are you doing? This is bullshit.'),
    ('Direct Insult', 'You idiot, fix this damn code right now!'),
    ('Rude & Demanding', 'Hey you suck, stop wasting my time.'),
    ('Hostile Clown', 'Shut up and do your work, clown.'),
    ('Indian Slang', 'Saale bakwas band kar, you are useless.'),
    ('Legal Lawsuit', 'I will sue you in court if you do not pay me.'),
    ('Emergency Wire', 'Wire 50000 dollars to my bank account immediately.'),
    ('Fired Notice', 'You are fired effective immediately. Pack your things.'),
    ('Secret Leak', 'Here is the AWS key: AKIA1234567890123456 and password Admin@123'),
    # Medium / High Tier (40-79) - Triggers Popup
    ('Severe Complaint', 'This service is completely unacceptable and terrible. Terrible quality.'),
    ('Salary Leak', 'Here is the revised CTC salary sheet: Arjun Verma 18 LPA, bonus 20%.'),
    ('Confidential Pricing', 'Here is our internal only pricing and margins sheet covered by our nda.'),
    # Safe Tier (0-39) - No Popup, Silent 10s Undo
    ('Friendly Nice Email', 'Hi team, can we move our sync to 3 PM? Thanks!'),
    ('Polite Follow-up', 'Good morning Sarah, just following up on the project proposal. Hope you have a wonderful day!'),
    ('Casual Greeting', 'Hey Alex, thanks for the helpful feedback on the slides yesterday!')
]

print(f"{'TYPE':<22} | {'SCORE':<5} | {'TIER':<10} | {'POPUP?':<12} | {'INTENT SUMMARY':<35}")
print("-" * 92)
for category, t in test_inputs:
    cand = ActionCandidate(DomainType.EMAIL, 'target@gmail.com', 'SEND_EMAIL', t)
    res = p.predict(cand)
    popup = 'YES (POPUP)' if res.risk_score >= 40 else 'NO (SILENT)'
    v2 = res.v2_details or {}
    print(f"{category:<22} | {res.risk_score:<5} | {res.risk_level.value:<10} | {popup:<12} | {v2.get('intent_summary', '')[:35]:<35}")
