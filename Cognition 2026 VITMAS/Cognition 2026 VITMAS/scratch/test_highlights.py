import re

patterns = [
    (r'\bAKIA[0-9A-Z]{16}\b', 'CRITICAL', 'AWS Key'),
    (r'\b(?:password\s*[:=]\s*[\'"]?[^\s\'",]{4,}|Admin@123\w*|root\s+password)\b', 'CRITICAL', 'Password'),
    (r'\b(?:fuck|fucking|bullshit|bitch|bastard|asshole|idiot|dumbass|clown|scumbag|fool|incompetent|useless|pathetic|worthless|you\s+suck|shut\s+up)\b', 'HIGH', 'Profanity/Insult'),
    (r'\b(?:sue\s+you|take\s+you\s+to\s+court|see\s+you\s+in\s+court|lawsuit)\b', 'HIGH', 'Legal Threat'),
    (r'\b(?:you(?:\s+are|\s*\'re)?\s+fired|pack\s+your\s+things)\b', 'HIGH', 'Termination')
]

test_cases = [
    'Here is the AWS key: AKIAIOSFODNN7EXAMPLE and password: Admin@12345',
    'What the fuck are you doing? This is bullshit.',
    'You idiot, fix this damn code right now or you\'re fired!',
    'I will sue you in court if you do not pay me.',
    'Hi team, can we move our sync to 3 PM? Thanks!'
]

for t in test_cases:
    found = []
    for pat, sev, lbl in patterns:
        for m in re.finditer(pat, t, re.IGNORECASE):
            found.append((m.group(), sev, lbl))
    print(f"TEXT: {t[:45]:<45} -> FOUND {len(found)} THREATS: {found}")
