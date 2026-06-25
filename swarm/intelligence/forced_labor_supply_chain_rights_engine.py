#!/usr/bin/env python3
"""
Forced Labor Supply Chain Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Forced Labor Supply Chain Rights Engine Agent"

ENTITIES = [
    ("FLS-001", 99, 96, 94, 92),  # critique
    ("FLS-002", 93, 90, 88, 86),  # critique
    ("FLS-003", 86, 83, 81, 79),  # critique
    ("FLS-004", 78, 76, 73, 71),  # critique
    ("FLS-005", 62, 59, 57, 55),  # élevé
    ("FLS-006", 51, 49, 47, 45),  # élevé
    ("FLS-007", 30, 28, 26, 24),  # modéré
    ("FLS-008", 10, 8, 7, 6),     # faible
]


def calculate_composite(s1, s2, s3, s4):
    return round(s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20, 2)


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
        estimated_forced_labor_supply_chain_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "supply_chain_forced_labor_score": s1,
            "corporate_due_diligence_gap_score": s2,
            "debt_bondage_score": s3,
            "repatriation_failure_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_forced_labor_supply_chain_index": estimated_forced_labor_supply_chain_index,
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
