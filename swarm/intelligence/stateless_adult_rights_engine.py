#!/usr/bin/env python3
"""
Stateless Adult Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Stateless Adult Rights Engine Agent"
ACCENT = "#374151"

ENTITIES = [
    ("SAR-001", 100, 98, 97, 96),
    ("SAR-002", 95, 93, 91, 89),
    ("SAR-003", 88, 85, 83, 81),
    ("SAR-004", 79, 77, 75, 73),
    ("SAR-005", 58, 55, 53, 51),
    ("SAR-006", 49, 47, 45, 43),
    ("SAR-007", 30, 28, 26, 24),
    ("SAR-008", 10, 8, 7, 5),
]

def calculate_composite(statelessness_documentation_denial_score,
                        civil_registration_exclusion_score,
                        employment_legal_barrier_score,
                        detention_stateless_score):
    return round(
        statelessness_documentation_denial_score * 0.30
        + civil_registration_exclusion_score * 0.25
        + employment_legal_barrier_score * 0.25
        + detention_stateless_score * 0.20,
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
        estimated_stateless_adult_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "statelessness_documentation_denial_score": s1,
            "civil_registration_exclusion_score": s2,
            "employment_legal_barrier_score": s3,
            "detention_stateless_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_stateless_adult_index": estimated_stateless_adult_index,
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
            f"  {r['entity_id']}: {r['composite_score']} "
            f"[{r['risk_level']}] "
            f"estimated_stateless_adult_index={r['estimated_stateless_adult_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
