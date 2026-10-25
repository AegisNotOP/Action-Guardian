import sys; sys.path.insert(0, '.')
from agent.predictor import ConsequencePredictor
p = ConsequencePredictor()

print('--- PROFESSOR TO STUDENT ---')
r1 = p.rewrite_email_safely('Grades', 'Your assignment was complete garbage. You are an idiot and you fail the class.')
print(r1['remediated_content'])

print('\n--- BOSS TO SUBORDINATE ---')
r2 = p.rewrite_email_safely('Warning', "Stop being so useless. Your work is crap. Fix this by tomorrow or you're fired.")
print(r2['remediated_content'])
