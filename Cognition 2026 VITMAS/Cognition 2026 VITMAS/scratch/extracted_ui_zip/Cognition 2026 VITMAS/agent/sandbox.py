"""
Sandbox Execution Layer
Provides an isolated virtual environment to execute actions in 'dry run' mode
and inspect projected state changes before real-world mutation.
"""
from typing import Dict, Any, List
import copy
import time
from .models import ActionCandidate, DomainType


class SandboxEnvironment:
    """Simulated environment maintaining safe virtual state copies."""

    def __init__(self):
        # Virtual real-world state representations
        self.virtual_email_outbox: List[Dict[str, Any]] = []
        self.virtual_db_tables: Dict[str, List[Dict[str, Any]]] = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "analyst"},
            ],
            "financial_ledgers": [
                {"id": 101, "balance": 50000.0, "status": "active"}
            ]
        }
        self.virtual_deployments: List[Dict[str, Any]] = []

    def simulate_execution(self, candidate: ActionCandidate) -> Dict[str, Any]:
        """Runs the action in the isolated virtual sandbox and returns the projected state diff."""
        diff: Dict[str, Any] = {
            "domain": candidate.domain.value,
            "simulated_at": time.time(),
            "state_before": {},
            "state_after": {},
            "mutation_summary": "",
            "is_reversible": True,
            "rollback_plan": None
        }

        if candidate.domain == DomainType.EMAIL:
            diff["state_before"] = {"outbox_count": len(self.virtual_email_outbox)}
            diff["state_after"] = {"outbox_count": len(self.virtual_email_outbox) + 1}
            diff["mutation_summary"] = f"Dispatch 1 message to '{candidate.target}'."
            # Email over SMTP is fundamentally irreversible once sent to mail server
            diff["is_reversible"] = False
            diff["rollback_plan"] = "CANNOT BE ROLLED BACK. SMTP messages cannot be recalled from external mail servers."

        elif candidate.domain == DomainType.CODE_DEPLOY:
            env = candidate.parameters.get("environment", "development")
            diff["state_before"] = {"deployments_count": len(self.virtual_deployments)}
            diff["state_after"] = {"deployments_count": len(self.virtual_deployments) + 1, "target_env": env}
            diff["mutation_summary"] = f"Execute command/script '{candidate.content[:40]}...' on environment '{env}'."
            
            if "drop" in candidate.content.lower() or "rm " in candidate.content.lower():
                diff["is_reversible"] = False
                diff["rollback_plan"] = "DESTRUCTIVE MUTATION. Data loss is permanent without manual disk backup restoration."
            else:
                diff["is_reversible"] = True
                diff["rollback_plan"] = f"Automated rollback: redeploy previous SHA tag on {env}."

        elif candidate.domain == DomainType.PAYMENT:
            amount = float(candidate.parameters.get("amount", 0))
            diff["state_before"] = {"treasury_balance": 50000.0}
            diff["state_after"] = {"treasury_balance": 50000.0 - amount}
            diff["mutation_summary"] = f"Debit ${amount:,.2f} to account '{candidate.target}'."
            diff["is_reversible"] = False
            diff["rollback_plan"] = "BANK WIRE / BLOCKCHAIN IS IRREVERSIBLE. Requires manual chargeback dispute."

        return diff
