#!/usr/bin/env python3
"""CaelumSwarm™ — Accès aux technologies d'assistance pour aveugles & droits à un financement suffisant pour les lecteurs d'écran et équipements Braille (Wave 1257)

Personnes aveugles ou malvoyantes incapables d'obtenir le financement pour des technologies d'assistance essentielles à l'emploi et l'éducation.
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("BATA-001", 99, 97, 95, 93),
    ("BATA-002", 93, 90, 88, 86),
    ("BATA-003", 85, 82, 80, 78),
    ("BATA-004", 80, 77, 75, 73),
    ("BATA-005", 61, 58, 56, 54),
    ("BATA-006", 51, 48, 46, 44),
    ("BATA-007", 32, 29, 27, 25),
    ("BATA-008", 13, 11, 9, 7),
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
            "estimated_blind_assistive_tech_index": round(composite / 100 * 10, 2),
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
    print("✓ Assertions passées — Wave 1257 Accès aux technologies d'assistance pour aveugles & droits à un financement suffisant pour les lecteurs d'écran et équipements Braille OK")
