#!/usr/bin/env python3
"""
Digital Authoritarianism Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Digital Authoritarianism Rights Engine Agent"
ACCENT = "#1e3a5f"

ENTITIES = [
    # (id, internet_shutdown_score, social_media_control_score, digital_repression_score, vpn_ban_score)
    ("DAR-001", 99, 98, 97, 95),
    ("DAR-002", 93, 91, 89, 87),
    ("DAR-003", 85, 83, 81, 79),
    ("DAR-004", 78, 76, 74, 72),
    ("DAR-005", 59, 57, 55, 53),
    ("DAR-006", 52, 50, 48, 46),
    ("DAR-007", 32, 30, 28, 26),
    ("DAR-008", 10,  8,  7,  6),
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
            "internet_shutdown_score": s1,
            "social_media_control_score": s2,
            "digital_repression_score": s3,
            "vpn_ban_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_digital_authoritarianism_index": estimated_index,
        })

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] | estimated_digital_authoritarianism_index={r['estimated_digital_authoritarianism_index']}")

    return results


if __name__ == "__main__":
    run_engine()
