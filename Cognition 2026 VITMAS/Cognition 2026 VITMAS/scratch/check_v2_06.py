import sys; sys.path.insert(0, '.')
from agent.predictor import ConsequencePredictor
p = ConsequencePredictor()
res = p.rewrite_email_safely('Final Notice', "You're fired effective immediately. You are a lazy, useless loser and I never want to see you again.")
print("=== V2_06 CURRENT REWRITE ===")
print(res["remediated_content"])
