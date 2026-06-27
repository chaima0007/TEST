#!/usr/bin/env python3
"""
Right to Leisure Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Right to Leisure Rights Engine Agent"
ACCENT = "#6d28d9"

ENTITIES = [
    ("RTL-001", 98, 95, 93, 91),
    ("RTL-002", 91, 88, 86, 84),
    ("RTL-003", 83, 80, 78, 76),
    ("RTL-004", 75, 73, 70, 68),
    ("RTL-005", 62, 59, 57, 55),
    ("RTL-006", 55, 53, 51, 49),
    ("RTL-007", 33, 31, 29, 27),
    ("RTL-008", 8, 6, 5, 4),
]


def calculate_composite(overwork_exploitation_score, rest_time_denial_score,
                         vacation_rights_violation_score, cultural_participation_exclusion_score):
    return round(
        overwork_exploitation_score * 0.30
        + rest_time_denial_score * 0.25
        + vacation_rights_violation_score * 0.25
        + cultural_participation_exclusion_score * 0.20,
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
        estimated_right_to_leisure_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "overwork_exploitation_score": s1,
            "rest_time_denial_score": s2,
            "vacation_rights_violation_score": s3,
            "cultural_participation_exclusion_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_right_to_leisure_index": estimated_right_to_leisure_index,
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
            f" | estimated_right_to_leisure_index={r['estimated_right_to_leisure_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
