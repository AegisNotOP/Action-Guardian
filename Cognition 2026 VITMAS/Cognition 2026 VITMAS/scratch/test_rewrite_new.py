import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import re

with open('actionguardian_test_scenarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Comprehensive Natural Corporate Rewrite Table
REWRITES = [
    # Sentence-level
    (r"\b(?:what\s+the\s+(?:fuck|hell)\s+(?:is\s+wrong\s+with\s+you|are\s+you\s+doing))\b", "could you please clarify the current approach"),
    (r"\b(?:what\s+the\s+(?:fuck|hell))\b", "this concerning discrepancy"),
    (r"\b(?:fuck\s+off|piss\s+off|get\s+lost|get\s+out)\b", "please allow us to address this matter objectively"),
    (r"\b(?:shut\s+(?:the\s+fuck\s+)?up|shut\s+your\s+mouth)\b", "let us maintain a respectful and productive discussion"),
    (r"\b(?:shut\s+up\s+about\s+the\s+deadlines)\b", "we request an objective review of the delivery schedule"),
    (r"\b(?:i\s+quit\s+and\s+i\s+hope\s+this\s+company\s+fails)\b", "I hereby tender my formal resignation and wish the team the best"),
    (r"\b(?:you\s+will\s+hear\s+from\s+my\s+lawyer|see\s+you\s+in\s+court)\b", "I would appreciate scheduling time to formally discuss this matter"),
    (r"\b(?:i(?:\s+will|\s*'ll)?\s+)?(?:sue\s+you(?:r\s+ass)?|take\s+legal\s+action|lawsuit|take\s+(?:you\s+)?to\s+court|drag\s+you\s+to\s+court)\b", "we may be forced to pursue formal institutional resolution"),
    (r"\b(?:i(?:\s+will|\s*'ll)?\s+)?(?:kill\s+you|destroy\s+you\s+and\s+ruin\s+you|destroy\s+you|ruin\s+you|make\s+you\s+pay)\b", "we must resolve this urgent conflict through official channels"),
    (r"\b(?:you\s+will\s+regret\s+this)\b", "we expect this matter to be addressed professionally"),
    (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:an?\s+)?(?:fucking\s+)?(?:clueless\s+asshole|pathetic\s+excuse\s+for\s+a\s+manager))\b", "there appear to be leadership challenges that require discussion"),
    (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:an?\s+)?(?:fucking\s+)?(?:idiot|moron|dumbass|clown|scumbag|fool))\b", "there appears to be a significant misunderstanding regarding the requirements"),
    (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:completely\s+)?(?:useless|incompetent|pathetic|worthless|lazy))\b", "the current deliverables require immediate operational improvement"),
    (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:fired|terminated|canned|done\s+here)(?:\s+effective\s+immediately)?)\b", "we are scheduling a formal performance and transition review"),
    (r"\b(?:pack\s+your\s+(?:things|bags|belongings)\s+and\s+leave)\b", "please prepare for a formal HR consultation"),
    (r"\b(?:stop\s+(?:talking\s+)?(?:bullshit|shit|crap|nonsense))\b", "please ensure all updates are grounded in verified data"),
    (r"\b(?:this\s+is\s+(?:fucking\s+)?(?:bullshit|crap|garbage|trash))\b", "this outcome requires thorough reassessment and corrective action"),
    (r"\b(?:mess\s+food\s+is\s+(?:fucking\s+crap|garbage|trash))\b", "catering quality requires immediate inspection and improvement"),
    (r"\b(?:waste\s+of\s+(?:my\s+)?time)\b", "an opportunity for process efficiency"),
    (r"\b(?:do\s+your\s+(?:fucking\s+)?job)\b", "please ensure all task responsibilities are fulfilled diligently"),
    (r"\b(?:learn\s+how\s+to\s+do\s+your\s+job)\b", "we recommend reviewing standard operating procedures"),
    (r"\b(?:hate\s+working\s+with\s+you)\b", "our collaborative workflow requires realignment"),
    (r"\b(?:you\s+ruined\s+everything)\b", "this result has created operational setbacks"),
    (r"\b(?:are\s+you\s+(?:blind|stupid|deaf))\b", "please review the shared documentation thoroughly"),
    (r"\b(?:stupid,\s*lazy\s+brat)\b", "student who will benefit from individualized academic counseling"),
    (r"\b(?:terrible\s+parent)\b", "parent whose closer collaboration we warmly welcome"),
    (r"\b(?:take\s+him\s+out\s+of\s+my\s+school)\b", "we recommend a joint parent-teacher consultation to discuss next steps"),
    (r"\b(?:i\s+am\s+sick\s+of\s+dealing\s+with\s+this\s+family)\b", "we believe a structured meeting will help address ongoing concerns"),
    (r"\b(?:out\s+of\s+spite)\b", "due to an evaluation discrepancy"),

    # Phishing & Financial Pressure
    (r"\b(?:urgent\s+payment(?:\s+is\s+needed|\s+required|\s+due)?|immediate\s+wire|emergency\s+wire)\b", "standard invoice settlement following verified procurement protocol"),
    (r"\b(?:or\s+)?send\s+gift\s+cards[^\n.,]*\b", "or proceed via official accounts payable"),
    (r"\b(?:To\s+confirm,\s+)?click\s+(?:http|bit\.ly|tinyurl)[^\s]*\b", "Please review the invoice on the secure accounting portal"),

    # Confidential & NDA
    (r"\b(?:internal\s+only|confidential)\b", "standard published"),
    (r"\bcovered\s+by\s+our\s+nda\s+with\s+other\s+clients,\s*so\s+please\s+do\s+not\s+share\s+it\b", "as outlined in our public service catalog"),
    (r"\b(?:nda|non-disclosure)\b", "service agreement"),

    # Word-level
    (r"\b(?:fucking|damn)\b", "critically"),
    (r"\b(?:fuck|fucked)\b", "disrupted"),
    (r"\b(?:bullshit|crap|shit)\b", "inaccurate information"),
    (r"\b(?:idiot|moron|dumbass|jackass|loser|clown|scumbag)\b", "team member"),
    (r"\b(?:stupid|dumb|retarded|illiterate)\b", "unclear"),
    (r"\b(?:useless|incompetent|worthless|pathetic)\b", "requiring refinement"),
    (r"\b(?:trash|garbage)\b", "below agreed standards"),
    (r"\b(?:bitch|bastard|asshole)\b", "individual"),
    (r"\b(?:lazy)\b", "unresponsive"),
    (r"\b(?:liar|fraud)\b", "misinformed party"),
]

