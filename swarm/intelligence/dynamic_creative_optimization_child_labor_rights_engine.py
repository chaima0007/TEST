#!/usr/bin/env python3
"""CaelumSwarm™ — Dynamic Creative Optimization Child Labor Rights Engine (Wave 346)"""
import json, statistics

ENTITIES = [
    ("Flashtalking DCO Platform", 99, 97, 95, 93),
    ("Celtra Creative Automation", 93, 90, 88, 86),
    ("Programmatic DSP DCO Engines", 85, 82, 80, 78),
    ("A/B Creative Testing Automation Tools", 80, 77, 75, 73),
    ("Feed-Based Ads Personalization Platforms", 61, 58, 56, 54),
    ("Programmatic Creative Agencies", 51, 48, 46, 44),
    ("AI-Driven Creative Studios", 32, 29, 27, 25),
    ("Creative Analytics & Attribution Vendors", 13, 11, 9, 7),
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
            "estimated_dynamic_creative_optimization_index": round(composite / 100 * 10, 2),
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
