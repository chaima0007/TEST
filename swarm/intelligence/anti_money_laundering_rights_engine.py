#!/usr/bin/env python3
"""
Anti Money Laundering Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Anti Money Laundering Rights Engine Agent"
ACCENT = "#065f46"

ENTITIES = [
    ("AML-001", 99, 97, 95, 93),
    ("AML-002", 93, 91, 89, 87),
    ("AML-003", 86, 84, 82, 80),
    ("AML-004", 78, 76, 74, 72),
    ("AML-005", 61, 59, 57, 55),
    ("AML-006", 51, 49, 47, 45),
    ("AML-007", 31, 29, 27, 25),
    ("AML-008", 11, 9, 7, 5),
]

def calculate_composite(illicit_finance_human_rights_score,
                         asset_recovery_failure_score,
                         offshore_secrecy_score,
                         beneficial_ownership_gap_score):
    return round(
        illicit_finance_human_rights_score * 0.30
        + asset_recovery_failure_score * 0.25
        + offshore_secrecy_score * 0.25
        + beneficial_ownership_gap_score * 0.20,
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
        estimated_anti_money_laundering_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "illicit_finance_human_rights_score": s1,
            "asset_recovery_failure_score": s2,
            "offshore_secrecy_score": s3,
            "beneficial_ownership_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_anti_money_laundering_index": estimated_anti_money_laundering_index,
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
            f" — estimated_anti_money_laundering_index={r['estimated_anti_money_laundering_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
