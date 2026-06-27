#!/usr/bin/env python3
"""
Speech Surveillance Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Speech Surveillance Rights Engine Agent"

ENTITIES = [
    ("SSR-001", 98, 95, 93, 91),
    ("SSR-002", 91, 88, 86, 84),
    ("SSR-003", 83, 80, 78, 76),
    ("SSR-004", 75, 73, 70, 68),
    ("SSR-005", 56, 53, 51, 49),
    ("SSR-006", 48, 46, 44, 42),
    ("SSR-007", 28, 26, 24, 22),
    ("SSR-008", 8, 6, 5, 4),
]

def calculate_composite(s1, s2, s3, s4):
    return round(s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20, 2)

def classify_risk(score):
    if score >= 60: return "critique"
    elif score >= 40: return "élevé"
    elif score >= 20: return "modéré"
    return "faible"

def run_engine():
    results = []
    for (eid, s1, s2, s3, s4) in ENTITIES:
        composite = calculate_composite(s1, s2, s3, s4)
        risk = classify_risk(composite)
        estimated_speech_surveillance_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "online_speech_monitoring_score": s1,
            "journalist_surveillance_score": s2,
            "political_speech_suppression_score": s3,
            "whistleblower_tracking_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_speech_surveillance_index": estimated_speech_surveillance_index
        })
    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results: dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}]")
    return results

if __name__ == "__main__":
    run_engine()
