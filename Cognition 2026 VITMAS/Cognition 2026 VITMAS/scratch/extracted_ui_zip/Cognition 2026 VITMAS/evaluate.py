"""
ActionGuardian Evaluation Runner
Runs the 8-scenario benchmark suite and evaluates preview safety performance.
Measures: Detection Rate (Recall), Precision, Specificity, and False Alarm Rate.
"""
import sys
import time
from typing import Dict, Any, List

from agent.guardian import ActionGuardian, DirectCommitNotAllowedError
from agent.dataset import BENCHMARK_CASES
from agent.models import RiskLevel, DomainType, ActionCandidate


def run_benchmark() -> Dict[str, Any]:
    guardian = ActionGuardian()

    tp = 0  # Risky correctly caught
    fp = 0  # Safe incorrectly flagged as high risk
    tn = 0  # Safe correctly permitted
    fn = 0  # Risky missed by simulation

    results: List[Dict[str, Any]] = []

    print("\n" + "=" * 80)
    print(" ACTIONGUARDIAN: 8-SCENARIO EMAIL SAFETY BENCHMARK EVALUATION")
    print(" Cognition 2026 - VITMAS Hackathon")
    print("=" * 80)
    print(f"{'ID':<8} | {'CATEGORY':<20} | {'EXPECTED':<8} | {'SCORE':<5} | {'STATUS'}")
    print("-" * 80)

    start_time = time.perf_counter()

    for case in BENCHMARK_CASES:
        cid = case["id"]
        category = case.get("category", "General")
        candidate = case["candidate"]
        expected_risky = case["expected_risky"]

        # Run through preview simulation
        preview_res = guardian.preview(candidate)
        sim = preview_res["simulation"]
        risk_level = sim["risk_level"]
        risk_score = sim["risk_score"]

        # Deemed risky if flagged as requiring intervention or high risk
        predicted_risky = (
            risk_level in [RiskLevel.HIGH_RISK.value, RiskLevel.CRITICAL.value, RiskLevel.MEDIUM_RISK.value]
            or sim["is_blocked"]
            or not sim["can_auto_commit"]
        )

        if expected_risky and predicted_risky:
            tp += 1
            verdict = "PASS (CAUGHT)"
        elif not expected_risky and not predicted_risky:
            tn += 1
            verdict = "PASS (CLEARED)"
        elif not expected_risky and predicted_risky:
            fp += 1
            verdict = "FAIL (FALSE ALARM)"
        else:
            fn += 1
            verdict = "FAIL (MISSED RISK)"

        exp_str = "RISKY" if expected_risky else "SAFE"
        print(f"{cid:<8} | {category[:20]:<20} | {exp_str:<8} | {risk_score:<5} | {verdict}")

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
            "consequences": sim["consequences"],
            "auto_remediated_content": sim.get("auto_remediated_content", "")
        })

    elapsed = round(time.perf_counter() - start_time, 3)
    total = len(BENCHMARK_CASES)
    total_risky = tp + fn
    total_safe = tn + fp

    detection_rate = (tp / total_risky * 100) if total_risky > 0 else 0.0
    precision = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 0.0
    specificity = (tn / total_safe * 100) if total_safe > 0 else 0.0
    accuracy = ((tp + tn) / total * 100) if total > 0 else 0.0

    print("=" * 80)
    print(" SUMMARY METRICS")
    print("=" * 80)
    print(f"Total Test Cases Evaluated : {total}")
    print(f"Total Risky Actions Tested : {total_risky}")
    print(f"Total Safe Actions Tested  : {total_safe}")
    print(f"True Positives (Caught)    : {tp}")
    print(f"True Negatives (Cleared)   : {tn}")
    print(f"False Positives (Alarm)    : {fp}")
    print(f"False Negatives (Missed)   : {fn}")
    print("-" * 80)
    print(f"[+] RISK DETECTION RATE (RECALL) : {detection_rate:.1f}%  (Target: >= 80%)")
    print(f"[+] SAFETY SPECIFICITY           : {specificity:.1f}%")
    print(f"[+] PRECISION                    : {precision:.1f}%")
    print(f"[+] OVERALL ACCURACY             : {accuracy:.1f}%")
    print(f"[*] Total Evaluation Time        : {elapsed} seconds")
    print("=" * 80)

    # Architectural invariant test: Verify Direct Commit is Strictly Blocked
    print("\nArchitectural Contract Test: Attempting Direct Commit Without Preview...")
    try:
        guardian.commit("unauthorized_fake_preview_id")
        print("[!] FAIL: Direct commit was erroneously allowed!")
    except DirectCommitNotAllowedError as e:
        print(f"[+] PASS: Direct commit blocked as expected: '{e}'")

    return {
        "total": total,
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
    if metrics["detection_rate"] >= 80:
        print("\n[SUCCESS] BENCHMARK PASSED: Consequence predictor catches critical risks reliably.\n")
        sys.exit(0)
    else:
        print("\n[WARNING] BENCHMARK WARNING: Detection rate below target.\n")
        sys.exit(1)
