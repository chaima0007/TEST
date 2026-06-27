#!/usr/bin/env python3
"""
Platform Workers Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Platform Workers Rights Engine Agent"
ACCENT = "#1e40af"

ENTITIES = [
    ("PWR-001", 99, 98, 97, 96),
    ("PWR-002", 95, 93, 91, 89),
    ("PWR-003", 87, 85, 83, 81),
    ("PWR-004", 78, 76, 74, 72),
    ("PWR-005", 58, 56, 54, 52),
    ("PWR-006", 49, 47, 45, 43),
    ("PWR-007", 30, 28, 26, 24),
    ("PWR-008", 9, 7, 6, 5),
]


def calculate_composite(gig_worker_misclassification_score,
                         algorithm_wage_manipulation_score,
                         social_protection_exclusion_score,
                         collective_bargaining_denial_score):
    return round(
        gig_worker_misclassification_score * 0.30
        + algorithm_wage_manipulation_score * 0.25
        + social_protection_exclusion_score * 0.25
        + collective_bargaining_denial_score * 0.20,
        2,
    )


def classify_risk(score):
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    return "faible"


def run_engine():
    results = []
    for (eid, s1, s2, s3, s4) in ENTITIES:
        composite = calculate_composite(s1, s2, s3, s4)
        risk = classify_risk(composite)
        estimated_platform_workers_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "gig_worker_misclassification_score": s1,
            "algorithm_wage_manipulation_score": s2,
            "social_protection_exclusion_score": s3,
            "collective_bargaining_denial_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_platform_workers_index": estimated_platform_workers_index,
        })

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] "
            f"— estimated_platform_workers_index={r['estimated_platform_workers_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
