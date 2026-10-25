"""
Unit tests for ActionGuardian core logic and API.
"""
import unittest
from agent.models import ActionCandidate, DomainType, RiskLevel
from agent.guardian import (
    ActionGuardian,
    DirectCommitNotAllowedError,
    ActionBlockedError,
    HumanConfirmationRequiredError
)


class TestActionGuardian(unittest.TestCase):

    def setUp(self):
        self.guardian = ActionGuardian()

    def test_direct_commit_forbidden(self):
        """Test that committing without preview raises DirectCommitNotAllowedError."""
        with self.assertRaises(DirectCommitNotAllowedError):
            self.guardian.commit("non_existent_preview_id")

    def test_safe_action_auto_commit(self):
        """Test that a benign action receives low risk and can commit cleanly."""
        candidate = ActionCandidate(
            domain=DomainType.EMAIL,
            target="colleague@company.com",
            action_type="SEND_EMAIL",
            content="Hi, please review the PR when you have time.",
            parameters={}
        )
        res = self.guardian.preview(candidate)
        self.assertEqual(res["simulation"]["risk_level"], RiskLevel.SAFE.value)
        self.assertTrue(res["simulation"]["can_auto_commit"])
        self.assertFalse(res["simulation"]["is_blocked"])

        # Execute commit
        receipt = self.guardian.commit(res["preview_id"])
        self.assertEqual(receipt.status, "SUCCESS")

    def test_credential_leak_blocked(self):
        """Test that credentials in email are flagged as CRITICAL and blocked."""
        candidate = ActionCandidate(
            domain=DomainType.EMAIL,
            target="outsider@gmail.com",
            action_type="SEND_EMAIL",
            content="Here is the master AWS key: AKIAIOSFODNN7EXAMPLE",
            parameters={}
        )
        res = self.guardian.preview(candidate)
        self.assertEqual(res["simulation"]["risk_level"], RiskLevel.CRITICAL.value)
        self.assertTrue(res["simulation"]["is_blocked"])

        # Attempt commit without override should fail
        with self.assertRaises(ActionBlockedError):
            self.guardian.commit(res["preview_id"], user_override=False)

    def test_destructive_code_deploy(self):
        """Test that DROP TABLE in production is flagged as CRITICAL."""
        candidate = ActionCandidate(
            domain=DomainType.CODE_DEPLOY,
            target="prod-db",
            action_type="MIGRATION",
            content="DROP TABLE user_records;",
            parameters={"environment": "production"}
        )
        res = self.guardian.preview(candidate)
        self.assertEqual(res["simulation"]["risk_level"], RiskLevel.CRITICAL.value)
        self.assertTrue(res["simulation"]["is_blocked"])
        self.assertFalse(res["dry_run_diff"]["is_reversible"])


if __name__ == "__main__":
    unittest.main()
