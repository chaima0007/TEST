#!/usr/bin/env python3
"""
Climate Finance Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Climate Finance Rights Engine Agent"
ACCENT = "#166534"

ENTITIES = [
    ("CFR-001", 99, 97, 96, 95),
    ("CFR-002", 95, 93, 91, 89),
    ("CFR-003", 87, 85, 83, 81),
    ("CFR-004", 78, 76, 74, 72),
    ("CFR-005", 59, 57, 55, 53),
    ("CFR-006", 51, 49, 47, 45),
    ("CFR-007", 31, 29, 27, 25),
    ("CFR-008", 11, 9, 7, 5),
]


def calculate_composite(loss_damage_funding_gap_score, adaptation_fund_exclusion_score,
                         green_conditionality_harm_score, climate_finance_transparency_gap_score):
    return round(
        loss_damage_funding_gap_score * 0.30
        + adaptation_fund_exclusion_score * 0.25
        + green_conditionality_harm_score * 0.25
        + climate_finance_transparency_gap_score * 0.20,
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
        estimated_climate_finance_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "loss_damage_funding_gap_score": s1,
            "adaptation_fund_exclusion_score": s2,
            "green_conditionality_harm_score": s3,
            "climate_finance_transparency_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_climate_finance_index": estimated_climate_finance_index,
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
            f" — estimated_climate_finance_index={r['estimated_climate_finance_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
