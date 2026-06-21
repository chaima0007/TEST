"""
Wave 179 — Food Right & Agribusiness Hunger Engine
Domain: Droit à l'Alimentation & Agro-industrie
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from datetime import datetime

ENTITIES = [
    {
        "id": "FRA-001",
        "name": "Yemen/Famine Guerre — 21M Insécurité Alimentaire Blocus Ports Hodeida ONU Dénonce Armes Saoudiennes",
        "sub1": 96,
        "sub2": 94,
        "sub3": 94,
        "sub4": 92,
    },
    {
        "id": "FRA-002",
        "name": "RD Congo/Faim Chroni — 27M Famine Acute Phase 3+ Conflit Est Déplacement MSF Accès Impossible",
        "sub1": 90,
        "sub2": 88,
        "sub3": 86,
        "sub4": 84,
    },
    {
        "id": "FRA-003",
        "name": "Éthiopie/Tigré Famine Arme — ONU 900 000 Famine 2021 Aide Bloquée Gouvernement Violation Droit International",
        "sub1": 84,
        "sub2": 80,
        "sub3": 78,
        "sub4": 76,
    },
    {
        "id": "FRA-004",
        "name": "Inde/Green Revolution Paradoxe — 189M Sous-Alimentés 3e Rang Mondial GM Corps Brevets Monopoles Semences",
        "sub1": 76,
        "sub2": 72,
        "sub3": 72,
        "sub4": 68,
    },
    {
        "id": "FRA-005",
        "name": "Brésil/Deforestation Soja — 69% Soja Export UE Déforestation Amazonie Peuples Autochtones Déplacés",
        "sub1": 60,
        "sub2": 56,
        "sub3": 54,
        "sub4": 52,
    },
    {
        "id": "FRA-006",
        "name": "USA/Farm Subsidies Big Ag — $20Mds/An Subventions Grandes Firmes Petits Agriculteurs Faillites Semences OGM",
        "sub1": 52,
        "sub2": 48,
        "sub3": 46,
        "sub4": 44,
    },
    {
        "id": "FRA-007",
        "name": "Kenya/Agroécologie — Transition Semences Locales Kounkuey Design Initiative Petits Paysans Résilience",
        "sub1": 34,
        "sub2": 30,
        "sub3": 28,
        "sub4": 24,
    },
    {
        "id": "FRA-008",
        "name": "Via Campesina/Droits Paysans — ONU Déclaration 2018 Semences Autonomie Alimentaire 200M Membres Mondial",
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

    estimated_food_rights_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_food_rights_index": estimated_food_rights_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Food Right & Agribusiness Hunger Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_food_rights_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "food-right-agribusiness-hunger-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
