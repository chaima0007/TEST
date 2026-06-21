"""
Wave 179 — Modern Slavery & Forced Labor Contemporary Engine
Domain: Esclavage Moderne & Travail Forcé Contemporain
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import math
from datetime import datetime

ENTITIES = [
    {
        "id": "MSL-001",
        "name": "Corée du Nord/Travail Forcé Étatique — 2.6M Travailleurs Forcés Camps Kwanliso Exportés Chine Russie",
        "sub1": 96,
        "sub2": 94,
        "sub3": 92,
        "sub4": 90,
    },
    {
        "id": "MSL-002",
        "name": "Érythrée/Service National Indéfini — Conscription Forcée Vie Entière Salaire $30/Mois Fuite Criminel",
        "sub1": 90,
        "sub2": 88,
        "sub3": 86,
        "sub4": 84,
    },
    {
        "id": "MSL-003",
        "name": "Mauritanie/Esclavage Héréditaire — 90 000 Esclaves Haratin Nés Esclavage Criminalisation 2007 Impunité",
        "sub1": 84,
        "sub2": 82,
        "sub3": 80,
        "sub4": 78,
    },
    {
        "id": "MSL-004",
        "name": "Inde/Travail Bonded — 18M Travailleurs Endettés Agriculture Briques Carrières Caste Dalits",
        "sub1": 76,
        "sub2": 74,
        "sub3": 72,
        "sub4": 70,
    },
    {
        "id": "MSL-005",
        "name": "Qatar/Kafala Mondial — 2M Travailleurs Migrants Passeport Confisqué Réforme 2021 Partielle FIFA",
        "sub1": 62,
        "sub2": 58,
        "sub3": 56,
        "sub4": 54,
    },
    {
        "id": "MSL-006",
        "name": "UAE/Kafala Construction — 500 000 Travailleurs Domestiques Exclus Labour Law Abus Dénoncés",
        "sub1": 54,
        "sub2": 50,
        "sub3": 48,
        "sub4": 46,
    },
    {
        "id": "MSL-007",
        "name": "Brésil/Trabalho Escravo — Opération Liberdade 3 000 Libérés/An Agriculture Textile Liste Suja",
        "sub1": 38,
        "sub2": 34,
        "sub3": 32,
        "sub4": 28,
    },
    {
        "id": "MSL-008",
        "name": "Portugal/Plan Anti-Traite — Décriminalisation Victimes Accès Justice Réseau Support ONG",
        "sub1": 18,
        "sub2": 14,
        "sub3": 12,
        "sub4": 10,
    },
]


def compute(entity: dict) -> dict:
    composite = (
        entity["sub1"] * 0.30
        + entity["sub2"] * 0.25
        + entity["sub3"] * 0.25
        + entity["sub4"] * 0.20
    )
    composite = round(composite, 2)

    if composite >= 65:
        risk_level = "critique"
    elif composite >= 45:
        risk_level = "élevé"
    elif composite >= 20:
        risk_level = "modéré"
    else:
        risk_level = "faible"

    estimated_modern_slavery_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_modern_slavery_index": estimated_modern_slavery_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Modern Slavery & Forced Labor Contemporary Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_modern_slavery_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "modern-slavery-forced-labor-contemporary-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
