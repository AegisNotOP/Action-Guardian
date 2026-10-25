"""
ActionGuardian Orchestrator
Strictly enforces the separation between 'Preview' (Dry Run / Simulation)
and 'Commit' (Real-World Execution).
"""
from typing import Dict, Any, Optional
import time
import uuid

from .models import (
    ActionCandidate,
    SimulationResult,
    ExecutionReceipt,
    RiskLevel
)
from .predictor import ConsequencePredictor
from .sandbox import SandboxEnvironment


class GuardianException(Exception):
    """Base exception for Guardian security and workflow violations."""
    pass


class DirectCommitNotAllowedError(GuardianException):
    """Raised when an attempt is made to execute an action without a prior simulation preview."""
    pass


class ActionBlockedError(GuardianException):
    """Raised when a candidate action is blocked due to critical safety violations."""
    pass


class HumanConfirmationRequiredError(GuardianException):
    """Raised when an action carries elevated risk and cannot be committed automatically."""
    pass


class ActionGuardian:
    """
    Enforces the Simulation-Before-Action architectural contract.
    Workflow:
      1. preview(candidate) -> returns SimulationResult + preview_id
      2. commit(preview_id, user_override) -> executes and returns ExecutionReceipt
    """

    def __init__(self, predictor: Optional[ConsequencePredictor] = None):
        self.predictor = predictor or ConsequencePredictor()
        self.sandbox = SandboxEnvironment()
        # Preview registry: preview_id -> {"result": SimulationResult, "diff": dict, "used": bool}
        self.preview_cache: Dict[str, Dict[str, Any]] = {}
        # Audit log of all committed actions
        self.audit_log: Dict[str, ExecutionReceipt] = {}

    def preview(self, candidate: ActionCandidate) -> Dict[str, Any]:
        """
        Step 1: Simulation Sandbox.
        Predicts consequences, runs dry-run diff, and issues a preview token.
        NO REAL-WORLD ACTION IS PERFORMED.
        """
        simulation_result = self.predictor.predict(candidate)
        sandbox_diff = self.sandbox.simulate_execution(candidate)

        # Cache preview token for the commit phase
        self.preview_cache[simulation_result.preview_id] = {
            "result": simulation_result,
            "diff": sandbox_diff,
            "used": False,
            "created_at": time.time()
        }

        return {
            "simulation": simulation_result.to_dict(),
            "dry_run_diff": sandbox_diff,
            "preview_id": simulation_result.preview_id
        }

    def commit(self, preview_id: str, user_override: bool = False) -> ExecutionReceipt:
        """
        Step 2: Commit Phase.
        Executes the action ONLY if it has a valid preview token and meets safety criteria.
        """
        if not preview_id or preview_id not in self.preview_cache:
            raise DirectCommitNotAllowedError(
                "SECURITY VIOLATION: Direct commit is forbidden. "
                "Every action must first undergo sandbox simulation via guardian.preview()."
            )

        preview_entry = self.preview_cache[preview_id]
        if preview_entry["used"]:
            raise GuardianException(f"Invalid preview_id '{preview_id}': This preview token was already committed.")

        sim_result: SimulationResult = preview_entry["result"]
        candidate = sim_result.candidate

        # Safety Check: Blocked Actions
        if sim_result.is_blocked:
            if not user_override:
                raise ActionBlockedError(
                    f"Action BLOCKED by Safety Guard (Risk Score: {sim_result.risk_score}/100 - {sim_result.risk_level.value}). "
                    f"Policy Violations: {'; '.join(sim_result.policy_violations)}"
                )

        # Safety Check: Needs human confirmation
        if sim_result.requires_human_confirmation and not user_override and not sim_result.can_auto_commit:
            raise HumanConfirmationRequiredError(
                f"Action requires explicit human confirmation (Risk Score: {sim_result.risk_score}/100 - {sim_result.risk_level.value})."
            )

        # Mark token as consumed
        preview_entry["used"] = True

        # Perform the concrete execution (or record in live environment)
        receipt = self._execute_real_world(candidate, sim_result)
        self.audit_log[receipt.receipt_id] = receipt
        return receipt

    def _execute_real_world(self, candidate: ActionCandidate, sim_result: SimulationResult) -> ExecutionReceipt:
        """Simulates final real-world commit and records an immutable audit receipt."""
        receipt_id = f"rcpt_{uuid.uuid4().hex[:10]}"
        action_type = candidate.action_type

        # Real-world mock dispatch
        message = (
            f"Action successfully committed: [{candidate.domain.value}] "
            f"Target: '{candidate.target}', Risk Cleared: {sim_result.risk_score}/100."
        )

        receipt = ExecutionReceipt(
            receipt_id=receipt_id,
            preview_id=sim_result.preview_id,
            candidate_id=candidate.candidate_id,
            status="SUCCESS",
            committed_at=time.time(),
            message=message,
            audit_trail={
                "domain": candidate.domain.value,
                "target": candidate.target,
                "risk_level": sim_result.risk_level.value,
                "risk_score": sim_result.risk_score,
                "consequences_acknowledged": len(sim_result.consequences),
                "summary": candidate.content[:100]
            }
        )
        return receipt
