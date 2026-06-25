#!/usr/bin/env python3
"""
Prison Reform Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Prison Reform Rights Engine Agent"
ACCENT = "#374151"

ENTITIES = [
    ("PRR-001", 98, 95, 93, 91),
    ("PRR-002", 91, 88, 86, 84),
    ("PRR-003", 83, 80, 78, 76),
    ("PRR-004", 75, 73, 70, 68),
    ("PRR-005", 62, 59, 57, 55),
    ("PRR-006", 55, 53, 51, 49),
    ("PRR-007", 33, 31, 29, 27),
    ("PRR-008", 8, 6, 5, 4),
]


def calculate_composite(inhumane_prison_conditions_score, solitary_overuse_score,
                         prison_corruption_score, reintegration_failure_score):
    return round(
        inhumane_prison_conditions_score * 0.30
        + solitary_overuse_score * 0.25
        + prison_corruption_score * 0.25
        + reintegration_failure_score * 0.20,
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
        estimated_prison_reform_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "inhumane_prison_conditions_score": s1,
            "solitary_overuse_score": s2,
            "prison_corruption_score": s3,
            "reintegration_failure_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_prison_reform_index": estimated_prison_reform_index,
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
            f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}]"
            f" | estimated_prison_reform_index={r['estimated_prison_reform_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
