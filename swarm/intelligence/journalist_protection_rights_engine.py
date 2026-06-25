#!/usr/bin/env python3
"""
Journalist Protection Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Journalist Protection Rights Engine Agent"
ACCENT = "#0369a1"

ENTITIES = [
    ("JPR-001", 100, 97, 95, 92),
    ("JPR-002", 93, 90, 88, 86),
    ("JPR-003", 86, 83, 81, 79),
    ("JPR-004", 79, 77, 74, 72),
    ("JPR-005", 61, 58, 56, 54),
    ("JPR-006", 53, 51, 49, 47),
    ("JPR-007", 33, 31, 29, 27),
    ("JPR-008", 13, 11, 10, 9),
]

def calculate_composite(journalist_killing_score, source_protection_failure_score, strategic_lawsuit_abuse_score, press_accreditation_denial_score):
    return round(
        journalist_killing_score * 0.30
        + source_protection_failure_score * 0.25
        + strategic_lawsuit_abuse_score * 0.25
        + press_accreditation_denial_score * 0.20,
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
        estimated_journalist_protection_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "journalist_killing_score": s1,
            "source_protection_failure_score": s2,
            "strategic_lawsuit_abuse_score": s3,
            "press_accreditation_denial_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_journalist_protection_index": estimated_journalist_protection_index,
        })
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] — journalist_protection_index={r['estimated_journalist_protection_index']}")
    return results

if __name__ == "__main__":
    run_engine()
