import re

def clean_repeated_greetings(text: str) -> str:
    # Remove stacked duplicate greetings
    pats = [
        r'^(?:\s*Dear\s+Team,?\s*\n+)+',
        r'^(?:\s*Dear\s+Colleague,?\s*\n+)+',
        r'^(?:\s*Sameer,?\s*\n+)+',
        r'^(?:\s*Student,?\s*\n+)+'
    ]
    cleaned = text.strip()
    for p in pats:
        if re.search(p, cleaned, re.IGNORECASE):
            # Replace multiple with single
            match = re.search(p, cleaned, re.IGNORECASE).group(0)
            first_line = match.strip().split('\n')[0].strip()
            cleaned = re.sub(p, first_line + '\n\n', cleaned, count=1, flags=re.IGNORECASE)
    return cleaned

test1 = "Dear Team,\n\nDear Team,\n\nDear Team,\n\nHi Meera, your revised CTC is Rs 14.2 LPA."
print("Cleaned:\n", clean_repeated_greetings(test1))
