"""
Wave 180 — Genocide Prevention & Early Warning Engine
Domain: Prévention du Génocide & Alerte Précoce
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from datetime import datetime

ENTITIES = [
    {"name": "Myanmar/Rohingya Génocide — 700 000 Déplacés Bangladesh CIJ Cas Génocide Documenté Armée Tatmadaw Crimes Contre Humanité", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"name": "Soudan/Darfour Récurrence — RSF Retour Violences 2023 El Fasher Assauts Civils ONU Alertes Génocide Imminentes", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"name": "Éthiopie/Tigré — 500 000 Morts Estimés Famine Arme Nettoyage Ethnique Documenté Amnesty HRW Preuves Satellitaires", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"name": "Chine/Ouïghours — Camps Détention 1M+ Stérilisations Forcées Destruction Mosquées ONU Violations Graves Droits", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"name": "RD Congo/Est — Massacres Communautaires Répétés FDLR ADF Groupes Armés Kyvu ONU Alerte Précoce Ignorée", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"name": "Inde/Manipur — Violence Ethnique Kuki-Meitei 2023 220+ Morts Déplacements Massifs Impunité Accusations Nettoyage", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"name": "Rwanda/Mémorial Génocide — Gacaca Tribunaux Réconciliation Modèle Prévention ICGLR Mécanisme Alerte Régional", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"name": "Canada/R2P Doctrine — Responsabilité Protéger ONU 2005 ICISS Rapport Normes Intervention Humanitaire Modèle", "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7}
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

    estimated_genocide_risk_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_genocide_risk_index": estimated_genocide_risk_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Genocide Prevention & Early Warning Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_genocide_risk_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "genocide-prevention-early-warning-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
