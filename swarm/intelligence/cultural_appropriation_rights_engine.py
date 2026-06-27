#!/usr/bin/env python3
"""
Cultural Appropriation Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Cultural Appropriation Rights Engine Agent"

ENTITIES = [
    ("CAR-001", 99, 97, 96, 94),
    ("CAR-002", 93, 91, 89, 87),
    ("CAR-003", 85, 83, 81, 79),
    ("CAR-004", 77, 75, 73, 71),
    ("CAR-005", 63, 60, 58, 56),
    ("CAR-006", 52, 49, 47, 45),
    ("CAR-007", 32, 29, 27, 25),
    ("CAR-008", 12, 9, 8, 6),
]

def calculate_composite(indigenous_cultural_theft_score, commercial_exploitation_sacred_score, ip_protection_gap_score, reparation_mechanism_absence_score):
    return round(
        indigenous_cultural_theft_score * 0.30
        + commercial_exploitation_sacred_score * 0.25
        + ip_protection_gap_score * 0.25
        + reparation_mechanism_absence_score * 0.20,
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
        estimated_cultural_appropriation_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "indigenous_cultural_theft_score": s1,
            "commercial_exploitation_sacred_score": s2,
            "ip_protection_gap_score": s3,
            "reparation_mechanism_absence_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_cultural_appropriation_index": estimated_cultural_appropriation_index,
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
            f" — estimated_cultural_appropriation_index={r['estimated_cultural_appropriation_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
