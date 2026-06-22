#!/usr/bin/env python3
"""
Deepfake Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Deepfake Rights Engine Agent"

ENTITIES = [
    ("DFR-001", 99, 96, 94, 92),  # critique
    ("DFR-002", 93, 90, 88, 86),  # critique
    ("DFR-003", 86, 83, 81, 79),  # critique
    ("DFR-004", 78, 76, 73, 71),  # critique
    ("DFR-005", 62, 59, 57, 55),  # élevé
    ("DFR-006", 51, 49, 47, 45),  # élevé
    ("DFR-007", 30, 28, 26, 24),  # modéré
    ("DFR-008", 10, 8, 7, 6),     # faible
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
        estimated_deepfake_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "non_consensual_deepfake_score": s1,
            "political_disinformation_deepfake_score": s2,
            "identity_fraud_deepfake_score": s3,
            "legal_framework_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_deepfake_index": estimated_deepfake_index,
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
