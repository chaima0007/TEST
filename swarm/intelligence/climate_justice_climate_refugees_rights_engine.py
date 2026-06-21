"""
Wave 179 — Climate Justice & Climate Refugees Rights Engine
Domain: Justice Climatique & Droits des Réfugiés Climatiques
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from datetime import datetime

ENTITIES = [
    {
        "id": "CJR-001",
        "name": "Bangladesh/Cyclones Déplacement — 13M Déplacés Climatiques 2050 Delta Submergé Chars Flottants Adaption",
        "sub1": 96,
        "sub2": 94,
        "sub3": 92,
        "sub4": 90,
    },
    {
        "id": "CJR-002",
        "name": "Tuvalu/Disparition Totale — Nation Insulaire 11 000 Habitants Submersion 2050 Accord NZ Migration Dignité",
        "sub1": 92,
        "sub2": 90,
        "sub3": 88,
        "sub4": 86,
    },
    {
        "id": "CJR-003",
        "name": "Pakistan/Inondations 2022 — 33M Affectés 1/3 Pays Sous Eau Pertes $30Mds Compensation Nulle Pollueurs",
        "sub1": 84,
        "sub2": 82,
        "sub3": 80,
        "sub4": 78,
    },
    {
        "id": "CJR-004",
        "name": "Somalie/Sécheresse Conflit — 7.8M Insécurité Alimentaire Déplacement Triple Nexus Conflit-Climat-Faim",
        "sub1": 78,
        "sub2": 76,
        "sub3": 74,
        "sub4": 72,
    },
    {
        "id": "CJR-005",
        "name": "Philippines/Yolanda Typhon — 6 300 Morts 4M Déplacés Reconstruction Inégale Droit Reconstruction Refusé",
        "sub1": 62,
        "sub2": 58,
        "sub3": 56,
        "sub4": 54,
    },
    {
        "id": "CJR-006",
        "name": "Mozambique/Idai Cyclone — 3M Affectés 2019 Reconstruction Lente Justice Climatique Procès Énergéticiens",
        "sub1": 54,
        "sub2": 50,
        "sub3": 48,
        "sub4": 46,
    },
    {
        "id": "CJR-007",
        "name": "USA/Puerto Rico Maria — $90Mds Dégâts Réponse Fédérale Discriminatoire Lenteur Reconstruction",
        "sub1": 38,
        "sub2": 34,
        "sub3": 32,
        "sub4": 28,
    },
    {
        "id": "CJR-008",
        "name": "Allemagne/Klimaseniorinnen — Cour Européenne DH Obligation Climatique États Modèle Litiges Stratégiques",
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

    estimated_climate_justice_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_climate_justice_index": estimated_climate_justice_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Climate Justice & Climate Refugees Rights Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_climate_justice_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "climate-justice-climate-refugees-rights-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
