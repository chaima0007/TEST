#!/usr/bin/env python3
"""
Post Conflict Reconstruction Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Post Conflict Reconstruction Rights Engine Agent"
ACCENT = "#4b5563"

ENTITIES = [
    ("PCR-001", 99, 97, 96, 95),
    ("PCR-002", 95, 93, 91, 89),
    ("PCR-003", 87, 85, 83, 81),
    ("PCR-004", 78, 76, 74, 72),
    ("PCR-005", 59, 57, 55, 53),
    ("PCR-006", 51, 49, 47, 45),
    ("PCR-007", 31, 29, 27, 25),
    ("PCR-008", 11, 9, 7, 5),
]


def calculate_composite(reconstruction_exclusion_score, transitional_justice_failure_score,
                         reparation_program_gap_score, reconciliation_mechanism_absence_score):
    return round(
        reconstruction_exclusion_score * 0.30
        + transitional_justice_failure_score * 0.25
        + reparation_program_gap_score * 0.25
        + reconciliation_mechanism_absence_score * 0.20,
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
        estimated_post_conflict_reconstruction_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "reconstruction_exclusion_score": s1,
            "transitional_justice_failure_score": s2,
            "reparation_program_gap_score": s3,
            "reconciliation_mechanism_absence_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_post_conflict_reconstruction_index": estimated_post_conflict_reconstruction_index,
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
            f" — estimated_post_conflict_reconstruction_index={r['estimated_post_conflict_reconstruction_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
