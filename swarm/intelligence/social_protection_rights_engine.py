#!/usr/bin/env python3
"""
Social Protection Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Social Protection Rights Engine Agent"
ACCENT = "#0891b2"

ENTITIES = [
    ("SPR-001", 98, 95, 93, 91),
    ("SPR-002", 91, 88, 86, 84),
    ("SPR-003", 83, 80, 78, 76),
    ("SPR-004", 75, 73, 70, 68),
    ("SPR-005", 62, 59, 57, 55),
    ("SPR-006", 55, 53, 51, 49),
    ("SPR-007", 33, 31, 29, 27),
    ("SPR-008", 8, 6, 5, 4),
]


def calculate_composite(social_safety_net_gap_score, unemployment_benefit_denial_score,
                         pension_rights_violation_score, healthcare_social_protection_gap_score):
    return round(
        social_safety_net_gap_score * 0.30
        + unemployment_benefit_denial_score * 0.25
        + pension_rights_violation_score * 0.25
        + healthcare_social_protection_gap_score * 0.20,
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
        estimated_social_protection_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "social_safety_net_gap_score": s1,
            "unemployment_benefit_denial_score": s2,
            "pension_rights_violation_score": s3,
            "healthcare_social_protection_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_social_protection_index": estimated_social_protection_index,
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
            f" | estimated_social_protection_index={r['estimated_social_protection_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
