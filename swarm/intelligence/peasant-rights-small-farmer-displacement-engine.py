#!/usr/bin/env python3
"""
Wave 185 — Peasant Rights & Small Farmer Displacement Engine
Caelum Partners · Swarm Intelligence Layer
"""

import json
from datetime import datetime

DOMAIN = "peasant-rights-small-farmer-displacement-engine"
ACCENT = "#16a34a"

entities_raw = [
    {
        "id": "PRF-001",
        "name": "Inde/Suicides Agriculteurs — 300 000 Depuis 1995, Dettes Monsanto, Lois Farm Acts Abrogées",
        "sub1": 94, "sub2": 92, "sub3": 93, "sub4": 92,
    },
    {
        "id": "PRF-002",
        "name": "Brésil/Amazonie Agribusiness — MST Paysans Tués, Déforestation Droits Territoriaux",
        "sub1": 88, "sub2": 86, "sub3": 87, "sub4": 85,
    },
    {
        "id": "PRF-003",
        "name": "Honduras/Paysans Palmier Huile — Berta Cáceres Assassinée, Défenseurs Terres Criminalisés",
        "sub1": 85, "sub2": 83, "sub3": 84, "sub4": 82,
    },
    {
        "id": "PRF-004",
        "name": "Éthiopie/Villagisation Forcée — 1.5M Déplacés Agro-Industrie Étrangère",
        "sub1": 81, "sub2": 79, "sub3": 80, "sub4": 78,
    },
    {
        "id": "PRF-005",
        "name": "Philippines/CARP Non-Appliqué — Réforme Agraire 1988 Bloquée, Landlordisme Persistant",
        "sub1": 54, "sub2": 52, "sub3": 53, "sub4": 51,
    },
    {
        "id": "PRF-006",
        "name": "France/Accaparement Terres Agricoles — Foncier Spéculatif, Jeunes Agriculteurs Exclus",
        "sub1": 46, "sub2": 44, "sub3": 45, "sub4": 43,
    },
    {
        "id": "PRF-007",
        "name": "ONU/UNDROP 2018 — Déclaration Droits Paysans, 121 États Votes Pour, Application Partielle",
        "sub1": 26, "sub2": 24, "sub3": 25, "sub4": 23,
    },
    {
        "id": "PRF-008",
        "name": "Bolivia/Révolution Agraire Evo Morales — Redistribution 6M Ha, Droits Constitutionnels",
        "sub1": 10, "sub2": 8, "sub3": 9, "sub4": 7,
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
    estimated_peasant_rights_index = round(composite / 100 * 10, 2)
    return {
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_peasant_rights_index": estimated_peasant_rights_index,
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
