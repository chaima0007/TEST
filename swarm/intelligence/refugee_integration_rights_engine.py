#!/usr/bin/env python3
"""
Refugee Integration Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Refugee Integration Rights Engine Agent"
ACCENT = "#1e40af"
PREFIX = "RIR"

ENTITIES = [
    ("RIR-001", 98, 97, 96, 92),
    ("RIR-002", 90, 89, 88, 84),
    ("RIR-003", 82, 81, 80, 76),
    ("RIR-004", 74, 73, 72, 68),
    ("RIR-005", 59, 58, 57, 53),
    ("RIR-006", 51, 50, 49, 45),
    ("RIR-007", 32, 31, 30, 26),
    ("RIR-008", 12, 11, 10, 6),
]


def calculate_composite(integration_program_absence_score,
                        language_barrier_exclusion_score,
                        employment_discrimination_refugee_score,
                        housing_segregation_refugee_score):
    return round(
        integration_program_absence_score * 0.30
        + language_barrier_exclusion_score * 0.25
        + employment_discrimination_refugee_score * 0.25
        + housing_segregation_refugee_score * 0.20,
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
        estimated_refugee_integration_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "integration_program_absence_score": s1,
            "language_barrier_exclusion_score": s2,
            "employment_discrimination_refugee_score": s3,
            "housing_segregation_refugee_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_refugee_integration_index": estimated_refugee_integration_index,
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
            f" — estimated_refugee_integration_index={r['estimated_refugee_integration_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
