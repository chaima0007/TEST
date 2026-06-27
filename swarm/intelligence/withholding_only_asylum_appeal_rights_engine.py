#!/usr/bin/env python3
"""CaelumSwarm™ — Appels des cas de withholding of removal uniquement & droits des personnes dont la demande d'asile a été refusée à plaider le retrait différé (Wave 1303)

Demandeurs d'asile déboutés non expulsables vers leur pays d'origine en raison de risques de torture mais sans statut légal permanent ni voie d'appel.
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("GNIN-001", 99, 97, 95, 93),
    ("GNIN-002", 93, 90, 88, 86),
    ("GNIN-003", 85, 82, 80, 78),
    ("GNIN-004", 80, 77, 75, 73),
    ("GNIN-005", 61, 58, 56, 54),
    ("GNIN-006", 51, 48, 46, 44),
    ("GNIN-007", 32, 29, 27, 25),
    ("GNIN-008", 13, 11, 9, 7),
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
            "estimated_withholding_appeal_index": round(composite / 100 * 10, 2),
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
    print("✓ Assertions passées — Wave 1303 Appels des cas de withholding of removal uniquement & droits des personnes dont la demande d'asile a été refusée à plaider le retrait différé OK")
