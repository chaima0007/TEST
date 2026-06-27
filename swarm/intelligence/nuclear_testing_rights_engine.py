#!/usr/bin/env python3
"""
Nuclear Testing Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Nuclear Testing Rights Engine Agent"
ACCENT = "#7f1d1d"

ENTITIES = [
    ("NTR-001", 99, 97, 96, 94),
    ("NTR-002", 93, 91, 89, 87),
    ("NTR-003", 85, 83, 81, 79),
    ("NTR-004", 76, 74, 72, 70),
    ("NTR-005", 59, 57, 55, 53),
    ("NTR-006", 50, 48, 46, 44),
    ("NTR-007", 35, 33, 31, 29),
    ("NTR-008", 12, 10, 9, 8),
]

def calculate_composite(radiation_exposure_civilian_score,
                         testing_zone_displacement_score,
                         long_term_health_impact_score,
                         reparation_denial_score):
    return round(
        radiation_exposure_civilian_score * 0.30
        + testing_zone_displacement_score * 0.25
        + long_term_health_impact_score * 0.25
        + reparation_denial_score * 0.20,
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
        estimated_nuclear_testing_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "radiation_exposure_civilian_score": s1,
            "testing_zone_displacement_score": s2,
            "long_term_health_impact_score": s3,
            "reparation_denial_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_nuclear_testing_index": estimated_nuclear_testing_index,
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
