#!/usr/bin/env python3
"""CaelumSwarm™ — Lead Paint Manufacturing Worker Rights Engine (Wave 301)

Domaine : exposition au plomb des travailleurs fabriquant des peintures au plomb
Régions  : Bangladesh, Inde, Pakistan, Afrique — petites usines non réglementées,
           saturnisme professionnel, absence de protections individuelles.
"""
import json, statistics

ENTITIES = [
    ("LPM-001", 99, 97, 95, 93),
    ("LPM-002", 93, 90, 88, 86),
    ("LPM-003", 85, 82, 80, 78),
    ("LPM-004", 80, 77, 75, 73),
    ("LPM-005", 61, 58, 56, 54),
    ("LPM-006", 51, 48, 46, 44),
    ("LPM-007", 32, 29, 27, 25),
    ("LPM-008", 13, 11, 9, 7),
]
WEIGHTS = (0.30, 0.25, 0.25, 0.20)
THRESHOLDS = {"critique": 60, "élevé": 40, "modéré": 20}


def classify(score):
    if score >= THRESHOLDS["critique"]:
        return "critique"
    if score >= THRESHOLDS["élevé"]:
        return "élevé"
    if score >= THRESHOLDS["modéré"]:
        return "modéré"
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
            "estimated_lead_paint_manufacturing_worker_index": round(composite / 100 * 10, 2),
        })
    avg = statistics.mean(r["composite_score"] for r in results)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1
    return {
        "entities": results,
        "avg_composite": round(avg, 2),
        "distribution": distribution,
    }


if __name__ == "__main__":
    output = compute()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    avg = output["avg_composite"]
    dist = output["distribution"]
    assert avg >= 60, f"avg_composite trop bas: {avg}"
    assert dist.get("critique", 0) == 4
    assert dist.get("élevé", 0) == 2
    assert dist.get("modéré", 0) == 1
    assert dist.get("faible", 0) == 1
    print("✓ Assertions passées")
