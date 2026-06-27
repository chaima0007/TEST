#!/usr/bin/env python3
"""CaelumSwarm™ — Limitation du nombre de demandes d'asile aux frontières & droits des demandeurs à présenter leur demande aux points d'entrée sans refoulement ni listes d'attente illégales (Wave 1358)

Demandeurs d'asile refoulés aux points d'entrée officiels par des pratiques de limitation quotidienne les contraignant à attendre dans des conditions dangereuses côté mexicain.
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("BAMT-001", 99, 97, 95, 93),
    ("BAMT-002", 93, 90, 88, 86),
    ("BAMT-003", 85, 82, 80, 78),
    ("BAMT-004", 80, 77, 75, 73),
    ("BAMT-005", 61, 58, 56, 54),
    ("BAMT-006", 51, 48, 46, 44),
    ("BAMT-007", 32, 29, 27, 25),
    ("BAMT-008", 13, 11, 9, 7),
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
            "estimated_border_asylum_metering_index": round(composite / 100 * 10, 2),
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
    print(f"\navg_composite = {avg}")
    print(f"distribution = {dist}")
    assert avg >= 60, f"avg {avg} < 60!"
    assert dist.get("critique", 0) == 4, f"critique={dist.get('critique',0)} != 4"
    assert dist.get("élevé", 0) == 2, f"élevé={dist.get('élevé',0)} != 2"
    assert dist.get("modéré", 0) == 1, f"modéré={dist.get('modéré',0)} != 1"
    assert dist.get("faible", 0) == 1, f"faible={dist.get('faible',0)} != 1"
    print("✓ Assertions passées — Wave 1358 Limitation du nombre de demandes d'asile aux frontières & droits des demandeurs à présenter leur demande aux points d'entrée sans refoulement ni listes d'attente illégales OK")
