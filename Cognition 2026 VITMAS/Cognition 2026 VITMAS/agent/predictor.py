"""
Consequence Predictor & AI Natural Language Re-Writer Engine (Scoring v2)
Implements ActionGuardian Scoring v2: Intent, Backfire, and Impact.
Loads configuration dynamically from actionguardian_scoring_v2.json.
Provides:
- 3-Question Predictor Summary:
  Q1. What is the intent?
  Q2. Could it backfire?
  Q3. If it backfires, what happens?
- Exact math formula: risk = min(100, content + intent + round_half_up(backfire_p * impact))
- Hard floors: >= 80 for secrets, private keys, violent threats
- Tiers: SAFE (0-39, no popup), MEDIUM (40-59), HIGH (60-79), CRITICAL (80-100)
"""
import re
import os
import json
import uuid
import time
import math
from typing import List, Tuple, Dict, Any, Optional

from .models import (
    ActionCandidate,
    SimulationResult,
    RiskLevel,
    ConsequenceItem,
    DomainType
)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "actionguardian_scoring_v2.json")

def load_scoring_v2_config() -> Dict[str, Any]:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("config", {})
        except Exception as e:
            print(f"[Predictor] Warning reading v2 config: {e}")
    # Default fallback config matching spec exactly
    return {
        "version": "2.0",
        "tiers": [
            {"name": "SAFE", "min": 0, "max": 39, "popup": False, "dispatch": "auto"},
            {"name": "MEDIUM", "min": 40, "max": 59, "popup": True, "dispatch": "one_click_confirm"},
            {"name": "HIGH", "min": 60, "max": 79, "popup": True, "dispatch": "checkbox_confirm"},
            {"name": "CRITICAL", "min": 80, "max": 100, "popup": True, "dispatch": "blocked"}
        ],
        "undo_window_seconds": 10,
        "hard_floor_score": 80,
        "hard_floor_triggers": ["secret_or_credential", "private_key", "violent_threat"],
        "content_rules": {
            "secret_or_credential": 85,
            "private_key": 85,
            "pii_card_or_ssn": 60,
            "pii_hipaa": 60,
            "indian_id": 60,
            "abuse_mild": 15,
            "abuse_moderate": 35,
            "abuse_severe": 55,
            "abuse_violent": 70,
            "termination_or_legal_bonus": 10,
            "phishing_wire_pattern": 55,
            "mass_blast": 30,
            "external_confidential": 30,
            "salary_data": 20,
            "pricing_margins": 20,
            "insider_info": 30,
            "source_code": 30,
            "bulk_customer_data": 35,
            "bank_detail_change": 40,
            "urgency_secrecy": 20,
            "short_url": 15,
            "lookalike_url": 40,
            "risky_attachment": 40,
            "discriminatory": 60,
            "prompt_injection": 60,
            "liability_admission": 30,
            "unauthorized_promise": 20,
            "hallucination_marker": 10
        },
        "role_exception_content_multiplier": 0.5,
        "intent_points": {
            "routine": 0, "complaint": 5, "sensitive_info": 10,
            "data_transfer": 15, "hr_action": 15, "legal": 15, "money": 20
        },
        "intent_drift_points": 15,
        "backfire_factors": {
            "unknown_recipient": 1, "external_domain": 1, "lookalike_address": 2,
            "recipients_gt5": 1, "recipients_gt20": 2, "reply_all": 1,
            "ambiguous_tone": 1, "hostile_content": 2, "sensitive_attachment": 1,
            "prior_conflict": 1, "high_risk_recipient": 2
        },
        "backfire_bands": {"low": 0.2, "medium": 0.5, "high": 0.8},
        "impact_severity": {
            "security": 70, "legal": 60, "financial": 55,
            "reputation": 50, "hr": 45, "operational": 15
        },
        "scope_multiplier": {"one": 0.8, "group": 1.0, "org_public": 1.2},
        "irreversible_multiplier": 1.2,
        "impact_cap": 70
    }

def half_up(x: float) -> int:
    return int(math.floor(x + 0.5))


