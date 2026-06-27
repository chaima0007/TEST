#!/usr/bin/env python3
"""
Supply Chain Transparency Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Supply Chain Transparency Rights Engine Agent"
ACCENT = "#1d4ed8"

ENTITIES = [
    ("SCT-001", 99, 97, 96, 94),
    ("SCT-002", 94, 92, 90, 88),
    ("SCT-003", 87, 85, 83, 81),
    ("SCT-004", 78, 76, 74, 72),
    ("SCT-005", 58, 56, 54, 52),
    ("SCT-006", 49, 47, 45, 43),
    ("SCT-007", 33, 31, 29, 27),
    ("SCT-008", 12, 10, 9, 7),
]

def calculate_composite(corporate_opacity_score,
                        due_diligence_absence_score,
                        audit_washing_score,
                        remedy_access_gap_score):
    return round(
        corporate_opacity_score * 0.30
        + due_diligence_absence_score * 0.25
        + audit_washing_score * 0.25
        + remedy_access_gap_score * 0.20,
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
        estimated_supply_chain_transparency_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "corporate_opacity_score": s1,
            "due_diligence_absence_score": s2,
            "audit_washing_score": s3,
            "remedy_access_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_supply_chain_transparency_index": estimated_supply_chain_transparency_index,
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
            f" — estimated_supply_chain_transparency_index={r['estimated_supply_chain_transparency_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
