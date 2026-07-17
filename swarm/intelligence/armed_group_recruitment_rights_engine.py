#!/usr/bin/env python3
"""
Armed Group Recruitment Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Armed Group Recruitment Rights Engine Agent"
ACCENT = "#7f1d1d"

ENTITIES = [
    ("AGR-001", 100, 98, 97, 96),
    ("AGR-002", 95, 93, 91, 89),
    ("AGR-003", 88, 85, 83, 81),
    ("AGR-004", 79, 77, 75, 73),
    ("AGR-005", 58, 55, 53, 51),
    ("AGR-006", 49, 47, 45, 43),
    ("AGR-007", 30, 28, 26, 24),
    ("AGR-008", 10, 8, 7, 5),
]

def calculate_composite(forced_recruitment_score,
                        economic_coercion_recruitment_score,
                        youth_targeting_score,
                        international_law_violation_score):
    return round(
        forced_recruitment_score * 0.30
        + economic_coercion_recruitment_score * 0.25
        + youth_targeting_score * 0.25
        + international_law_violation_score * 0.20,
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
        estimated_armed_group_recruitment_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "forced_recruitment_score": s1,
            "economic_coercion_recruitment_score": s2,
            "youth_targeting_score": s3,
            "international_law_violation_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_armed_group_recruitment_index": estimated_armed_group_recruitment_index,
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
            f"estimated_armed_group_recruitment_index={r['estimated_armed_group_recruitment_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
