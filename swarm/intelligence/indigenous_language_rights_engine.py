#!/usr/bin/env python3
"""
Indigenous Language Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Indigenous Language Rights Engine Agent"
ACCENT = "#166534"

ENTITIES = [
    # (id, language_extinction_rate_score, education_language_suppression_score, official_language_exclusion_score, cultural_transmission_gap_score)
    ("ILR-001", 99, 98, 97, 95),
    ("ILR-002", 93, 91, 89, 87),
    ("ILR-003", 85, 83, 81, 79),
    ("ILR-004", 78, 76, 74, 72),
    ("ILR-005", 59, 57, 55, 53),
    ("ILR-006", 52, 50, 48, 46),
    ("ILR-007", 32, 30, 28, 26),
    ("ILR-008", 10,  8,  7,  6),
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
        estimated_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "language_extinction_rate_score": s1,
            "education_language_suppression_score": s2,
            "official_language_exclusion_score": s3,
            "cultural_transmission_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_indigenous_language_index": estimated_index,
        })

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] | estimated_indigenous_language_index={r['estimated_indigenous_language_index']}")

    return results


if __name__ == "__main__":
    run_engine()
