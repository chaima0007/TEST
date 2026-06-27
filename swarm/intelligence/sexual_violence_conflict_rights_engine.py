#!/usr/bin/env python3
"""
Sexual Violence Conflict Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Sexual Violence Conflict Rights Engine Agent"
ACCENT = "#9f1239"

ENTITIES = [
    ("SVC-001", 99, 97, 95, 93),
    ("SVC-002", 93, 91, 89, 87),
    ("SVC-003", 86, 84, 82, 80),
    ("SVC-004", 78, 76, 74, 72),
    ("SVC-005", 61, 59, 57, 55),
    ("SVC-006", 51, 49, 47, 45),
    ("SVC-007", 31, 29, 27, 25),
    ("SVC-008", 11, 9, 7, 5),
]

def calculate_composite(wartime_rape_prevalence_score,
                         survivor_support_gap_score,
                         perpetrator_impunity_score,
                         justice_mechanism_failure_score):
    return round(
        wartime_rape_prevalence_score * 0.30
        + survivor_support_gap_score * 0.25
        + perpetrator_impunity_score * 0.25
        + justice_mechanism_failure_score * 0.20,
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
        estimated_sexual_violence_conflict_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "wartime_rape_prevalence_score": s1,
            "survivor_support_gap_score": s2,
            "perpetrator_impunity_score": s3,
            "justice_mechanism_failure_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_sexual_violence_conflict_index": estimated_sexual_violence_conflict_index,
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
            f" — estimated_sexual_violence_conflict_index={r['estimated_sexual_violence_conflict_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
