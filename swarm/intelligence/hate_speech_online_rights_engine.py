#!/usr/bin/env python3
"""
Hate Speech Online Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Hate Speech Online Rights Engine Agent"

ENTITIES = [
    ("HSO-001", 99, 97, 96, 94),
    ("HSO-002", 93, 91, 89, 87),
    ("HSO-003", 85, 83, 81, 79),
    ("HSO-004", 77, 75, 73, 71),
    ("HSO-005", 63, 60, 58, 56),
    ("HSO-006", 52, 49, 47, 45),
    ("HSO-007", 32, 29, 27, 25),
    ("HSO-008", 12, 9, 8, 6),
]

def calculate_composite(online_incitement_violence_score, platform_moderation_failure_score, minority_targeting_score, legal_accountability_gap_score):
    return round(
        online_incitement_violence_score * 0.30
        + platform_moderation_failure_score * 0.25
        + minority_targeting_score * 0.25
        + legal_accountability_gap_score * 0.20,
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
        estimated_hate_speech_online_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "online_incitement_violence_score": s1,
            "platform_moderation_failure_score": s2,
            "minority_targeting_score": s3,
            "legal_accountability_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_hate_speech_online_index": estimated_hate_speech_online_index,
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
            f" — estimated_hate_speech_online_index={r['estimated_hate_speech_online_index']}"
        )
    return results

if __name__ == "__main__":
    run_engine()
