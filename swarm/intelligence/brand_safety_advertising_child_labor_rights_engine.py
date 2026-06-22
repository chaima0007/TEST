#!/usr/bin/env python3
"""CaelumSwarm™ — Brand Safety Advertising Child Labor Rights Engine (Wave 349)"""
import json, statistics

ENTITIES = [
    ("DoubleVerify Brand Safety Suite", 99, 97, 95, 93),
    ("Integral Ad Science Brand Safety", 93, 90, 88, 86),
    ("HUMAN Security Ad Verification", 85, 82, 80, 78),
    ("White Ops Brand Protection", 80, 77, 75, 73),
    ("Oracle Moat Brand Safety Analytics", 61, 58, 56, 54),
    ("Pixalate Brand Safety Platform", 51, 48, 46, 44),
    ("Adalytics Brand Safety Research", 32, 29, 27, 25),
    ("GARM Global Alliance for Responsible Media", 13, 11, 9, 7),
]
WEIGHTS = (0.30, 0.25, 0.25, 0.20)
THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}

def classify(score):
    if score >= THRESHOLDS["critique"]: return "critique"
    if score >= THRESHOLDS["élevé"]: return "élevé"
    if score >= THRESHOLDS["modéré"]: return "modéré"
    return "faible"

def compute():
    results = []
    for entity in ENTITIES:
        eid, *subs = entity
        composite = sum(s * w for s, w in zip(subs, WEIGHTS))
        results.append({
            "entity": eid,
            "composite_score": round(composite, 2),
            "risk_level": classify(composite),
            "estimated_brand_safety_advertising_index": round(composite / 100 * 10, 2),
        })
    avg = statistics.mean(r["composite_score"] for r in results)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1
    return {"entities": results, "avg_composite": round(avg, 2), "distribution": distribution}

if __name__ == "__main__":
    output = compute()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    avg = output["avg_composite"]
    dist = output["distribution"]
    assert avg >= 60
    assert dist.get("critique", 0) == 4
    assert dist.get("élevé", 0) == 2
    assert dist.get("modéré", 0) == 1
    assert dist.get("faible", 0) == 1
    print("✓ Assertions passées")
