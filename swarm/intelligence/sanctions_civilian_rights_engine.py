#!/usr/bin/env python3
"""
Sanctions Civilian Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Sanctions Civilian Rights Engine Agent"
ACCENT = "#44403c"

ENTITIES = [
    ("SCR-001", 99, 97, 96, 94),
    ("SCR-002", 93, 91, 89, 87),
    ("SCR-003", 85, 83, 81, 79),
    ("SCR-004", 76, 74, 72, 70),
    ("SCR-005", 59, 57, 55, 53),
    ("SCR-006", 50, 48, 46, 44),
    ("SCR-007", 35, 33, 31, 29),
    ("SCR-008", 12, 10, 9, 8),
]

def calculate_composite(humanitarian_goods_blockage_score,
                         medicine_access_denial_score,
                         civilian_economic_impact_score,
                         sanctions_exemption_gap_score):
    return round(
        humanitarian_goods_blockage_score * 0.30
        + medicine_access_denial_score * 0.25
        + civilian_economic_impact_score * 0.25
        + sanctions_exemption_gap_score * 0.20,
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
        estimated_sanctions_civilian_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "humanitarian_goods_blockage_score": s1,
            "medicine_access_denial_score": s2,
            "civilian_economic_impact_score": s3,
            "sanctions_exemption_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_sanctions_civilian_index": estimated_sanctions_civilian_index,
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
