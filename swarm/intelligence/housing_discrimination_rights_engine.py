#!/usr/bin/env python3
"""
Housing Discrimination Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Housing Discrimination Rights Engine Agent"

ENTITIES = [
    ("HDR-001", 99, 96, 94, 92),  # critique
    ("HDR-002", 93, 90, 88, 86),  # critique
    ("HDR-003", 86, 83, 81, 79),  # critique
    ("HDR-004", 78, 76, 73, 71),  # critique
    ("HDR-005", 62, 59, 57, 55),  # élevé
    ("HDR-006", 51, 49, 47, 45),  # élevé
    ("HDR-007", 30, 28, 26, 24),  # modéré
    ("HDR-008", 10, 8, 7, 6),     # faible
]


def calculate_composite(s1, s2, s3, s4):
    return round(s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20, 2)


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
        estimated_housing_discrimination_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "racial_housing_discrimination_score": s1,
            "eviction_abuse_score": s2,
            "segregation_persistence_score": s3,
            "housing_policy_bias_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_housing_discrimination_index": estimated_housing_discrimination_index,
        })
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}]")
    return results


if __name__ == "__main__":
    run_engine()
