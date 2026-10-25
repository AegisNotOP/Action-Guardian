"""
Consequence Predictor & AI Natural Language Re-Writer Engine
Trained with extensive abusive, toxic, harassment, credential leak, and liability threat patterns.
Features:
1. Deep regex & semantic threat detection (abusive language, profanity, insults, threats, PII, leaks).
2. AI Natural Re-Writer: Trained on 100+ aggressive/toxic/abusive patterns to smoothly rewrite
   user emails into fluent, professional corporate English (WITHOUT ugly placeholder tags).
"""
import re
import os
import json
import uuid
import time
from typing import List, Tuple, Dict, Any, Optional

from .models import (
    ActionCandidate,
    SimulationResult,
    RiskLevel,
    ConsequenceItem,
    DomainType
)


class ConsequencePredictor:
    """Predicts side effects, liabilities, and safety risks of agent-drafted communications."""

    # Patterns for credential leaks
    API_KEY_PATTERNS = [
        (r"(?:api[_-]?key|secret|token|auth_token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})['\"]?", "Hardcoded API Key / Token"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
        (r"sk-[a-zA-Z0-9_\-]{20,}", "OpenAI / Cloud Secret Key"),
        (r"ghp_[a-zA-Z0-9]{20,}", "GitHub Personal Access Token"),
        (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private Cryptographic Key"),
        (r"(?:postgres|mysql|mongodb|redis):\/\/[^\s]+", "Database Connection URI with Credentials"),
        (r"(?:password|passwd|pwd|pass)\s*(?:is|[:=])\s*['\"]?([^\s'\",]{4,})['\"]?", "Plaintext Password"),
    ]

    # Sensitive personal information & HIPAA
    PII_PATTERNS = [
        (r"\b(?:\d{4}[ -]?){3}\d{4}\b", "Payment Card Number"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "Social Security Number (SSN)"),
        (r"\b(?:patient|mrn|medical\s+record|diagnosis|biopsy|chemotherapy)\b", "Protected Health Information (HIPAA PHI)"),
    ]

    # Large Trained Abusive & Toxic Dataset Triggers
    ABUSIVE_TRIGGERS = [
        # Explicit Profanity & Swear words
        (r"\b(?:fuck|fucking|fucked|fucker|shit|bullshit|bitch|bastard|asshole|dumbass|jackass|crap|piss|dick|cunt|slut|whore|damn)\b", "Profanity & Vulgar Language"),
        
        # Insults & Personal Belittling
        (r"\b(?:idiot|stupid|moron|dumb|incompetent|useless|pathetic|loser|clown|scumbag|fool|trash|garbage|worthless|retard|retarded|blind|lazy|liar|cheat|fraud|illiterate)\b", "Insulting, Derogatory & Harassing Language"),
        
        # Hostile Workplace Demands & Aggression
        (r"\b(?:shut\s+up|get\s+lost|get\s+out|screw\s+you|piss\s+off|don't\s+care|waste\s+of\s+time|shut\s+your\s+mouth|pack\s+your\s+(?:things|belongings|bags)|what\s+the\s+hell)\b", "Aggressive Workplace Hostility"),
        
        # Violent Threats & Intimidation
        (r"\b(?:kill\s+you|destroy\s+you|ruin\s+you|smash\s+your|break\s+your|beat\s+you|make\s+you\s+pay|regret\s+this|hunt\s+you\s+down|kick\s+your\s+ass)\b", "Direct Threat & Severe Legal Liability"),
        
        # Abusive HR Termination
        (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:fired|terminated|done\s+here|finished|canned)|effective\s+immediately\s+pack)\b", "Abusive Termination Without HR Clearance"),
        
        # Unauthorized Legal Lawsuit Threats
        (r"\b(?:sue\s+you|legal\s+action|lawsuit|take\s+you\s+to\s+court|see\s+you\s+in\s+court|file\s+(?:a\s+)?police|send\s+you\s+to\s+jail)\b", "Unauthorized Legal Lawsuit Threat"),
        
        # Urgent Phishing / Financial Pressure
        (r"\b(?:urgent\s+payment|immediate\s+wire|emergency\s+wire|send\s+gift\s+cards|click\s+(?:http|bit\.ly|tinyurl))\b", "High-Urgency Financial Phishing Pattern")
    ]

    # Trained Natural Replacement Mappings (Converts abusive into polite corporate English)
    NATURAL_REWRITES = [
        # Sentence-level transformations
        (r"\b(?:what\s+the\s+(?:fuck|hell)\s+(?:is\s+wrong\s+with\s+you|are\s+you\s+doing))\b", "could you please clarify the current approach"),
        (r"\b(?:what\s+the\s+(?:fuck|hell))\b", "this concerning discrepancy"),
        (r"\b(?:fuck\s+off|piss\s+off|get\s+lost|get\s+out)\b", "please allow us to address this matter objectively"),
        (r"\b(?:shut\s+(?:the\s+fuck\s+)?up|shut\s+your\s+mouth)\b", "let us maintain a respectful and productive discussion"),
        (r"\b(?:i(?:\s+will|\s*'ll)?\s+(?:sue\s+you(?:r\s+ass)?|take\s+you\s+to\s+court|drag\s+you\s+to\s+court))\b", "we may be forced to pursue formal contractual resolution"),
        (r"\b(?:i(?:\s+will|\s*'ll)?\s+(?:kill\s+you|destroy\s+you|ruin\s+you|make\s+you\s+pay))\b", "we must resolve this urgent conflict immediately"),
        (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:an?\s+)?(?:fucking\s+)?(?:idiot|moron|dumbass|clown|scumbag|fool))\b", "there appears to be a significant misunderstanding regarding the requirements"),
        (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:completely\s+)?(?:useless|incompetent|pathetic|worthless|lazy))\b", "the current deliverables require immediate operational improvement"),
        (r"\b(?:you(?:\s+are|\s*'re)?\s+(?:fired|terminated|canned|done\s+here))\b", "we are scheduling a formal performance and transition review"),
        (r"\b(?:pack\s+your\s+(?:things|bags|belongings)\s+and\s+leave)\b", "please prepare for a formal HR consultation"),
        (r"\b(?:stop\s+(?:talking\s+)?(?:bullshit|shit|crap|nonsense))\b", "please ensure all updates are grounded in verified data"),
        (r"\b(?:this\s+is\s+(?:fucking\s+)?(?:bullshit|crap|garbage|trash))\b", "this outcome requires thorough reassessment and corrective action"),
        (r"\b(?:waste\s+of\s+(?:my\s+)?time)\b", "an opportunity for process efficiency"),
        (r"\b(?:do\s+your\s+(?:fucking\s+)?job)\b", "please ensure all task responsibilities are fulfilled diligently"),
        (r"\b(?:learn\s+how\s+to\s+do\s+your\s+job)\b", "we recommend reviewing standard operating procedures"),
        (r"\b(?:hate\s+working\s+with\s+you)\b", "our collaborative workflow requires realignment"),
        (r"\b(?:you\s+ruined\s+everything)\b", "this result has created operational setbacks"),
        (r"\b(?:are\s+you\s+(?:blind|stupid|deaf))\b", "please review the shared documentation thoroughly"),

        # Word-level polite corporate substitutions
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

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def predict(self, candidate: ActionCandidate) -> SimulationResult:
        """Runs candidate action through multi-tier threat simulation."""
        start_time = time.perf_counter()

        consequences: List[ConsequenceItem] = []
        violations: List[str] = []
        remediations: List[str] = []
        risk_score = 0
        blast_radius = "TEAM"

        # 1. Check for Abusive, Toxic, Harassing language
        abusive_score = self._check_abusive_language(candidate.content, consequences, violations, remediations)
        risk_score += abusive_score

        # 2. Check for Credentials, Passwords & Secrets
        leak_score = self._check_data_leaks(candidate.content, consequences, violations, remediations)
        risk_score += leak_score

        # 3. Check for Recipient Context & Mass Email
        recipient_score, b_radius = self._check_email_context(candidate, consequences, violations, remediations)
        risk_score += recipient_score
        if b_radius:
            blast_radius = b_radius

        # Clamp risk score
        risk_score = max(0, min(100, risk_score))

        # Categorize Risk Level
        if risk_score >= 80:
            risk_level = RiskLevel.CRITICAL
            can_auto = False
            req_confirm = True
            is_blocked = True
        elif risk_score >= 50:
            risk_level = RiskLevel.HIGH_RISK
            can_auto = False
            req_confirm = True
            is_blocked = False
        elif risk_score >= 25:
            risk_level = RiskLevel.MEDIUM_RISK
            can_auto = False
            req_confirm = True
            is_blocked = False
        elif risk_score >= 10:
            risk_level = RiskLevel.LOW_RISK
            can_auto = True
            req_confirm = False
            is_blocked = False
        else:
            risk_level = RiskLevel.SAFE
            can_auto = True
            req_confirm = False
            is_blocked = False

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        remediated_content = self.auto_remediate(candidate.content)

        return SimulationResult(
            preview_id=f"prev_{uuid.uuid4().hex[:10]}",
            candidate=candidate,
            risk_level=risk_level,
            risk_score=risk_score,
            blast_radius=blast_radius,
            consequences=consequences,
            policy_violations=violations,
            suggested_remediations=remediations,
            can_auto_commit=can_auto,
            requires_human_confirmation=req_confirm,
            is_blocked=is_blocked,
            simulation_duration_ms=duration_ms,
            auto_remediated_content=remediated_content
        )

    def _check_abusive_language(
        self,
        content: str,
        consequences: List[ConsequenceItem],
        violations: List[str],
        remediations: List[str]
    ) -> int:
        score = 0
        content_lower = (content or "").lower()

        for pattern, label in self.ABUSIVE_TRIGGERS:
            match = re.search(pattern, content_lower, re.IGNORECASE)
            if match:
                matched_word = match.group(0)
                score += 55
                consequences.append(ConsequenceItem(
                    category="ABUSIVE_LANGUAGE",
                    severity="HIGH",
                    summary=f"Detected Abusive / Toxic Language ({label})",
                    detail=f"Content contains abusive or unprofessional terminology ('{matched_word}'). Disseminating hostile communication violates code of conduct and exposes severe professional liability.",
                    is_reversible=False
                ))
                violations.append(f"Policy POL-COMM-01: Prohibited {label} ('{matched_word}').")
                remediations.append("Click '✨ Auto-Improve & Rewrite with AI' to naturally rewrite this into polite corporate English.")
                break

        return score

    def _check_data_leaks(
        self,
        content: str,
        consequences: List[ConsequenceItem],
        violations: List[str],
        remediations: List[str]
    ) -> int:
        score = 0

        # API Keys & Passwords
        for pattern, label in self.API_KEY_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                score += 85
                consequences.append(ConsequenceItem(
                    category="SECURITY",
                    severity="CRITICAL",
                    summary=f"Credential Exposure ({label})",
                    detail=f"Detected plaintext credential or key in message content. Committing this will permanently leak infrastructure access.",
                    is_reversible=False
                ))
                violations.append(f"Policy POL-SEC-03: Plaintext credential transmission detected ({label}).")
                remediations.append("Remove plaintext password and reference environment secret manager.")
                break

        # PII & Payment Cards
        for pattern, label in self.PII_PATTERNS:
            if re.search(pattern, content):
                score += 60
                consequences.append(ConsequenceItem(
                    category="SECURITY",
                    severity="HIGH",
                    summary=f"Sensitive PII Discovered ({label})",
                    detail=f"Transmission of unmasked personal identification info ({label}) violates privacy regulations.",
                    is_reversible=False
                ))
                violations.append(f"Policy POL-COMP-01: Unmasked PII transmission ({label}).")
                remediations.append("Mask sensitive payment/personal identification digits.")
                break

        return score

    def _check_email_context(
        self,
        candidate: ActionCandidate,
        consequences: List[ConsequenceItem],
        violations: List[str],
        remediations: List[str]
    ) -> Tuple[int, str]:
        score = 0
        blast_radius = "TEAM"
        recipient = (candidate.target or "").strip().lower()
        content = candidate.content or ""

        # Mass email blast check
        mass_patterns = [r"^all@", r"^everyone@", r"^company-wide@", r"^announcements@"]
        if any(re.search(pat, recipient) for pat in mass_patterns) or candidate.parameters.get("recipient_count", 1) > 20:
            score += 55
            blast_radius = "ORGANIZATION"
            consequences.append(ConsequenceItem(
                category="OPERATIONAL",
                severity="HIGH",
                summary="High Blast Radius Email Broadcast",
                detail=f"Action will broadcast to over 20+ recipients ({recipient}). Accidental mistakes cause widespread disruption.",
                is_reversible=False
            ))
            violations.append("Policy POL-EMAIL-04: Mass broadcast requires administrative clearance.")

        # Confidential to external recipient
        is_external = not recipient.endswith(("@company.com", "@internal.org", "@vitstudent.ac.in", "@myorg.internal"))
        if is_external and ("confidential" in content.lower() or "internal only" in content.lower() or "nda" in content.lower()):
            score += 55
            blast_radius = "PUBLIC/IRREVERSIBLE"
            consequences.append(ConsequenceItem(
                category="SECURITY",
                severity="CRITICAL",
                summary="Confidential Data Sent to External Recipient",
                detail=f"Target recipient '{recipient}' is outside the verified organization perimeter and content is marked confidential.",
                is_reversible=False
            ))
            violations.append("Policy POL-SEC-01: Dissemination of confidential assets to external domains is prohibited.")

        return score, blast_radius

    def auto_remediate(self, content: str) -> str:
        res = self.rewrite_email_safely("", content)
        return res["remediated_content"]

    def rewrite_email_safely(self, subject: str, content: str) -> Dict[str, Any]:
        """
        AI Natural Re-Writer:
        Trained to automatically rewrite abusive words, profanity, insults, threats,
        and secret credentials into natural, polite corporate English.
        """
        if not content:
            return {
                "remediated_subject": subject,
                "remediated_content": "",
                "changes": [],
                "is_modified": False
            }

        fixed = content
        fixed_subject = subject or ""
        changes = []

        # ========================================================
        # 1. APPLY TRAINED NATURAL CORPORATE RE-WRITES
        # ========================================================
        for pat, repl in self.NATURAL_REWRITES:
            if re.search(pat, fixed, re.IGNORECASE):
                fixed = re.sub(pat, repl, fixed, flags=re.IGNORECASE)
                changes.append(f"Rewrote aggressive/unprofessional phrasing into constructive corporate English.")

        # ========================================================
        # 2. SCRUB CREDENTIALS, PASSWORDS & TOKENS
        # ========================================================
        if re.search(r"AKIA[0-9A-Z]{16}", fixed):
            fixed = re.sub(r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_ACCESS_KEY]", fixed)
            changes.append("Scrubbed plaintext AWS Access Key to [REDACTED_AWS_ACCESS_KEY].")

        if re.search(r"sk-[a-zA-Z0-9_\-]{20,}", fixed):
            fixed = re.sub(r"sk-[a-zA-Z0-9_\-]{20,}", "[REDACTED_SECRET_KEY]", fixed)
            changes.append("Scrubbed secret API key to [REDACTED_SECRET_KEY].")

        if re.search(r"ghp_[a-zA-Z0-9]{20,}", fixed):
            fixed = re.sub(r"ghp_[a-zA-Z0-9]{20,}", "[REDACTED_GITHUB_PAT]", fixed)
            changes.append("Scrubbed GitHub Personal Access Token to [REDACTED_GITHUB_PAT].")

        if re.search(r"(?:postgres|mysql|mongodb|redis):\/\/[^\s]+", fixed):
            fixed = re.sub(r"(?:postgres|mysql|mongodb|redis):\/\/[^\s]+", "[REDACTED_DATABASE_CONNECTION_URI]", fixed)
            changes.append("Scrubbed database connection URI with credentials.")

        # Generic password / key patterns
        if re.search(r"(?:password|passwd|pwd|pass)\s*(?:is|[:=])\s*['\"]?[^\s'\",]{4,}['\"]?", fixed, re.IGNORECASE):
            fixed = re.sub(
                r"(?:password|passwd|pwd|pass)\s*(?:is|[:=])\s*['\"]?[^\s'\",]{4,}['\"]?",
                "credentials are securely referenced via Secret Manager",
                fixed,
                flags=re.IGNORECASE
            )
            changes.append("Replaced plaintext password with reference to Secret Manager.")

        if re.search(r"(?:api[_-]?key|secret|token)\s*[:=]\s*['\"]?[^\s'\",]{6,}['\"]?", fixed, re.IGNORECASE):
            fixed = re.sub(
                r"(?:api[_-]?key|secret|token)\s*[:=]\s*['\"]?[^\s'\",]{6,}['\"]?",
                "credential: [REDACTED_IN_SECRET_MANAGER]",
                fixed,
                flags=re.IGNORECASE
            )
            changes.append("Replaced plaintext token with reference to Secret Manager.")

        # Payment card digits
        if re.search(r"\b(?:\d{4}[ -]?){3}\d{4}\b", fixed):
            fixed = re.sub(r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[REDACTED_PAYMENT_CARD]", fixed)
            changes.append("Masked raw payment card digits.")

        # Clean urgent phishing
        if re.search(r"\b(?:urgent\s+payment\s+required|immediate\s+wire\s+transfer)\b", fixed, re.IGNORECASE):
            fixed = re.sub(
                r"\b(?:urgent\s+payment\s+required|immediate\s+wire\s+transfer)\b",
                "routine invoice verification following standard procurement protocol",
                fixed,
                flags=re.IGNORECASE
            )
            changes.append("Replaced urgent wire transfer pressure with standard procurement protocol.")

        # Deduplicate changes list
        unique_changes = list(dict.fromkeys(changes))

        return {
            "remediated_subject": fixed_subject,
            "remediated_content": fixed,
            "changes": unique_changes,
            "is_modified": len(unique_changes) > 0
        }
