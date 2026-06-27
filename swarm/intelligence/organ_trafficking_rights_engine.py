#!/usr/bin/env python3
"""
Organ Trafficking Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Organ Trafficking Rights Engine Agent"
ACCENT = "#dc2626"

ENTITIES = [
    ("OTR-001", 100, 97, 95, 92),
    ("OTR-002", 93, 90, 88, 86),
    ("OTR-003", 86, 83, 81, 79),
    ("OTR-004", 79, 77, 74, 72),
    ("OTR-005", 61, 58, 56, 54),
    ("OTR-006", 53, 51, 49, 47),
    ("OTR-007", 33, 31, 29, 27),
    ("OTR-008", 13, 11, 10, 9),
]

def calculate_composite(organ_trade_prevalence_score, transplant_tourism_score, donor_coercion_score, legal_enforcement_gap_score):
    return round(
        organ_trade_prevalence_score * 0.30
        + transplant_tourism_score * 0.25
        + donor_coercion_score * 0.25
        + legal_enforcement_gap_score * 0.20,
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
        estimated_organ_trafficking_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "organ_trade_prevalence_score": s1,
            "transplant_tourism_score": s2,
            "donor_coercion_score": s3,
            "legal_enforcement_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_organ_trafficking_index": estimated_organ_trafficking_index,
        })
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] — organ_trafficking_index={r['estimated_organ_trafficking_index']}")
    return results

if __name__ == "__main__":
    run_engine()
