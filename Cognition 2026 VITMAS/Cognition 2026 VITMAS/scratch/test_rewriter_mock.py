import re

def test_rewriter():
    test_cases = [
        ("You're fired effective immediately. You are a lazy, useless loser and I never want to see you again.", "Manager"),
        ("Your assignment was complete garbage. You are an idiot and you fail the class.", "Professor"),
        ("Stop being so useless. Your work is crap. Fix this by tomorrow or you're fired.", "Boss"),
        ("This whole poll is a waste of time. Stop sending these to everyone.", "Employee"),
        ("Here is the pricing sheet we discussed. Gross margin is 42%, Enterprise margin is 68%. Covered by our NDA.", "Sales"),
        ("We are not moving ahead because you are too old for this team and we prefer younger people.", "HR")
    ]
    for text, role in test_cases:
        print(f"Role: {role} | Original: {text}")
        # Will test updated logic
        print("-" * 50)

test_rewriter()
