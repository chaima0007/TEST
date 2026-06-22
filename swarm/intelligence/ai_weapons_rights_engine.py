#!/usr/bin/env python3
"""
AI Weapons Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "AI Weapons Rights Engine Agent"
ACCENT = "#1e293b"

ENTITIES = [
    ("AWR-001", 99, 97, 96, 94),
    ("AWR-002", 94, 92, 90, 88),
    ("AWR-003", 87, 85, 83, 81),
    ("AWR-004", 78, 76, 74, 72),
    ("AWR-005", 58, 56, 54, 52),
    ("AWR-006", 49, 47, 45, 43),
    ("AWR-007", 33, 31, 29, 27),
    ("AWR-008", 12, 10, 9, 7),
]

def calculate_composite(autonomous_weapon_civilian_harm_score,
                        accountability_gap_lethal_ai_score,
                        arms_race_destabilization_score,
                        ban_treaty_absence_score):
    return round(
        autonomous_weapon_civilian_harm_score * 0.30
        + accountability_gap_lethal_ai_score * 0.25
        + arms_race_destabilization_score * 0.25
        + ban_treaty_absence_score * 0.20,
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
        estimated_ai_weapons_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "autonomous_weapon_civilian_harm_score": s1,
            "accountability_gap_lethal_ai_score": s2,
            "arms_race_destabilization_score": s3,
            "ban_treaty_absence_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_ai_weapons_index": estimated_ai_weapons_index,
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
            f" — estimated_ai_weapons_index={r['estimated_ai_weapons_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
