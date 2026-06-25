#!/usr/bin/env python3
"""
Neuroethics Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Neuroethics Rights Engine Agent"

ENTITIES = [
    ("NER-001", 99, 97, 95, 93),
    ("NER-002", 93, 90, 88, 86),
    ("NER-003", 85, 82, 80, 78),
    ("NER-004", 80, 77, 75, 73),
    ("NER-005", 61, 58, 56, 54),
    ("NER-006", 51, 48, 46, 44),
    ("NER-007", 32, 29, 27, 25),
    ("NER-008", 13, 11, 9, 7),
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
        estimated_neuroethics_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "brain_data_commodification_score": s1,
            "neurotech_coercion_score": s2,
            "cognitive_autonomy_violation_score": s3,
            "nonconsensual_brain_scanning_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_neuroethics_index": estimated_neuroethics_index
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
