"""
Wave 179 — Modern Slavery & Forced Labor Contemporary Engine
Domain: Esclavage Moderne & Travail Forcé Contemporain
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import math
from datetime import datetime

ENTITIES = [
    {"id": "MSFL-001", "name": "Corée du Nord/Travail Forcé Étatique — 2.6M Travailleurs Forcés Camps Kwanliso Exportés Chine Russie", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"id": "MSFL-002", "name": "Érythrée/Service National Indéfini — Conscription Forcée Vie Entière Salaire $30/Mois Fuite Criminel", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"id": "MSFL-003", "name": "Mauritanie/Esclavage Héréditaire — 90 000 Esclaves Haratin Nés Esclavage Criminalisation 2007 Impunité", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"id": "MSFL-004", "name": "Inde/Travail Bonded — 18M Travailleurs Endettés Agriculture Briques Carrières Caste Dalits", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"id": "MSFL-005", "name": "Qatar/Kafala Mondial — 2M Travailleurs Migrants Passeport Confisqué Réforme 2021 Partielle FIFA", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"id": "MSFL-006", "name": "UAE/Kafala Construction — 500 000 Travailleurs Domestiques Exclus Labour Law Abus Dénoncés", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"id": "MSFL-007", "name": "Brésil/Trabalho Escravo — Opération Liberdade 3 000 Libérés/An Agriculture Textile Liste Suja", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"id": "MSFL-008", "name": "Portugal/Plan Anti-Traite — Décriminalisation Victimes Accès Justice Réseau Support ONG", "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7}
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
