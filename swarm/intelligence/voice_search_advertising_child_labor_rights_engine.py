#!/usr/bin/env python3
"""CaelumSwarm™ — Voice Search Advertising Child Labor Rights Engine (Wave 344)"""
import json, statistics

ENTITIES = [
    ("Amazon Alexa Ads", 99, 97, 95, 93),
    ("Google Assistant Ads", 93, 90, 88, 86),
    ("Apple Siri Ads", 85, 82, 80, 78),
    ("Fabricants smart speakers", 80, 77, 75, 73),
    ("Agences SEO vocal", 61, 58, 56, 54),
    ("Plateformes podcasts ads", 51, 48, 46, 44),
    ("Fournisseurs NLP", 32, 29, 27, 25),
    ("Développeurs skills/actions", 13, 11, 9, 7),
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
            "estimated_voice_search_advertising_index": round(composite / 100 * 10, 2),
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
