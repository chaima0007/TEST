#!/usr/bin/env python3
"""
Water Conflict Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Water Conflict Rights Engine Agent"
ACCENT = "#0369a1"

ENTITIES = [
    ("WCR-001", 99, 97, 96, 94),
    ("WCR-002", 94, 92, 90, 88),
    ("WCR-003", 87, 85, 83, 81),
    ("WCR-004", 78, 76, 74, 72),
    ("WCR-005", 58, 56, 54, 52),
    ("WCR-006", 49, 47, 45, 43),
    ("WCR-007", 33, 31, 29, 27),
    ("WCR-008", 12, 10, 9, 7),
]

def calculate_composite(transboundary_water_conflict_score,
                        weaponization_water_score,
                        dam_displacement_score,
                        water_rights_enforcement_gap_score):
    return round(
        transboundary_water_conflict_score * 0.30
        + weaponization_water_score * 0.25
        + dam_displacement_score * 0.25
        + water_rights_enforcement_gap_score * 0.20,
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
        estimated_water_conflict_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "transboundary_water_conflict_score": s1,
            "weaponization_water_score": s2,
            "dam_displacement_score": s3,
            "water_rights_enforcement_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_water_conflict_index": estimated_water_conflict_index,
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
            f" — estimated_water_conflict_index={r['estimated_water_conflict_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
