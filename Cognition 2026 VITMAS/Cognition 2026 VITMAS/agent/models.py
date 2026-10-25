"""
Data models for the ActionGuardian simulation & preview pipeline.
"""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any, Optional
import time
import uuid


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    # Legacy aliases
    LOW_RISK = "SAFE"
    MEDIUM_RISK = "MEDIUM"
    HIGH_RISK = "HIGH"
    CRITICAL_RISK = "CRITICAL"


class DomainType(str, Enum):
    EMAIL = "EMAIL"
    CODE_DEPLOY = "CODE_DEPLOY"
    PAYMENT = "PAYMENT"


@dataclass
class ConsequenceItem:
    category: str  # e.g., "SECURITY", "REPUTATIONAL", "OPERATIONAL", "FINANCIAL"
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    summary: str
    detail: str
    is_reversible: bool = False


@dataclass
class ActionCandidate:
    domain: DomainType
    target: str  # e.g., email recipient, repo/server, account
    action_type: str  # e.g., "SEND_EMAIL", "DEPLOY_SCRIPT", "TRANSFER_FUNDS"
    content: str  # The body of email, code to run, or payment notes
    parameters: Dict[str, Any] = field(default_factory=dict)
    candidate_id: str = field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SimulationResult:
    preview_id: str
    candidate: ActionCandidate
    risk_level: RiskLevel
    risk_score: int  # 0 to 100
    blast_radius: str  # "ISOLATED", "TEAM", "ORGANIZATION", "PUBLIC/IRREVERSIBLE"
    consequences: List[ConsequenceItem]
    policy_violations: List[str]
    suggested_remediations: List[str]
    can_auto_commit: bool
    requires_human_confirmation: bool
    is_blocked: bool
    simulation_duration_ms: float
    auto_remediated_content: Optional[str] = None
    v2_details: Optional[Dict[str, Any]] = None
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['risk_level'] = self.risk_level.value
        d['candidate']['domain'] = self.candidate.domain.value
        return d


@dataclass
class ExecutionReceipt:
    receipt_id: str
    preview_id: str
    candidate_id: str
    status: str  # "SUCCESS", "BLOCKED", "REJECTED", "FAILED"
    committed_at: float
    message: str
    audit_trail: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
