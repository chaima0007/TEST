#!/usr/bin/env python3
"""
Indigenous Self Determination Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Indigenous Self Determination Rights Engine Agent"
ACCENT = "#14532d"

ENTITIES = [
    ("ISD-001", 98, 97, 96, 95),
    ("ISD-002", 93, 91, 90, 88),
    ("ISD-003", 85, 83, 82, 80),
    ("ISD-004", 77, 75, 73, 71),
    ("ISD-005", 58, 56, 54, 52),
    ("ISD-006", 49, 47, 46, 44),
    ("ISD-007", 31, 29, 27, 25),
    ("ISD-008", 11, 9, 8, 6),
]


def calculate_composite(autonomy_suppression_score, fpic_violation_score,
                        territorial_sovereignty_denial_score, governance_interference_score):
    return round(
        autonomy_suppression_score * 0.30
        + fpic_violation_score * 0.25
        + territorial_sovereignty_denial_score * 0.25
        + governance_interference_score * 0.20,
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
        estimated_indigenous_self_determination_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "autonomy_suppression_score": s1,
            "fpic_violation_score": s2,
            "territorial_sovereignty_denial_score": s3,
            "governance_interference_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_indigenous_self_determination_index": estimated_indigenous_self_determination_index,
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
            f" — estimated_indigenous_self_determination_index={r['estimated_indigenous_self_determination_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
