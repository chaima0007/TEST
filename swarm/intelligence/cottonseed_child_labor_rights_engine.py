#!/usr/bin/env python3
"""CaelumSwarm™ — Cottonseed Child Labor Rights Engine (Wave 299)

Domaine : travail des enfants dans la production de graines de coton hybride
(Inde — Andhra Pradesh, Gujarat, Karnataka — pollinisation manuelle par des enfants,
exposition aux pesticides, privation de scolarité, travail de nuit)
"""
import json, statistics

ENTITIES = [
    # (ID, sub1_child_labor_prevalence, sub2_pesticide_exposure, sub3_school_deprivation, sub4_wage_exploitation)
    ("CSC-001", 99, 97, 95, 93),  # Andhra Pradesh — Kurnool district, enfants 7-14 ans, saison intensive
    ("CSC-002", 93, 90, 88, 86),  # Gujarat — Sabarkantha, pollinisation coton Bt, exposition organophosphorés
    ("CSC-003", 85, 82, 80, 78),  # Karnataka — Raichur district, travail nocturne documenté par HRW
    ("CSC-004", 80, 77, 75, 73),  # Telangana — Warangal, filières semencières multinationales impliquées
    ("CSC-005", 61, 58, 56, 54),  # Maharashtra — Akola, audits tiers partiels, accès école réduit
    ("CSC-006", 51, 48, 46, 44),  # Rajasthan — Barmer, travail saisonnier familial non déclaré
    ("CSC-007", 32, 29, 27, 25),  # Madhya Pradesh — Nimar, programmes NREGA partiellement actifs
    ("CSC-008", 13, 11, 9, 7),    # Haryana — Sirsa, inspection du travail renforcée, ONG présentes
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
            "estimated_cottonseed_child_labor_index": round(composite / 100 * 10, 2),
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
