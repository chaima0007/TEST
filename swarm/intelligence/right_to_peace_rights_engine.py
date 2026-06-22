#!/usr/bin/env python3
"""
Right to Peace Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Right to Peace Rights Engine Agent"
ACCENT = "#0c4a6e"

ENTITIES = [
    ("RTP-001", 99, 97, 96, 95),
    ("RTP-002", 95, 93, 91, 89),
    ("RTP-003", 87, 85, 83, 81),
    ("RTP-004", 78, 76, 74, 72),
    ("RTP-005", 59, 57, 55, 53),
    ("RTP-006", 51, 49, 47, 45),
    ("RTP-007", 31, 29, 27, 25),
    ("RTP-008", 11, 9, 7, 5),
]


def calculate_composite(armed_conflict_persistence_score, militarization_civilian_harm_score,
                         peace_negotiation_exclusion_score, disarmament_failure_score):
    return round(
        armed_conflict_persistence_score * 0.30
        + militarization_civilian_harm_score * 0.25
        + peace_negotiation_exclusion_score * 0.25
        + disarmament_failure_score * 0.20,
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
        estimated_right_to_peace_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "armed_conflict_persistence_score": s1,
            "militarization_civilian_harm_score": s2,
            "peace_negotiation_exclusion_score": s3,
            "disarmament_failure_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_right_to_peace_index": estimated_right_to_peace_index,
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
            f" — estimated_right_to_peace_index={r['estimated_right_to_peace_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
