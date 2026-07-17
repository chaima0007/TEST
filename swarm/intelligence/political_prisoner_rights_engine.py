#!/usr/bin/env python3
"""
Political Prisoner Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Political Prisoner Rights Engine Agent"
ACCENT = "#1e3a5f"

ENTITIES = [
    ("PPR-001", 99, 97, 96, 94),
    ("PPR-002", 93, 91, 89, 87),
    ("PPR-003", 85, 83, 81, 79),
    ("PPR-004", 76, 74, 72, 70),
    ("PPR-005", 59, 57, 55, 53),
    ("PPR-006", 50, 48, 46, 44),
    ("PPR-007", 35, 33, 31, 29),
    ("PPR-008", 12, 10, 9, 8),
]

def calculate_composite(arbitrary_detention_score,
                         torture_in_detention_score,
                         fair_trial_denial_score,
                         prisoner_of_conscience_score):
    return round(
        arbitrary_detention_score * 0.30
        + torture_in_detention_score * 0.25
        + fair_trial_denial_score * 0.25
        + prisoner_of_conscience_score * 0.20,
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
        estimated_political_prisoner_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "arbitrary_detention_score": s1,
            "torture_in_detention_score": s2,
            "fair_trial_denial_score": s3,
            "prisoner_of_conscience_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_political_prisoner_index": estimated_political_prisoner_index,
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
