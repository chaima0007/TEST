#!/usr/bin/env python3
"""
Wave 185 — Mental Health Detention & Psychiatric Rights Engine
Caelum Partners · Swarm Intelligence Layer
"""

import json
from datetime import datetime

DOMAIN = "mental-health-detention-psychiatric-rights-engine"
ACCENT = "#0891b2"

entities_raw = [
    {
        "id": "MHD-001",
        "name": "Russie/Psychiatrie Punitive Héritée — Opposants Internés, Psikhushka Modernisé",
        "sub1": 93, "sub2": 91, "sub3": 92, "sub4": 91,
    },
    {
        "id": "MHD-002",
        "name": "Chine/Ankang Centres Détention Psychiatrique — Dissidents Pétitionnaires Internés",
        "sub1": 89, "sub2": 87, "sub3": 88, "sub4": 87,
    },
    {
        "id": "MHD-003",
        "name": "Indonésie/Pasung Enchaînement Malades Mentaux — 18 000 Cas Documentés, Pratique Traditionnelle",
        "sub1": 85, "sub2": 83, "sub3": 84, "sub4": 82,
    },
    {
        "id": "MHD-004",
        "name": "Nigeria/Prayer Camps Détention Religieuse — 700 000 Sans Soins Psychiatriques",
        "sub1": 80, "sub2": 78, "sub3": 79, "sub4": 77,
    },
    {
        "id": "MHD-005",
        "name": "USA/Psychiatrisation Carcérale — 2M Détenus Troubles Mentaux, Soins Insuffisants",
        "sub1": 55, "sub2": 53, "sub3": 54, "sub4": 52,
    },
    {
        "id": "MHD-006",
        "name": "France/Hospitalisation Sans Consentement — 92 000/An, Contrôle Judiciaire Insuffisant",
        "sub1": 47, "sub2": 45, "sub3": 46, "sub4": 44,
    },
    {
        "id": "MHD-007",
        "name": "UK/Mental Health Act Review 2022 — Réforme En Cours, Disparités Raciales",
        "sub1": 28, "sub2": 26, "sub3": 27, "sub4": 25,
    },
    {
        "id": "MHD-008",
        "name": "Finlande/Psychiatrie Ouverte Tornio — Modèle Open Dialogue, Internement Minimal",
        "sub1": 9, "sub2": 7, "sub3": 8, "sub4": 7,
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
    estimated_mental_health_rights_index = round(composite / 100 * 10, 2)
    return {
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_mental_health_rights_index": estimated_mental_health_rights_index,
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
