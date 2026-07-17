#!/usr/bin/env python3
"""
Ecocide Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Ecocide Rights Engine Agent"
ACCENT = "#166534"

ENTITIES = [
    ("ECR-001", 98, 97, 96, 95),
    ("ECR-002", 93, 91, 90, 88),
    ("ECR-003", 85, 83, 82, 80),
    ("ECR-004", 77, 75, 73, 71),
    ("ECR-005", 58, 56, 54, 52),
    ("ECR-006", 49, 47, 46, 44),
    ("ECR-007", 31, 29, 27, 25),
    ("ECR-008", 11, 9, 8, 6),
]


def calculate_composite(large_scale_ecosystem_destruction_score, corporate_environmental_impunity_score,
                        indigenous_land_ecocide_score, international_law_gap_score):
    return round(
        large_scale_ecosystem_destruction_score * 0.30
        + corporate_environmental_impunity_score * 0.25
        + indigenous_land_ecocide_score * 0.25
        + international_law_gap_score * 0.20,
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
        estimated_ecocide_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "large_scale_ecosystem_destruction_score": s1,
            "corporate_environmental_impunity_score": s2,
            "indigenous_land_ecocide_score": s3,
            "international_law_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_ecocide_index": estimated_ecocide_index,
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
            f" — estimated_ecocide_index={r['estimated_ecocide_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