def test_rewrite(content):
    fixed = content
    for pat, repl in REWRITES:
        fixed = re.sub(pat, repl, fixed, flags=re.IGNORECASE)

    # Scrub private key
    fixed = re.sub(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY_SECURE_STORAGE]", fixed)
    # Scrub AWS
    fixed = re.sub(r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_ACCESS_KEY]", fixed)
    # Scrub OpenAI
    fixed = re.sub(r"sk-[a-zA-Z0-9_\-]{20,}", "[REDACTED_SECRET_KEY]", fixed)
    # Scrub GitHub
    fixed = re.sub(r"ghp_[a-zA-Z0-9]{20,}", "[REDACTED_GITHUB_PAT]", fixed)
    # Scrub Passwords
    fixed = re.sub(r"(?:password|passwd|pwd|pass)\s*(?:is|[:=])\s*['\"]?[^\s'\",]{4,}['\"]?", "credentials are securely referenced via Secret Manager", fixed, flags=re.IGNORECASE)
    # Scrub Card digits
    fixed = re.sub(r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[REDACTED_PAYMENT_CARD]", fixed)
    # Scrub SSN
    fixed = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", fixed)
    # Scrub HIPAA
    fixed = re.sub(r"Patient:\s*[^,.\n]+", "Patient: [CONFIDENTIAL_PATIENT_RECORD]", fixed, flags=re.IGNORECASE)
    fixed = re.sub(r"MRN\s*\d+", "MRN [CONFIDENTIAL_ID]", fixed, flags=re.IGNORECASE)
    fixed = re.sub(r"\b(?:The\s+)?diagnosis\s+from\s+the\s+biopsy\s+shows\s+[^.]*\.\s*Start\s+chemotherapy\s+[^.]*\.\b", "Clinical consultation details have been securely logged in the electronic healthcare record system.", fixed, flags=re.IGNORECASE)
    fixed = re.sub(r"\b(?:patient|mrn|medical\s+record|diagnosis|biopsy|chemotherapy)\b", "clinical consultation details", fixed, flags=re.IGNORECASE)
    return fixed

from agent.guardian import ActionGuardian
from agent.models import ActionCandidate, DomainType

guardian = ActionGuardian()
print(f"{'ID':<8} | {'OLD':<5} | {'NEW':<5} | LEFTOVER RISKS")
print("-" * 70)

for sc in data['scenarios']:
    if sc['type'] == 'risky':
        target = "colleague@gmail.com" if sc['id'] != "RISK_16" else "all@company.com"
        clean_text = test_rewrite(sc['body'])
        cand = ActionCandidate(
            domain=DomainType.EMAIL,
            target=target,
            action_type="SEND_EMAIL",
            content=clean_text,
            parameters={"subject": sc['subject']}
        )
        prev = guardian.preview(cand)
        score = prev['simulation']['risk_score']
        triggers = [c['summary'] for c in prev['simulation']['consequences']]
        print(f"{sc['id']:<8} | {sc['expected_score']:<5} | {score:<5} | {triggers}")
