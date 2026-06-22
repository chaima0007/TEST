#!/usr/bin/env python3
"""
Right to Strike Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Right to Strike Rights Engine Agent"
ACCENT = "#ea580c"

ENTITIES = [
    ("RSS-001", 100, 97, 95, 92),
    ("RSS-002", 93, 90, 88, 86),
    ("RSS-003", 86, 83, 81, 79),
    ("RSS-004", 79, 77, 74, 72),
    ("RSS-005", 61, 58, 56, 54),
    ("RSS-006", 53, 51, 49, 47),
    ("RSS-007", 33, 31, 29, 27),
    ("RSS-008", 13, 11, 10, 9),
]

def calculate_composite(strike_ban_score, essential_services_abuse_score, strike_retaliation_score, collective_action_restriction_score):
    return round(
        strike_ban_score * 0.30
        + essential_services_abuse_score * 0.25
        + strike_retaliation_score * 0.25
        + collective_action_restriction_score * 0.20,
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
        estimated_right_to_strike_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "strike_ban_score": s1,
            "essential_services_abuse_score": s2,
            "strike_retaliation_score": s3,
            "collective_action_restriction_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_right_to_strike_index": estimated_right_to_strike_index,
        })
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] — right_to_strike_index={r['estimated_right_to_strike_index']}")
    return results

if __name__ == "__main__":
    run_engine()
