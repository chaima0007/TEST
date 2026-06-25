#!/usr/bin/env python3
"""
Right to Development Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Right to Development Rights Engine Agent"
ACCENT = "#065f46"

ENTITIES = [
    ("RDD-001", 100, 98, 97, 96),
    ("RDD-002", 95, 93, 91, 89),
    ("RDD-003", 88, 85, 83, 81),
    ("RDD-004", 79, 77, 75, 73),
    ("RDD-005", 58, 55, 53, 51),
    ("RDD-006", 49, 47, 45, 43),
    ("RDD-007", 30, 28, 26, 24),
    ("RDD-008", 10, 8, 7, 5),
]

def calculate_composite(development_exclusion_score,
                        resource_benefit_denial_score,
                        development_forced_displacement_score,
                        participation_rights_gap_score):
    return round(
        development_exclusion_score * 0.30
        + resource_benefit_denial_score * 0.25
        + development_forced_displacement_score * 0.25
        + participation_rights_gap_score * 0.20,
        2
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
        estimated_right_to_development_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "development_exclusion_score": s1,
            "resource_benefit_denial_score": s2,
            "development_forced_displacement_score": s3,
            "participation_rights_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_right_to_development_index": estimated_right_to_development_index,
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
            f"  {r['entity_id']}: {r['composite_score']} "
            f"[{r['risk_level']}] "
            f"estimated_right_to_development_index={r['estimated_right_to_development_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
