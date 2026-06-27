#!/usr/bin/env python3
"""
Algorithmic Discrimination Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Algorithmic Discrimination Rights Engine Agent"
ACCENT = "#4338ca"

ENTITIES = [
    ("ADR-001", 99, 97, 95, 93),
    ("ADR-002", 93, 91, 89, 87),
    ("ADR-003", 86, 84, 82, 80),
    ("ADR-004", 78, 76, 74, 72),
    ("ADR-005", 61, 59, 57, 55),
    ("ADR-006", 51, 49, 47, 45),
    ("ADR-007", 31, 29, 27, 25),
    ("ADR-008", 11, 9, 7, 5),
]

def calculate_composite(biased_ai_deployment_score,
                         predictive_policing_bias_score,
                         hiring_algorithm_discrimination_score,
                         ai_accountability_gap_score):
    return round(
        biased_ai_deployment_score * 0.30
        + predictive_policing_bias_score * 0.25
        + hiring_algorithm_discrimination_score * 0.25
        + ai_accountability_gap_score * 0.20,
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
        estimated_algorithmic_discrimination_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "biased_ai_deployment_score": s1,
            "predictive_policing_bias_score": s2,
            "hiring_algorithm_discrimination_score": s3,
            "ai_accountability_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_algorithmic_discrimination_index": estimated_algorithmic_discrimination_index,
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
            f" — estimated_algorithmic_discrimination_index={r['estimated_algorithmic_discrimination_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
