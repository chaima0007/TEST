#!/usr/bin/env python3
"""
Wave 185 — Intersex Rights & Bodily Integrity Engine
Caelum Partners · Swarm Intelligence Layer
"""

import json
from datetime import datetime

DOMAIN = "intersex-rights-bodily-integrity-engine"
ACCENT = "#7c3aed"

entities_raw = [
    {
        "id": "IRB-001",
        "name": "USA/Chirurgies Intersexes Nourrissons — Pratique Courante Sans Consentement, AAP Réticent",
        "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 92,
    },
    {
        "id": "IRB-002",
        "name": "Allemagne/Interdiction Partielle 2021 — Loi Insuffisante, Exceptions Larges Maintien Pratiques",
        "sub1": 86, "sub2": 84, "sub3": 85, "sub4": 83,
    },
    {
        "id": "IRB-003",
        "name": "Chine/Intersexes Invisibles — Médicalisation Forcée, Zéro Reconnaissance Légale",
        "sub1": 83, "sub2": 81, "sub3": 82, "sub4": 80,
    },
    {
        "id": "IRB-004",
        "name": "Afrique du Sud/Chirurgies Normalisantes — Sport Caster Semenya, CAS vs IAAF Droits Bafoués",
        "sub1": 79, "sub2": 77, "sub3": 78, "sub4": 76,
    },
    {
        "id": "IRB-005",
        "name": "France/Loi Bioéthique 2021 Partielle — Moratoire Non Contraignant, Pratiques Continuent",
        "sub1": 54, "sub2": 51, "sub3": 52, "sub4": 49,
    },
    {
        "id": "IRB-006",
        "name": "Australie/Senate Inquiry 2013 — Recommandations Non Appliquées, États Divergents",
        "sub1": 46, "sub2": 44, "sub3": 45, "sub4": 43,
    },
    {
        "id": "IRB-007",
        "name": "Malte/Loi GIGESC 2015 — Premier Pays Interdiction Totale, Modèle Mondial",
        "sub1": 23, "sub2": 22, "sub3": 21, "sub4": 22,
    },
    {
        "id": "IRB-008",
        "name": "Portugal/Interdiction 2018 Complète — Droits Complets Reconnaissance Légale Genre",
        "sub1": 8, "sub2": 6, "sub3": 7, "sub4": 6,
    },
]


def compute_entity(e):
    composite = (
        e["sub1"] * 0.30
        + e["sub2"] * 0.25
        + e["sub3"] * 0.25
        + e["sub4"] * 0.20
    )
    composite = round(composite, 2)
    if composite >= 60:
        risk_level = "critique"
    elif composite >= 40:
        risk_level = "élevé"
    elif composite >= 20:
        risk_level = "modéré"
    else:
        risk_level = "faible"
    estimated_intersex_rights_index = round(composite / 100 * 10, 2)
    return {
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_intersex_rights_index": estimated_intersex_rights_index,
    }


def main():
    entities = [compute_entity(e) for e in entities_raw]
    distribution = {}
    for ent in entities:
        lvl = ent["risk_level"]
        distribution[lvl] = distribution.get(lvl, 0) + 1

    avg_composite = round(sum(e["composite_score"] for e in entities) / len(entities), 2)

    result = {
        "domain": DOMAIN,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": entities,
        "avg_composite": avg_composite,
        "risk_distribution": distribution,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Validations
    assert distribution.get("critique", 0) == 4, f"Expected 4 critique, got {distribution.get('critique', 0)}"
    assert distribution.get("élevé", 0) == 2, f"Expected 2 élevé, got {distribution.get('élevé', 0)}"
    assert distribution.get("modéré", 0) == 1, f"Expected 1 modéré, got {distribution.get('modéré', 0)}"
    assert distribution.get("faible", 0) == 1, f"Expected 1 faible, got {distribution.get('faible', 0)}"
    print(f"\n✓ avg_composite: {avg_composite}")
    print(f"✓ Distribution: {distribution}")
    print("✓ All assertions passed")


if __name__ == "__main__":
    main()
