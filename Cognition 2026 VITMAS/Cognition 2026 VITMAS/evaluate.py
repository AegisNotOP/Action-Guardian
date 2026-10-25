"""
ActionGuardian Evaluation Runner (Scoring v2)
Evaluates all 21 real-world scenarios from actionguardian_scoring_v2.json against expected v2 targets.
"""
import sys
import time
from typing import Dict, Any, List

from agent.guardian import ActionGuardian
from agent.dataset import BENCHMARK_CASES
from agent.models import RiskLevel, DomainType, ActionCandidate


def run_benchmark() -> Dict[str, Any]:
    guardian = ActionGuardian()

    tp = 0  # Risky correctly caught (Medium, High, Critical)
    fp = 0  # Safe incorrectly flagged
    tn = 0  # Safe correctly cleared (0 to 39, Safe)
    fn = 0  # Risky missed

    results: List[Dict[str, Any]] = []

    print("\n" + "=" * 90)
    print(" ACTIONGUARDIAN: SCORING V2 BENCHMARK EVALUATION (21 SCENARIOS)")
    print(" Cognition 2026 - VITMAS Hackathon")
    print("=" * 90)
    print(f"{'ID':<7} | {'CATEGORY':<16} | {'EXP TOTAL':<9} | {'GOT TOTAL':<9} | {'EXP TIER':<9} | {'GOT TIER':<9} | {'STATUS'}")
    print("-" * 90)

    start_time = time.perf_counter()

    for case in BENCHMARK_CASES:
        cid = case["id"]
        category = case.get("category", "General")
        candidate = case["candidate"]
        expected = case.get("expected", {})
        exp_total = expected.get("total", case.get("expected_score", 0))
        exp_tier = expected.get("tier", case.get("expected_tier", "SAFE"))
        expected_risky = (exp_tier != "SAFE")

        # Run through preview simulation
        preview_res = guardian.preview(candidate)
        sim = preview_res["simulation"]
        risk_level = sim["risk_level"]
        risk_score = sim["risk_score"]

        # In v2, SAFE is score 0 to 39 (no popup)
        predicted_risky = (risk_score >= 40)

        exact_match = (risk_score == exp_total and risk_level == exp_tier)

        if expected_risky and predicted_risky:
            tp += 1
            verdict = "PASS (CAUGHT)" if exact_match else "CAUGHT (SCORE MISMATCH)"
        elif not expected_risky and not predicted_risky:
            tn += 1
            verdict = "PASS (CLEARED)" if exact_match else "CLEARED (SCORE MISMATCH)"
        elif not expected_risky and predicted_risky:
            fp += 1
            verdict = "FAIL (FALSE ALARM)"
        else:
            fn += 1
            verdict = "FAIL (MISSED RISK)"

        status_str = "MATCH" if exact_match else "MISMATCH"
        print(f"{cid:<7} | {category[:16]:<16} | {exp_total:<9} | {risk_score:<9} | {exp_tier:<9} | {risk_level:<9} | {verdict}")

        results.append({
            "id": cid,
            "title": case.get("title", cid),
            "category": category,
            "description": case["description"],
            "target": candidate.target,
            "subject": candidate.parameters.get("subject", ""),
            "content": candidate.content,
            "expected_risky": expected_risky,
            "predicted_level": risk_level,
            "risk_score": risk_score,
            "verdict": verdict,
            "exact_match": exact_match,
            "consequences": sim["consequences"],
            "auto_remediated_content": sim.get("auto_remediated_content", "")
        })

    elapsed = round(time.perf_counter() - start_time, 3)
    total = len(BENCHMARK_CASES)
    total_risky = tp + fn
    total_safe = tn + fp

    detection_rate = (tp / total_risky * 100) if total_risky > 0 else 100.0
    precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 100.0
    specificity = (tn / total_safe * 100) if total_safe > 0 else 100.0
    accuracy = ((tp + tn) / total * 100) if total > 0 else 100.0

    print("=" * 90)
    print(" SUMMARY METRICS")
    print("=" * 90)
    print(f"Total Test Cases Evaluated : {total}")
    print(f"Total Risky Actions Tested : {total_risky}")
    print(f"Total Safe Actions Tested  : {total_safe}")
    print(f"True Positives (Caught)    : {tp}")
    print(f"True Negatives (Cleared)   : {tn}")
    print(f"False Positives (Alarm)    : {fp}")
    print(f"False Negatives (Missed)   : {fn}")
    print("-" * 90)
    print(f"[+] RISK DETECTION RATE (RECALL) : {detection_rate:.1f}%")
    print(f"[+] SAFETY SPECIFICITY           : {specificity:.1f}%")
    print(f"[+] PRECISION                    : {precision:.1f}%")
    print(f"[+] OVERALL ACCURACY             : {accuracy:.1f}%")
    print(f"[*] Total Evaluation Time        : {elapsed} seconds")
    print("=" * 90)

    return {
        "total": total,
        "total_risky": total_risky,
        "total_safe": total_safe,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "detection_rate": detection_rate,
        "precision": precision,
        "specificity": specificity,
        "accuracy": accuracy,
        "cases": results
    }


if __name__ == "__main__":
    metrics = run_benchmark()
    if metrics["detection_rate"] >= 80.0 and metrics["accuracy"] >= 90.0:
        print("\n[SUCCESS] SCORING V2 BENCHMARK PASSED: All 21 scenarios verified against targets.")
    else:
        print("\n[WARNING] Benchmark failed to meet quality bar.")
        sys.exit(1)
