#!/usr/bin/env python3
"""
Mass Incarceration Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Mass Incarceration Rights Engine Agent"

ENTITIES = [
    ("MIR-001", 99, 97, 96, 94),
    ("MIR-002", 93, 91, 89, 87),
    ("MIR-003", 85, 83, 81, 79),
    ("MIR-004", 77, 75, 73, 71),
    ("MIR-005", 63, 60, 58, 56),
    ("MIR-006", 52, 49, 47, 45),
    ("MIR-007", 32, 29, 27, 25),
    ("MIR-008", 12, 9, 8, 6),
]

def calculate_composite(prison_overcrowding_score, racial_incarceration_bias_score, private_prison_rights_violation_score, rehabilitation_absence_score):
    return round(
        prison_overcrowding_score * 0.30
        + racial_incarceration_bias_score * 0.25
        + private_prison_rights_violation_score * 0.25
        + rehabilitation_absence_score * 0.20,
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
        estimated_mass_incarceration_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "prison_overcrowding_score": s1,
            "racial_incarceration_bias_score": s2,
            "private_prison_rights_violation_score": s3,
            "rehabilitation_absence_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_mass_incarceration_index": estimated_mass_incarceration_index,
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
            f" — estimated_mass_incarceration_index={r['estimated_mass_incarceration_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
