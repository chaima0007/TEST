#!/usr/bin/env python3
"""CaelumSwarm™ — Périodes d'inscription spéciale ACA & droits des consommateurs à s'inscrire dans les plans Marketplace hors période ouverte lors d'événements déclencheurs valides (Wave 1329)

Consommateurs subissant des changements de vie comme la perte d'emploi ou le mariage ignorant qu'ils ont 60 jours pour s'inscrire à une couverture ACA hors saison.
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("ASEP-001", 99, 97, 95, 93),
    ("ASEP-002", 93, 90, 88, 86),
    ("ASEP-003", 85, 82, 80, 78),
    ("ASEP-004", 80, 77, 75, 73),
    ("ASEP-005", 61, 58, 56, 54),
    ("ASEP-006", 51, 48, 46, 44),
    ("ASEP-007", 32, 29, 27, 25),
    ("ASEP-008", 13, 11, 9, 7),
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
            "estimated_aca_special_enroll_index": round(composite / 100 * 10, 2),
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
    print("✓ Assertions passées — Wave 1329 Périodes d'inscription spéciale ACA & droits des consommateurs à s'inscrire dans les plans Marketplace hors période ouverte lors d'événements déclencheurs valides OK")
