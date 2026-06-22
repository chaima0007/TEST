"""
Wave 180 — Solitary Confinement & Torture Methods Engine
Domain: Isolement Cellulaire & Méthodes de Torture
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from datetime import datetime

ENTITIES = [
    {"name": "USA/ADX Florence — Supermax Isolement Total 23h/Jour 400+ Détenus Suicide Taux Élevé HRW Torture Psychologique", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Chine/Laojiao Réforme — Éducation Forcée Ouïghours Falun Gong Privation Sommeil Torture Mentale Aveux Contraints", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Russie/SHIZO Punition — Cellules Punitives Isolement Absolu Navalny Décès Conditions Inhumaines CPT Rapport", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "Turquie/Type F Prison — Isolement Cellulaire Individuel Réservé Politiques Kurdes Longue Durée CPT Critique", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "Israël/Incommunicado — Détention Prolongée Sans Contact Gazaouis 2023 Installations Sde Teiman Témoignages Abus", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Égypte/Disparitions Forcées — Détention Incommunicado Opposants Politique 60 000+ Prisonniers Politiques Estimés AI", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "Danemark/Réforme Isolement — Interdiction Isolement Préventif -18 Ans Limite 4 Semaines Adultes Modèle Nordic", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Règles Nelson Mandela ONU — Standard Minimum Traitement Détenus 2015 Révisées Isolement Max 15 Jours Consécutifs", "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7}
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

    estimated_torture_solitary_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_torture_solitary_index": estimated_torture_solitary_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Solitary Confinement & Torture Methods Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_torture_solitary_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "solitary-confinement-torture-methods-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
