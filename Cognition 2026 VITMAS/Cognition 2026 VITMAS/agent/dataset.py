"""
Curated Benchmark Dataset for Cognition 2026 Hackathon (Scoring v2)
Loads the 21 real-world scenarios from actionguardian_scoring_v2.json.
"""
import os
import json
from typing import List, Dict, Any
from .models import ActionCandidate, DomainType

DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "actionguardian_scoring_v2.json")

def load_benchmark_cases() -> List[Dict[str, Any]]:
    cases = []
    if os.path.exists(DATASET_FILE):
        try:
            with open(DATASET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for sc in data.get("scenarios", []):
                recipient_context = sc.get("recipient_context", "").lower()
                target = "colleague@gmail.com"
                if "all@" in recipient_context or "300 people" in recipient_context or "team alias" in recipient_context:
                    target = "all@company.com"
                elif "external" in recipient_context or "journalist" in recipient_context:
                    target = "external.contact@gmail.com"
                elif "internal" in recipient_context:
                    target = "internal.team@company.com"

                candidate = ActionCandidate(
                    domain=DomainType.EMAIL,
                    target=target,
                    action_type="SEND_EMAIL",
                    content=sc.get("body", ""),
                    parameters={"subject": sc.get("subject", "")}
                )

                expected = sc.get("expected", {})
                expected_tier = expected.get("tier", "SAFE")
                is_risky = (expected_tier != "SAFE")

                cases.append({
                    "id": sc.get("id"),
                    "type": "risky" if is_risky else "safe",
                    "category": sc.get("inputs", {}).get("intent_type", "general").upper().replace("_", " "),
                    "category_chip": sc.get("inputs", {}).get("intent_type", "general").upper().replace("_", " "),
                    "title": sc.get("title", ""),
                    "description": f"{sc.get('persona', 'Agent')}: {sc.get('prompt_to_agent', '')} ({sc.get('recipient_context', '')})",
                    "persona": sc.get("persona", ""),
                    "prompt_to_agent": sc.get("prompt_to_agent", ""),
                    "recipient_context": sc.get("recipient_context", ""),
                    "subject": sc.get("subject", ""),
                    "body": sc.get("body", ""),
                    "content": sc.get("body", ""),
                    "inputs": sc.get("inputs", {}),
                    "expected": expected,
                    "expected_risky": is_risky,
                    "expected_score": expected.get("total", 0),
                    "expected_tier": expected_tier,
                    "target": target,
                    "candidate": candidate
                })
            return cases
        except Exception as e:
            print(f"[Dataset] Warning loading json: {e}")

    return cases

BENCHMARK_CASES: List[Dict[str, Any]] = load_benchmark_cases()