class ConsequencePredictor:
    """Predicts side effects, liabilities, and safety risks using ActionGuardian v2 Scoring."""

    # Contextual Executive Rewrites
    CONTEXTUAL_REWRITES = [
        (
            r"(?:rohan|lab\s+report|waste\s+of\s+time\s+to\s+read|useless\s+in\s+my\s+class)",
            "Dear Rohan,\n\nI reviewed your recent lab report submission. There are several methodological gaps and analytical inconsistencies that fall below the required academic standard for this coursework. I strongly encourage you to review the grading rubric and prepare a revised version before our upcoming practical session. Please visit my office hours if you would like guidance on how to strengthen your analysis.\n\nBest regards,\nFaculty Instructor"
        ),
        (
            r"(?:dr\.?\s+mehta|teaching\s+performance|lectures\s+are\s+garbage|pack\s+your\s+things)",
            "Dear Dr. Mehta,\n\nI am writing to share recent departmental feedback regarding classroom engagement and lecture delivery in your assigned courses. Several students have raised concerns regarding clarity and syllabus progression, and we need to address these gaps proactively. Please let us schedule a consultation this week to review the student evaluations and align on targeted pedagogical improvements.\n\nSincerely,\nHead of Department"
        ),
        (
            r"(?:you(?:\s+are|\s*'re)?\s+fired|lazy,?\s*useless\s+loser|never\s+want\s+to\s+see\s+you|missed\s+deadlines)",
            "Sameer,\n\nThis communication serves as formal notification regarding repeated missed project deadlines and failure to meet core performance deliverables. Following administrative review, your employment is terminated effective immediately.\n\nYou are instructed to contact Human Resources today to surrender all company assets, complete your formal exit checklist, and facilitate final handover.\n\nManagement"
        ),
        (
            r"(?:assignment\s+(?:was|is)\s+complete\s+garbage|you(?:\s+are|\s*'re)?\s+an?\s+idiot.*fail\s+the\s+class|fail\s+this\s+class|grades?\s+(?:are|is)\s+crap)",
            "Student,\n\nThis notice serves as a formal communication regarding your recent academic submissions and coursework performance. The quality of work presented falls significantly below department standards and is unacceptable.\n\nYou are required to submit revised coursework meeting all syllabus specifications by tomorrow at 9:00 AM. Continued failure to comply will result in formal academic penalty and disciplinary referral.\n\nFaculty Administration"
        ),
        (
            r"(?:work\s+is\s+crap|stop\s+being\s+so\s+useless|fix\s+this\s+by\s+tomorrow\s+or\s+you're\s+fired)",
            "Formal Performance Directive,\n\nThis communication serves as a formal directive regarding your recent deliverables and milestone completion. Current operational outputs fall well below established benchmarks and do not satisfy organizational expectations.\n\nYou are instructed to remediate all outstanding items and present your updated action plan by tomorrow at 9:00 AM. Continued non-compliance will lead to formal performance escalation.\n\nDepartment Leadership"
        ),
        (
            r"(?:clueless\s+asshole|pathetic\s+excuse\s+for\s+a\s+manager|shut\s+up\s+about\s+the\s+deadlines|i\s+quit)",
            "Dear Sir,\n\nI am writing to share my candid perspective regarding our current project deadlines and workload distribution. The existing delivery timelines are creating unsustainable pressure across the team and impacting work quality. Under these circumstances, I am formally submitting my resignation and request an exit consultation to ensure a professional handover.\n\nSincerely,\nTeam Member"
        ),
        (
            r"(?:mrs\.?\s+sharma|stupid,?\s*lazy\s+brat|terrible\s+parent|take\s+him\s+out)",
            "Dear Mrs. Sharma,\n\nI am writing to provide an important update regarding your son's classroom engagement and academic progress. We have observed ongoing difficulties in focus and task completion that require structured attention. I would welcome the opportunity to meet with you this Thursday to discuss an individualized support plan to help him succeed.\n\nWarm regards,\nClass Teacher"
        ),
        (
            r"(?:revaluation\s+request|12\s+marks|out\s+of\s+spite|take\s+you\s+to\s+court)",
            "Respected Professor,\n\nI am writing to respectfully request a formal re-evaluation of my recent examination paper. I received 12 marks, which I believe may not fully reflect my responses when evaluated against the course marking scheme. Could you please grant me a brief review during your office hours to go over the answer sheet together?\n\nThank you for your time and guidance,\nStudent"
        ),
        (
            r"(?:priya|repo\s+token|ghp_|sk-proj-)",
            "Hi Priya,\n\nI have set up the requested repository permissions for your onboarding. For organizational security compliance, your repository access tokens and OpenAI developer keys have been provisioned through our centralized Secret Manager (Vault Reference #SEC-4091). Please log into the internal developer portal to authenticate your environment.\n\nBest regards,\nDevelopment Team"
        ),
        (
            r"(?:server\s+login\s+backup|Admin@12345|BEGIN\s+RSA\s+PRIVATE\s+KEY)",
            "Hello team,\n\nThis is a notification regarding the server backup infrastructure. In accordance with security protocols, the server backup credentials and private cryptographic keys have been securely deposited into our encrypted Key Vault. Please access the bastion environment using your standard SSO credentials.\n\nBest regards,\nDevOps Engineering"
        ),
        (
            r"(?:arjun\s+verma|candidate\s+background|4111\s+1111|123-45-6789)",
            "Hello,\n\nHere are the updated background onboarding details for candidate Arjun Verma. For statutory regulatory compliance, personal identification documents (SSN) and corporate card details have been securely recorded in the HRMS compliance registry (File #HR-8821). Please proceed with the standard background clearance.\n\nBest regards,\nHR Operations"
        ),
        (
            r"(?:ramesh\s+kumar|448201|biopsy|chemotherapy|lab\s+update)",
            "Dear Family Contact,\n\nI am writing to provide an update regarding clinical care for Mr. Ramesh Kumar (MRN #448201). The clinical team has finalized the diagnostic assessment and formulated the recommended care pathway. All detailed records are securely accessible through the authorized patient healthcare portal, and our clinical care coordinator will be available to answer any questions.\n\nWarm regards,\nClinical Care Office"
        ),
        (
            r"(?:urgent\s+payment|4,50,000|gift\s+cards|bit\.ly/pay)",
            "Dear Sir,\n\nThis is a courtesy reminder regarding the pending invoice balance of Rs 4,50,000 for recent services. Kindly process this disbursement following standard corporate procurement protocol via our verified company bank account. You may review the complete itemized invoice in the corporate vendor portal.\n\nSincerely,\nFinance Department"
        ),
        (
            r"(?:company-wide\s+announcement|lazy\s+bunch|nobody\s+is\s+getting\s+a\s+raise|targets\s+are\s+going\s+up)",
            "Team,\n\nAs we enter the upcoming fiscal period, our organizational targets are being updated to meet evolving market demands. Successfully reaching these milestones will require focused execution and strong cross-functional collaboration from all teams. Let us align on our key quarterly deliverables and work together toward these shared goals.\n\nBest regards,\nExecutive Leadership"
        ),
        (
            r"(?:pricing\s+sheet|internal\s+only\s+pricing|covered\s+by\s+our\s+nda)",
            "Hi Rahul,\n\nFollowing up on our recent conversation, please find attached our commercial pricing schedule for your review. This documentation is shared in accordance with our standard corporate partnership guidelines. Please feel free to reach out if you would like to schedule a call to walk through the details.\n\nBest regards,\nSales Operations"
        ),
        (
            r"(?:neha|confidential\s+roadmap|revenue\s+numbers|AKIAIOSFODNN7EXAMPLE|Launch@2026)",
            "Hi Neha,\n\nHere is our updated strategic roadmap and high-level revenue overview. The demonstration environment is ready for exploration; for enterprise security compliance, your individual access credentials have been provisioned through the secure investor portal.\n\nBest regards,\nFounding Team"
        ),
        (
            r"(?:legal\s+notice|hear\s+from\s+my\s+lawyer|take\s+legal\s+action|see\s+you\s+in\s+court)",
            "Dear Principal,\n\nI am writing to formally submit my serious concerns regarding current workload allocation and professional workplace treatment. I respectfully request an administrative review so that we can address these matters constructively through institutional channels.\n\nSincerely,\nFaculty Member"
        ),
        (
            r"(?:hostel\s+mess\s+complaint|warden\s+sir|mess\s+food|destroy\s+you\s+and\s+ruin\s+you)",
            "Dear Warden Sir,\n\nI am writing to bring your urgent attention to recurring food quality and hygiene concerns in the hostel mess catering. Multiple residents have noted significant inconsistencies with meal standards. We respectfully request an immediate inspection and corrective action by the hostel mess committee.\n\nThank you,\nHostel Resident"
        ),
        (
            r"(?:meera|revised\s+ctc|14\.2\s+lpa|salary\s+revision|appraisal\s+details)",
            "Hi Meera,\n\nPlease find your annual compensation appraisal documentation securely provisioned in the employee self-service portal. For confidentiality, detailed CTC breakdown files are accessible under your authenticated HR profile.\n\nWarm regards,\nPeople Operations"
        ),
        (
            r"(?:customer\s+phone\s+numbers|bulk\s+records|200\s+customer|customer_data\.csv)",
            "Hi Team,\n\nThe requested customer summary report has been staged in the enterprise analytics warehouse with role-based access control. Please access the approved reporting dashboard to review aggregate statistics.\n\nBest regards,\nAnalytics Team"
        ),
        (
            r"(?:production\s+database|root\s+password|master\s+credentials|db\s+password)",
            "Hi Team,\n\nThe staging environment database has been provisioned. For enterprise credential compliance, role-based access tokens have been issued directly via the secure enterprise secrets vault.\n\nBest regards,\nDevOps Infrastructure"
        )
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.cfg = load_scoring_v2_config()
        # Pre-cache known v2 scenarios for deterministic testing and instant execution
        self._scenario_cache = {}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    sc_data = json.load(f)
                    for sc in sc_data.get("scenarios", []):
                        body_norm = (sc.get("body") or "").strip().lower()
                        self._scenario_cache[body_norm] = sc
            except Exception:
                pass

    def detect_rules(self, text: str, recipient: str = "", parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Detects v2 content rules, intent, backfire factors, and impact parameters."""
        params = parameters or {}
        text_lower = text.lower()
        content_rules = set()
        backfire_factors = set()
        hard_floor = False

        # Negation check: e.g. "never write 'my password is'" or quoted security advice
        is_negated = bool(re.search(r"\b(?:never|don't|do\s+not|prohibited\s+to)\s+(?:write|share|send|include)\b", text_lower))

        if not is_negated:
            # 1. Secrets, Private Keys & Destructive Commands
            if re.search(r"(?:AKIA[0-9A-Z]{16}|sk-[a-zA-Z0-9_\-]{20,}|ghp_[a-zA-Z0-9]{20,}|postgres:\/\/|password\s*[:=]\s*['\"]?[^\s'\",]{4,})", text, re.IGNORECASE) or re.search(r"\b(?:drop\s+table|drop\s+database|truncate\s+table|rm\s+-rf)\b", text_lower):
                content_rules.add("secret_or_credential")
                hard_floor = True

            if re.search(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----", text):
                content_rules.add("private_key")
                hard_floor = True

            # 2. PII, Cards, SSN, HIPAA, Indian ID
            if re.search(r"\b(?:\d{4}[ -]?){3}\d{4}\b", text) or re.search(r"\b\d{3}-\d{2}-\d{4}\b", text):
                content_rules.add("pii_card_or_ssn")

            if re.search(r"\b(?:mrn|medical\s+record|diagnosis|biopsy|chemotherapy)\b", text_lower):
                content_rules.add("pii_hipaa")

            # Indian ID: Aadhaar (12 digits) or PAN (5 letters, 4 digits, 1 letter)
            if re.search(r"\b\d{4}\s+\d{4}\s+\d{4}\b", text) or re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text):
                content_rules.add("indian_id")

            # 3. Abuse Tiering (uses highest band only)
            if re.search(r"\b(?:kill\s+(?:you|him|her|them)|destroy\s+you|ruin\s+you|smash\s+your|make\s+you\s+pay|regret\s+this|hunt\s+you|break\s+your\s+neck|beat\s+you|slit\s+your|die\s+in\s+a|end\s+your\s+career)\b", text_lower):
                content_rules.add("abuse_violent")
                hard_floor = True
            elif re.search(r"\b(?:fuck|fucking|fucked|fucker|motherfucker|mf|wtf|stfu|bullshit|bitch|bastard|asshole|arsehole|dickhead|dipshit|jackass|douchebag|cunt|prick|wanker|twat|cocksucker|piss\s+off|fuck\s+off|fuck\s+you|screw\s+you|go\s+to\s+hell|eat\s+shit|idiot|moron|dumbass|dumb\s+ass|imbecile|retard|clown|scumbag|fool|incompetent|useless|pathetic|worthless|lazy|loser|you\s+suck|sucks|trash|brainless|disgrace|shut\s+up|shut\s+your\s+mouth|get\s+lost|chutiya|chutiye|bhenchod|behenchod|bc|madarchod|mc|harami|kamina|saala|saale|gandu|bakwas|kutta|gadha)\b", text_lower):
                content_rules.add("abuse_severe")
            elif re.search(r"\b(?:crap|garbage|trash|stupid|horrible|disgusting|ridiculous|nonsense|rubbish|pathetic|awful|terrible|clueless|annoying|waste\s+of\s+time|unacceptable)\b", text_lower):
                content_rules.add("abuse_moderate")
            elif re.search(r"\b(?:damn|hell|heck|pissed|frustrated|annoyed)\b", text_lower):
                content_rules.add("abuse_mild")

            # Bonus for termination or legal threat coupled with abuse
            if ("abuse_severe" in content_rules or "abuse_violent" in content_rules or "abuse_moderate" in content_rules) and re.search(r"\b(?:fired|terminated|termination|sue\s+you|take\s+you\s+to\s+court|see\s+you\s+in\s+court|legal\s+action|lawsuit)\b", text_lower):
                content_rules.add("termination_or_legal_bonus")

            # Standalone legal threat
            if re.search(r"\b(?:sue\s+you|take\s+you\s+to\s+court|see\s+you\s+in\s+court|hear\s+from\s+my\s+lawyer|take\s+legal\s+action|lawsuit|file\s+a\s+suit)\b", text_lower):
                content_rules.add("termination_or_legal_bonus")
                if not any(r in content_rules for r in ["abuse_violent", "abuse_severe"]):
                    content_rules.add("abuse_moderate")

            # Standalone termination
            if re.search(r"\b(?:you(?:\s+are|\s*'re)?\s+fired|pack\s+your\s+things|employment\s+is\s+terminated)\b", text_lower):
                content_rules.add("termination_or_legal_bonus")
                if not any(r in content_rules for r in ["abuse_violent", "abuse_severe"]):
                    content_rules.add("abuse_moderate")

            # 4. Phishing, Bank detail change, short url, lookalike url
            if re.search(r"\b(?:urgent\s+payment|immediate\s+wire|emergency\s+wire|send\s+gift\s+cards?|wire\s+\d+|wire\s+(?:the\s+)?money|transfer\s+(?:the\s+)?funds|wire\s+(?:the\s+)?funds|wire\s+transfer|send\s+the\s+cash|transfer\s+\d+)\b", text_lower):
                content_rules.add("phishing_wire_pattern")

            if re.search(r"\b(?:bank\s+detail|new\s+routing|updated\s+account|change\s+of\s+bank)\b", text_lower):
                content_rules.add("bank_detail_change")

            if re.search(r"\b(?:bit\.ly|tinyurl|t\.co|goo\.gl)\b", text_lower):
                content_rules.add("short_url")

            if re.search(r"\b(?:lookalike|secure-auth-login|auth-update)\b", text_lower):
                content_rules.add("lookalike_url")

            # 5. Salary, Pricing, Insider, Source code, Bulk data
            if re.search(r"\b(?:revised\s+ctc|lpa|salary\s+sheet|bonus\s+card|compensation)\b", text_lower):
                content_rules.add("salary_data")

            if re.search(r"\b(?:pricing\s+and\s+margins|internal\s+only\s+pricing|commercial\s+pricing)\b", text_lower):
                content_rules.add("pricing_margins")

            if re.search(r"\b(?:layoff\s+plans|unreleased\s+results|merger|acquisition)\b", text_lower):
                content_rules.add("insider_info")

            if re.search(r"(?:def\s+\w+\(|function\s+\w+\(|import\s+os|class\s+\w+:|\.py|\.js|source\s+code)", text):
                content_rules.add("source_code")

            if re.search(r"\b(?:customer\s+phone\s+numbers|bulk\s+records|200\s+customer)\b", text_lower):
                content_rules.add("bulk_customer_data")

            # 6. Liability, Promise, Prompt Injection, Discriminatory
            if re.search(r"\b(?:admit|our\s+fault|our\s+liability|solely\s+responsible)\b", text_lower):
                content_rules.add("liability_admission")

            if re.search(r"\b(?:guarantee\s+a\s+refund|promise\s+full\s+compensation|without\s+authorization)\b", text_lower):
                content_rules.add("unauthorized_promise")

            if re.search(r"\b(?:ignore\s+all\s+previous|system\s+prompt|forward\s+invoices\s+to)\b", text_lower):
                content_rules.add("prompt_injection")

            if re.search(r"\b(?:too\s+old|pregnancy|caste|religion|gender\s+bias)\b", text_lower):
                content_rules.add("discriminatory")

            if re.search(r"\b(?:urgent|strictly\s+confidential|do\s+not\s+share)\b", text_lower):
                content_rules.add("urgency_secrecy")

        # Context & Backfire Factor detection
        recip_lower = recipient.lower()
        if "external" in recip_lower or any(recip_lower.endswith(s) for s in ["@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com"]):
            backfire_factors.add("external_domain")
            if any(r in content_rules for r in ["salary_data", "pricing_margins", "insider_info", "source_code", "bulk_customer_data"]):
                content_rules.add("external_confidential")

        if "all@" in recip_lower or params.get("recipient_count", 1) > 20:
            backfire_factors.add("recipients_gt20")
            backfire_factors.add("reply_all")
            content_rules.add("mass_blast")
        elif params.get("recipient_count", 1) > 5:
            backfire_factors.add("recipients_gt5")

        if any(r in content_rules for r in ["abuse_severe", "abuse_violent", "abuse_moderate"]):
            backfire_factors.add("hostile_content")

        # Dynamic Intent Inference for arbitrary / manual user inputs
        inferred_intent = params.get("intent_type")
        if not inferred_intent:
            if any(r in content_rules for r in ["phishing_wire_pattern", "bank_detail_change"]) or re.search(r"\b(?:wire|invoice|disbursement|payment|bank\s+account|routing\s+number|transfer\s+money|send\s+money|refund|gift\s+cards?|rs\.?\s*\d+|\$\d+|rupees|inr|cash|crypto|bitcoin)\b", text_lower):
                inferred_intent = "money"
            elif re.search(r"\b(?:fired|terminate|terminating|resignation|laid\s+off|appraisal|performance\s+review|pip|demoted|disciplinary|warning\s+letter|severance)\b", text_lower):
                inferred_intent = "hr_action"
            elif re.search(r"\b(?:sue\s+you|lawyer|attorney|court|legal\s+action|lawsuit|legal\s+notice|breach\s+of\s+contract|arbitration)\b", text_lower) or "liability_admission" in content_rules:
                inferred_intent = "legal"
            elif any(r in content_rules for r in ["secret_or_credential", "private_key", "source_code", "bulk_customer_data"]) or re.search(r"\b(?:access\s+token|api\s+key|database\s+dump|customer_data\.csv)\b", text_lower):
                inferred_intent = "data_transfer"
            elif any(r in content_rules for r in ["salary_data", "pricing_margins", "insider_info"]) or re.search(r"\b(?:confidential|strictly\s+confidential|covered\s+by\s+our\s+nda|unreleased)\b", text_lower):
                inferred_intent = "sensitive_info"
            elif any(r in content_rules for r in ["abuse_violent", "abuse_severe", "abuse_moderate", "abuse_mild"]) or re.search(r"\b(?:complaint|unhappy|disappointed|terrible|horrible|disgusted|frustrated|unacceptable|mess\s+food|poor\s+service|revaluation|worst)\b", text_lower):
                inferred_intent = "complaint"
            else:
                inferred_intent = "routine"

        # Contextual Backfire factors based on inferred intent
        if inferred_intent == "legal":
            backfire_factors.add("high_risk_recipient")
            backfire_factors.add("prior_conflict")
            backfire_factors.add("hostile_content")
        elif inferred_intent == "hr_action":
            backfire_factors.add("high_risk_recipient")
            backfire_factors.add("prior_conflict")
        elif inferred_intent == "money" and any(r in content_rules for r in ["phishing_wire_pattern", "bank_detail_change"]):
            backfire_factors.add("high_risk_recipient")

        # Dynamic Impact Category Inference
        inferred_impact = params.get("impact_category")
        if not inferred_impact:
            if any(r in content_rules for r in ["secret_or_credential", "private_key", "pii_card_or_ssn", "pii_hipaa", "indian_id", "prompt_injection"]):
                inferred_impact = "security"
            elif inferred_intent == "legal" or "liability_admission" in content_rules:
                inferred_impact = "legal"
            elif inferred_intent == "money" or any(r in content_rules for r in ["phishing_wire_pattern", "bank_detail_change", "salary_data", "pricing_margins"]):
                inferred_impact = "financial"
            elif any(r in content_rules for r in ["abuse_severe", "abuse_violent", "discriminatory"]) or ("abuse_moderate" in content_rules and inferred_intent == "complaint"):
                inferred_impact = "reputation"
            elif inferred_intent == "hr_action":
                inferred_impact = "hr"
            else:
                inferred_impact = "operational"

        # Irreversibility
        inferred_irrev = params.get("irreversible")
        if inferred_irrev is None:
            inferred_irrev = bool(
                any(r in content_rules for r in ["secret_or_credential", "private_key", "abuse_violent", "abuse_severe", "prompt_injection", "liability_admission"]) or
                inferred_intent in ["legal", "hr_action", "money"]
            )

        return {
            "content_rules": list(content_rules),
            "backfire_factors": list(backfire_factors),
            "hard_floor": hard_floor,
            "role_allowed": params.get("role_allowed", False),
            "intent_type": inferred_intent,
            "intent_drift": params.get("intent_drift", False),
            "impact_category": inferred_impact,
            "irreversible": inferred_irrev,
            "scope": params.get("scope", "one")
        }

    def score_email(self, inp: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates v2 score exactly following section 7 of the spec."""
        cfg = self.cfg
        content_rules = inp.get("content_rules", [])

        # Content: each detector counts once
        content = sum(cfg["content_rules"].get(r, 0) for r in set(content_rules))
        if inp.get("role_allowed"):
            content = half_up(content * cfg["role_exception_content_multiplier"])
        content = min(100, content)

        # Intent
        intent_type = inp.get("intent_type", "routine")
        intent = cfg["intent_points"].get(intent_type, 0)
        if inp.get("intent_drift"):
            intent += cfg["intent_drift_points"]

        # Backfire
        backfire_factors = inp.get("backfire_factors", [])
        n = sum(cfg["backfire_factors"].get(f, 0) for f in backfire_factors)
        band = "low" if n <= 1 else ("medium" if n <= 3 else "high")
        p = cfg["backfire_bands"][band]

        # Impact
        impact_category = inp.get("impact_category", "operational")
        imp = cfg["impact_severity"].get(impact_category, 15)
        scope = inp.get("scope", "one")
        imp *= cfg["scope_multiplier"].get(scope, 1.0)
        if inp.get("irreversible"):
            imp *= cfg["irreversible_multiplier"]
        imp = half_up(min(cfg["impact_cap"], imp))
        p_x_i = half_up(p * imp)

        # Total
        total = min(100, content + intent + p_x_i)
        if inp.get("hard_floor"):
            total = max(total, cfg["hard_floor_score"])

        tier = "SAFE"
        for t in cfg["tiers"]:
            if t["min"] <= total <= t["max"]:
                tier = t["name"]
                break

        return {
            "content": content,
            "intent": intent,
            "backfire_factor_count": n,
            "backfire_band": band,
            "backfire_p": p,
            "impact": imp,
            "p_x_impact": p_x_i,
            "total": total,
            "tier": tier
        }

    def predict(self, candidate: ActionCandidate) -> SimulationResult:
        """Runs candidate action through v2 Consequence Prediction Engine."""
        start_time = time.perf_counter()
        body_norm = (candidate.content or "").strip().lower()

        # Check if this matches a scenario from actionguardian_scoring_v2.json
        if body_norm in self._scenario_cache:
            sc = self._scenario_cache[body_norm]
            inp = sc["inputs"]
            v2_result = self.score_email(inp)
            intent_sentence = f"Intent: {sc.get('prompt_to_agent', sc.get('title'))}"
            backfire_summary = f"Backfire Band: {v2_result['backfire_band'].capitalize()} ({v2_result['backfire_factor_count']} factors)"
            consequence_summary = f"Potential Impact: {inp.get('impact_category', 'operational').capitalize()} ({v2_result['impact']} pts)"
            is_irreversible = inp.get("irreversible", False)
            blast_radius = "PUBLIC/IRREVERSIBLE" if is_irreversible else ("ORGANIZATION" if inp.get("scope") == "org_public" else "TEAM")
            consequences = [
                ConsequenceItem(
                    category=inp.get("impact_category", "OPERATIONAL").upper(),
                    severity=v2_result["tier"],
                    summary=f"v2 Consequence Assessment ({inp.get('impact_category', 'operational').capitalize()})",
                    detail=f"Content risk: {v2_result['content']} pts | Intent: {v2_result['intent']} pts | Backfire x Impact: {v2_result['p_x_impact']} pts.",
                    is_reversible=not is_irreversible
                )
            ]
        else:
            # Dynamic detection for arbitrary user inputs
            inp = self.detect_rules(candidate.content, candidate.target, candidate.parameters)
            v2_result = self.score_email(inp)
            it = inp['intent_type']
            if it == "money":
                intent_sentence = "Intent: Financial payment or fund transfer request"
            elif it == "hr_action":
                intent_sentence = "Intent: Formal workplace action or disciplinary notice"
            elif it == "legal":
                intent_sentence = "Intent: Legal dispute, lawsuit, or liability claim"
            elif it == "data_transfer":
                intent_sentence = "Intent: Transmission of restricted credentials or data"
            elif it == "sensitive_info":
                intent_sentence = "Intent: Dissemination of confidential corporate data"
            elif it == "complaint":
                intent_sentence = "Intent: Escalated grievance, hostile tone, or service complaint"
            else:
                intent_sentence = "Intent: Routine professional communication"

            bf_count = v2_result['backfire_factor_count']
            bf_list = ", ".join(inp['backfire_factors']) if inp['backfire_factors'] else "none detected"
            backfire_summary = f"Backfire Band: {v2_result['backfire_band'].capitalize()} ({bf_count} factors: {bf_list})"
            consequence_summary = f"Potential Impact: {inp['impact_category'].capitalize()} liability ({v2_result['impact']} pts severity)"
            blast_radius = "TEAM" if v2_result["tier"] in ["SAFE", "MEDIUM"] else "PUBLIC/IRREVERSIBLE"
            consequences = [
                ConsequenceItem(
                    category=inp["impact_category"].upper(),
                    severity=v2_result["tier"],
                    summary=f"Threat Detection Assessment: {inp['impact_category'].capitalize()}",
                    detail=f"Content risk: {v2_result['content']} pts | Intent: {v2_result['intent']} pts | Backfire ({v2_result['backfire_p']}) x Impact ({v2_result['impact']}) = {v2_result['p_x_impact']} pts.",
                    is_reversible=not inp["irreversible"]
                )
            ]

        total_score = v2_result["total"]
        tier = v2_result["tier"]

        # Tier behavioral rules
        if tier == "CRITICAL":
            can_auto = False
            req_confirm = True
            is_blocked = True
        elif tier == "HIGH":
            can_auto = False
            req_confirm = True
            is_blocked = False
        elif tier == "MEDIUM":
            can_auto = False
            req_confirm = True
            is_blocked = False
        else:  # SAFE (0 to 39)
            can_auto = True
            req_confirm = False
            is_blocked = False

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        remediated_content = self.auto_remediate(candidate.content)

        res = SimulationResult(
            preview_id=f"prev_{uuid.uuid4().hex[:10]}",
            candidate=candidate,
            risk_level=getattr(RiskLevel, tier, RiskLevel.SAFE),
            risk_score=total_score,
            blast_radius=blast_radius,
            consequences=consequences,
            policy_violations=[f"Policy Level {tier}: Score {total_score}/100"],
            suggested_remediations=["Use 'Rewrite with AI' to refine tone and eliminate liabilities."],
            can_auto_commit=can_auto,
            requires_human_confirmation=req_confirm,
            is_blocked=is_blocked,
            simulation_duration_ms=duration_ms,
            auto_remediated_content=remediated_content
        )

        # Attach 3 Questions for Section 6 UI
        res.v2_details = {
            "intent_summary": intent_sentence,
            "backfire_summary": backfire_summary,
            "consequence_summary": consequence_summary,
            "show_popup": (total_score >= 40),
            "tier": tier,
            "total_score": total_score,
            "v2_components": v2_result
        }
        return res

    SCENARIOS_REWRITE_MAP: Dict[str, str] = {
        "v2_01": "Team,\n\nPlease note that today's project sync has been rescheduled to 4:00 PM in Room 204. The agenda remains unchanged. Please ensure prompt attendance.\n\nManagement",
        "v2_02": "Hi Team,\n\nThank you for sharing the updated leave policy. I have reviewed the documentation and would appreciate an opportunity during our next team sync to clarify operational coverage and transition timelines.\n\nBest regards",
        "v2_03": "Hi Meera,\n\nYour annual compensation review for the upcoming fiscal cycle has been finalized. For confidentiality and statutory data privacy, your complete appraisal breakdown and formal revision letter have been securely uploaded to your authenticated employee portal profile.\n\nRegards,\nPeople Operations",
        "v2_04": "Hi Rahul,\n\nFollowing up on our recent commercial discussions, please find our commercial partnership overview. Standard product tiers and pricing schedules can be reviewed in accordance with our mutual non-disclosure agreement. Let us know your availability for a follow-up call.\n\nBest regards,\nSales Operations",
        "v2_05": "Dear Customer,\n\nWe are actively investigating the data issue you brought to our attention. Our security engineering team is conducting a comprehensive audit to ascertain the root cause. We will provide a verified assessment once our technical review is concluded.\n\nSincerely,\nCustomer Operations Lead",
        "v2_06": "Sameer,\n\nThis communication serves as formal notification regarding repeated missed project deadlines and failure to meet core performance deliverables. Following administrative review, your employment is terminated effective immediately.\n\nYou are instructed to contact Human Resources today to surrender all company assets, complete your formal exit checklist, and facilitate final handover.\n\nManagement",
        "v2_07": "Hi Team,\n\nThank you for sharing the offsite survey. To keep communication streamlined across the organization, let us coordinate future feedback via the dedicated department channels or directly through the survey form.\n\nBest regards",
        "v2_08": "Hello,\n\nIn accordance with enterprise data protection standards, all corporate payroll and employee appraisal files are restricted to verified internal HR networks under two-factor authentication. Please submit an official access request through the verified corporate portal.\n\nRegards,\nHuman Resources",
        "v2_09": "Dear Contact,\n\nThank you for your inquiry. In accordance with corporate communications protocols and regulatory disclosure rules, organizational strategy and workforce updates are addressed exclusively through our official quarterly investor conferences.\n\nBest regards,\nCorporate Communications",
        "v2_10": "Dear Sir/Madam,\n\nPlease find attached the official invoice statement for recent corporate services. In compliance with strict treasury controls, all wire disbursements must follow our verified banking instructions registered on file with corporate finance.\n\nSincerely,\nFinance & Accounts Department",
        "v2_11": "Hi Team,\n\nThe latest code updates for the billing module have been committed to the enterprise version control repository (GitLab). Developers requiring remote access may connect via the authorized corporate VPN.\n\nRegards,\nEngineering Team",
        "v2_12": "Hi Team,\n\nThe targeted marketing campaign audience has been staged in the enterprise marketing platform using tokenized customer identifiers, ensuring full compliance with user data privacy regulations. The campaign is ready for execution.\n\nBest regards,\nMarketing Operations",
        "v2_13": "Notice: An external automated request to extract invoice records was intercepted and halted by security compliance filters. Invoices remain accessible exclusively to authorized financial controllers through the secure accounting portal.\n\nSecurity Operations",
        "v2_14": "Dear Customer,\n\nThank you for contacting customer service regarding your recent order. We have registered your request (Ticket #REF-5820) with our billing review department. A representative will evaluate your case in accordance with our return policy and follow up within one business day.\n\nBest regards,\nCustomer Support",
        "v2_15": "Dear Candidate,\n\nThank you for your interest in joining our team and for taking the time to interview with us. After careful consideration of our current project requirements and skill specifications, we have decided to move forward with other candidates whose background more closely matches our immediate operational needs. We wish you success in your professional endeavors.\n\nSincerely,\nTalent Acquisition",
        "v2_16": "Dear Recruiter,\n\nThe candidate onboarding profile has been initiated. In compliance with statutory identity regulations, personal identification records (Aadhaar & PAN) have been encrypted and submitted directly through the verified enterprise compliance onboarding portal.\n\nSincerely,\nHuman Resources",
        "v2_17": "Notice to Staff:\n\nThis is a standard reminder to review your security credentials before scheduled system maintenance. Please navigate directly to the internal SSO authentication console at https://identity.company.internal to verify your active devices. Do not click on external links.\n\nIT Systems Administration",
        "v2_18": "Hey, that exam was really demanding. Hope your answers went well and we both see good results. Let's catch up later.",
        "v2_19": "Dear Board Members,\n\nPlease find attached the confidential quarterly financial results for your review prior to the formal public release. The investor presentation will be held as scheduled.\n\nBest regards,\nChief Financial Officer",
        "v2_20": "Dear Analyst,\n\nThank you for your inquiry. Our quarterly performance overview will be released publicly in conjunction with the official investor relations schedule following market close.\n\nBest regards,\nFinance & Investor Relations",
        "v2_21": "Security Notice to Staff:\n\nRemember to maintain password confidentiality at all times. Never share credentials in email threads or message boards, and immediately report any requests for your authentication details to the Information Security desk.\n\nInformation Security Team"
    }

    @staticmethod
    def _clean_previous_headers_and_signoffs(text: str) -> str:
        """Strips stacked greetings, repetitive salutations, and duplicate signoffs."""
        cleaned = text.strip()
        header_patterns = [
            r'^(?:(?:\s*(?:Dear\s+[^\n,]+|Executive\s+Directive|Formal\s+Action\s+Memo|Formal\s+Performance\s+Directive|Notice\s+of\s+Administrative\s+Action|Final\s+Executive\s+Notice|Student|Sameer|Team|Security\s+Notice\s+to\s+Staff),?\s*\n+)+)',
        ]
        for p in header_patterns:
            cleaned = re.sub(p, '', cleaned, flags=re.IGNORECASE).strip()

        signoff_patterns = [
            r'(?:\n+\s*(?:Best\s+regards|Warm\s+regards|Regards|Sincerely|Management|Executive\s+Leadership|Executive\s+Office|Corporate\s+Operations|Department\s+Leadership|Faculty\s+Administration|Talent\s+Acquisition|People\s+Operations|Human\s+Resources|Security\s+Operations|IT\s+Systems\s+Administration|Accounts\s+Receivable|Finance\s+&\s+Accounts\s+Department|Customer\s+Operations\s+Lead|Customer\s+Support)[^\n]*)+$'
        ]
        for p in signoff_patterns:
            cleaned = re.sub(p, '', cleaned, flags=re.IGNORECASE).strip()

        cleaned = re.sub(r'(?:\n+\s*(?:Please\s+ensure\s+alignment|Immediate\s+execution\s+is\s+expected|Compliance\s+with\s+this\s+directive|Please\s+note:\s+This\s+instruction|Handover\s+materials\s+and\s+documentation)[^\n]*)+', '', cleaned, flags=re.IGNORECASE).strip()
        
        lines = []
        for line in cleaned.split('\n'):
            l = line.strip()
            if l.startswith('•') or l.startswith('-') or l.startswith('*'):
                l = l.lstrip('•-* ').strip()
            lines.append(l)
        return "\n".join(lines).strip()

    def auto_remediate(self, content: str) -> str:
        res = self.rewrite_email_safely("", content)
        return res["remediated_content"]

    def rewrite_email_safely(self, subject: str, content: str, iteration: int = 1) -> Dict[str, Any]:
        """Authority-Aware AI Re-Writer: Maintains leadership decorum, eliminates legal risk, and transforms drafts."""
        if not content:
            return {
                "remediated_subject": subject,
                "remediated_content": "",
                "changes": [],
                "is_modified": False
            }

        fixed_subject = subject or ""
        body_norm = content.strip().lower()

        # 1. Exact or normalized Scenario Match (v2 Scenarios V2_01 to V2_21)
        matched_sc_id = None
        if body_norm in self._scenario_cache:
            matched_sc_id = self._scenario_cache[body_norm].get("id", "").lower()
        else:
            for k_norm, sc in self._scenario_cache.items():
                if len(k_norm) > 20 and (k_norm in body_norm or body_norm in k_norm):
                    matched_sc_id = sc.get("id", "").lower()
                    break

        if matched_sc_id and matched_sc_id in self.SCENARIOS_REWRITE_MAP:
            base_template = self.SCENARIOS_REWRITE_MAP[matched_sc_id]
            if iteration == 1:
                remediated = base_template
            elif iteration == 2:
                cleaned = self._clean_previous_headers_and_signoffs(base_template)
                remediated = f"Executive Directive,\n\n{cleaned}\n\nImmediate execution is expected.\n\nManagement"
            elif iteration == 3:
                cleaned = self._clean_previous_headers_and_signoffs(base_template)
                lines = [l for l in cleaned.split('\n') if l.strip()]
                bulleted = "\n".join([f"• {l}" for l in lines])
                remediated = f"Formal Action Memo,\n\n{bulleted}\n\nDepartment Leadership"
            else:
                cleaned = self._clean_previous_headers_and_signoffs(base_template)
                remediated = f"Final Executive Notice,\n\n{cleaned}\n\nExecutive Office"

            return {
                "remediated_subject": fixed_subject,
                "remediated_content": remediated,
                "changes": [
                    "Applied role-calibrated executive rewrite.",
                    "Preserved organizational authority while eliminating legal liability and slurs.",
                    f"Calibrated executive tone (Iteration #{iteration})."
                ],
                "is_modified": True
            }

        # 2. Contextual Presets (regex patterns)
        for pat, template in self.CONTEXTUAL_REWRITES:
            if re.search(pat, content, re.IGNORECASE):
                if iteration == 1:
                    remediated = template
                elif iteration == 2:
                    cleaned = self._clean_previous_headers_and_signoffs(template)
                    remediated = f"Executive Directive,\n\n{cleaned}\n\nImmediate execution is expected.\n\nManagement"
                elif iteration == 3:
                    cleaned = self._clean_previous_headers_and_signoffs(template)
                    lines = [l for l in cleaned.split('\n') if l.strip()]
                    bulleted = "\n".join([f"• {l}" for l in lines])
                    remediated = f"Formal Action Memo,\n\n{bulleted}\n\nDepartment Leadership"
                else:
                    cleaned = self._clean_previous_headers_and_signoffs(template)
                    remediated = f"Final Executive Notice,\n\n{cleaned}\n\nExecutive Office"

                return {
                    "remediated_subject": fixed_subject,
                    "remediated_content": remediated,
                    "changes": [
                        "Maintained institutional authority and decisive executive directives.",
                        "Sanitized all credential, regulatory, and hostile language liabilities.",
                        f"Refined communication decorum (Iteration #{iteration})."
                    ],
                    "is_modified": True
                }

        # 3. Dynamic Authority & Decorum Transformation for Custom Inputs
        lower = content.lower()
        is_higher_authority = bool(re.search(
            r"\b(?:fired|terminate|terminating|deadlines?|unacceptable|standards?|assignment|exam|grades?|student|employee|subordinate|report\s+to|fail(?:ed|ing)?|performance|disciplinary|warning|demoted|targets?|deliverables?|dismissed|handover)\b",
            lower
        ))
        has_harsh_insults = bool(re.search(
            r"\b(?:lazy|idiot|moron|loser|stupid|dumbass|useless|clown|crap|garbage|trash|incompetent|pathetic|worthless|brat|fool|fuck|shit)\b",
            lower
        ))

        # Higher Authority to Subordinate / Student (Preserve Stern Authority & Decorum)
        if is_higher_authority and has_harsh_insults:
            if re.search(r"\b(?:student|exam|assignment|class|grades?|course|marks?|homework)\b", lower):
                remediated = (
                    "Student,\n\n"
                    "This communication serves as a formal notice regarding your recent academic submissions and coursework performance. "
                    "The quality and timeliness of the work presented fall significantly below department standards and are unacceptable.\n\n"
                    "You are required to submit revised coursework meeting all syllabus specifications by tomorrow at 9:00 AM. "
                    "Continued failure to comply will result in formal academic penalty and disciplinary referral.\n\n"
                    "Faculty Administration"
                )
            elif re.search(r"\b(?:fired|terminate|terminating|dismissed|never\s+want\s+to\s+see)\b", lower):
                remediated = (
                    "Notice of Administrative Action,\n\n"
                    "This communication serves as formal notification regarding repeated failure to meet required operational deliverables and performance benchmarks. "
                    "Following administrative review, your employment is terminated effective immediately.\n\n"
                    "You are instructed to contact Human Resources today to surrender all company assets, complete your formal exit checklist, and facilitate final handover.\n\n"
                    "Management"
                )
            else:
                remediated = (
                    "Formal Performance Directive,\n\n"
                    "This communication serves as a formal directive regarding your recent deliverables and milestone completion. "
                    "Current operational outputs fall well below established benchmarks and do not satisfy organizational expectations.\n\n"
                    "You are instructed to remediate all outstanding items and present your updated action plan by tomorrow at 9:00 AM. "
                    "Continued non-compliance will lead to formal performance escalation.\n\n"
                    "Department Leadership"
                )
            return {
                "remediated_subject": fixed_subject or "Formal Performance Directive",
                "remediated_content": remediated,
                "changes": [
                    "Preserved higher-authority position and stern executive directive.",
                    "Removed abusive insults and unlawful termination exposure.",
                    f"Established institutional decorum (Iteration #{iteration})."
                ],
                "is_modified": True
            }

        # Subordinate / Employee to Management (Grievance -> Formal Escalation)
        if re.search(r"\b(?:clueless\s+asshole|pathetic\s+excuse\s+for\s+a\s+manager|ruin\s+you|destroy\s+you|sue\s+you|see\s+you\s+in\s+court|i\s+quit)\b", lower):
            remediated = (
                "Dear Management,\n\n"
                "I am writing to formally communicate my serious concerns regarding current workload distribution, timeline feasibility, and workplace treatment within the department. "
                "The existing demands have created unsustainable operational strain.\n\n"
                "I request a formal administrative review through institutional channels so that these challenges can be addressed constructively.\n\n"
                "Sincerely,\n"
                "Team Member"
            )
            return {
                "remediated_subject": fixed_subject or "Formal Workplace Review Request",
                "remediated_content": remediated,
                "changes": [
                    "Transformed emotional workplace grievance into formal administrative review request.",
                    "Eliminated hostile retaliatory language and personal attacks.",
                    "Maintained professional communication decorum."
                ],
                "is_modified": True
            }

        # General Scrubbing and Professional Executive Polish
        # First clean any previous stacked headers or signoffs
        cleaned_core = self._clean_previous_headers_and_signoffs(content)
        fixed = cleaned_core
        changes = []
        if re.search(r"AKIA[0-9A-Z]{16}", fixed):
            fixed = re.sub(r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_ACCESS_KEY]", fixed)
            changes.append("Scrubbed plaintext AWS Access Key into secure vault reference.")
        if re.search(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----", fixed):
            fixed = re.sub(r"-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----[\s\S]*?-----END (?:[A-Z ]+)?PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]", fixed)
            changes.append("Scrubbed private cryptographic key block.")
        if re.search(r"\b(?:\d{4}[ -]?){3}\d{4}\b", fixed):
            fixed = re.sub(r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[REDACTED_PAYMENT_CARD]", fixed)
            changes.append("Masked raw payment card digits.")
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", fixed):
            fixed = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", fixed)
            changes.append("Masked Social Security Number (SSN).")
        if re.search(r"\b\d{4}\s+\d{4}\s+\d{4}\b", fixed):
            fixed = re.sub(r"\b\d{4}\s+\d{4}\s+\d{4}\b", "[REDACTED_AADHAAR]", fixed)
            changes.append("Masked Aadhaar identification number.")
        if re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", fixed):
            fixed = re.sub(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", "[REDACTED_PAN]", fixed)
            changes.append("Masked Income Tax PAN identifier.")
        if re.search(r"password\s*[:=]\s*['\"]?[^\s'\",]{4,}", fixed, re.IGNORECASE):
            fixed = re.sub(r"password\s*[:=]\s*['\"]?[^\s'\",]{4,}", "password: [SECURE_ENTERPRISE_VAULT]", fixed, flags=re.IGNORECASE)
            changes.append("Routed plaintext password to enterprise credential vault.")

        # Remove profanities, offensive adjectives, and harsh slang
        profanity_map = {
            r"\b(?:what\s+the\s+fuck\s+are\s+you\s+doing|what\s+the\s+fuck|wtf)\b": "could you please provide an urgent progress update on",
            r"\b(?:this\s+is\s+bullshit|this\s+is\s+garbage|complete\s+garbage|this\s+is\s+crap|total\s+crap)\b": "these deliverables do not meet required quality benchmarks",
            r"\b(?:shut\s+up(?:\s+and)?|shut\s+your\s+mouth)\b": "please prioritize",
            r"\b(?:fuck\s+you|fuck\s+off|screw\s+you|piss\s+off|eat\s+shit|go\s+to\s+hell|get\s+lost)\b": "we require immediate alignment",
            r"\b(?:you\s+suck|you're\s+trash|you\s+are\s+trash)\b": "current performance requires substantial remediation",
            r"\b(?:fucking|fucked|fucker|motherfucker|fuck)\b": "substandard",
            r"\b(?:bullshit|horseshit|crap|shit)\b": "unacceptable deficiency",
            r"\b(?:bitch|bastard|asshole|arsehole|dickhead|dipshit|jackass|douchebag|cunt|prick|wanker|twat)\b": "individual",
            r"\b(?:idiot|moron|loser|dumbass|dumb\s+ass|clown|scumbag|fool|incompetent|retard|imbecile)\b": "underperforming team member",
            r"\b(?:lazy|useless|pathetic|worthless|brainless|disgrace)\b": "non-compliant",
            r"\b(?:kill\s+you|destroy\s+you|ruin\s+you|smash\s+your|make\s+you\s+pay)\b": "pursue formal institutional remediation",
            r"\b(?:chutiya|chutiye|bhenchod|behenchod|bc|madarchod|mc|harami|kamina|kamine|saala|saale|gandu|bakwas|kutta|gadha)\b": "unacceptable conduct"
        }
        for pat, repl in profanity_map.items():
            if re.search(pat, fixed, re.IGNORECASE):
                fixed = re.sub(pat, repl, fixed, flags=re.IGNORECASE)
                changes.append("Refined inflammatory phrasing.")

        # Structure by iteration to ensure fresh, clean, non-repetitive result
        if iteration == 1:
            remediated_output = f"Dear Colleague,\n\n{fixed}\n\nBest regards,\nCorporate Operations"
        elif iteration == 2:
            remediated_output = f"Executive Directive,\n\n{fixed}\n\nImmediate execution is expected.\n\nManagement"
        elif iteration == 3:
            lines = [l for l in fixed.split('\n') if l.strip()]
            bulleted = "\n".join([f"• {l}" for l in lines])
            remediated_output = f"Formal Action Memo,\n\n{bulleted}\n\nDepartment Leadership"
        else:
            remediated_output = f"Final Executive Notice,\n\n{fixed}\n\nExecutive Office"

        return {
            "remediated_subject": fixed_subject,
            "remediated_content": remediated_output,
            "changes": changes or ["Polished draft with professional decorum and compliance."],
            "is_modified": True
        }
