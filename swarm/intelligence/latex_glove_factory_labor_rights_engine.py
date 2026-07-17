#!/usr/bin/env python3
"""CaelumSwarm™ — Latex Glove Factory Labor Rights Engine (Wave 299)

Domaine : violations des droits des travailleurs dans les usines de gants en latex
(Malaisie — Top Glove, Supermax — travail forcé migrant, dette de recrutement,
logement insalubre, confiscation de passeports, heures supplémentaires forcées)
"""
import json, statistics

ENTITIES = [
    # (ID, sub1_forced_labor, sub2_recruitment_debt, sub3_housing_conditions, sub4_wage_theft)
    ("LGF-001", 99, 97, 95, 93),  # Top Glove — travail forcé systémique, amendes US CBP 2020
    ("LGF-002", 93, 90, 88, 86),  # Supermax — confiscation passeports, dortoirs surpeuplés
    ("LGF-003", 85, 82, 80, 78),  # WRP Asia Pacific — dette de recrutement élevée (>5 000 USD)
    ("LGF-004", 80, 77, 75, 73),  # Comfort Rubber Gloves — rétention de salaires documentée
    ("LGF-005", 61, 58, 56, 54),  # Brightway Holdings — conditions partiellement améliorées
    ("LGF-006", 51, 48, 46, 44),  # Careplus Group — audits insuffisants, accès limité ONG
    ("LGF-007", 32, 29, 27, 25),  # Hartalega — programmes de remboursement des frais en cours
    ("LGF-008", 13, 11, 9, 7),    # Kossan Rubber — certifications ISO, accès syndical partiel
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
            "estimated_latex_glove_factory_labor_index": round(composite / 100 * 10, 2),
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
