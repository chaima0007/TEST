#!/usr/bin/env python3
"""CaelumSwarm™ — Dispenses du test de citoyenneté pour les personnes handicapées & droits des candidats à la naturalisation avec handicaps cognitifs à des exemptions ou accommodements de l'examen (Wave 1374)

Candidats à la naturalisation avec handicaps cognitifs ou médicaux se voyant refuser l'exemption d'examen civique et linguistique malgré leur éligibilité au formulaire de dérogation médicale.
Sous-scores : plus le score est élevé, plus le risque est élevé.
"""
import json, statistics

ENTITIES = [
    ("CTDW-001", 99, 97, 95, 93),
    ("CTDW-002", 93, 90, 88, 86),
    ("CTDW-003", 85, 82, 80, 78),
    ("CTDW-004", 80, 77, 75, 73),
    ("CTDW-005", 61, 58, 56, 54),
    ("CTDW-006", 51, 48, 46, 44),
    ("CTDW-007", 32, 29, 27, 25),
    ("CTDW-008", 13, 11, 9, 7),
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
            "estimated_citizenship_test_waiver_index": round(composite / 100 * 10, 2),
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
    print("✓ Assertions passées — Wave 1374 Dispenses du test de citoyenneté pour les personnes handicapées & droits des candidats à la naturalisation avec handicaps cognitifs à des exemptions ou accommodements de l'examen OK")
