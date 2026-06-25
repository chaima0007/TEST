"""
Wave 180 — Child Soldiers & Armed Recruitment (Contemporain) Engine
Domain: Enfants Soldats & Recrutement Armé Contemporain
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from datetime import datetime

ENTITIES = [
    {"id": "CSAR-001", "name": "RD Congo/M23 Recrutement — 3 000+ Enfants Soldats M23 CNDP Kyvu 2023 ONU Rapport Enrôlement Forcé Dès 8 Ans", "sub1": 99, "sub2": 97, "sub3": 95, "sub4": 93},
    {"id": "CSAR-002", "name": "Somalie/Al-Shabaab — 5 000+ Enfants Recrutés Annuellement Suicide Bombing Enfants ONU Cas Documentés UNICEF", "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 86},
    {"id": "CSAR-003", "name": "Soudan/RSF Enfants — Forces Appui Rapide Recrutent Enfants Darfour 2023 12-17 Ans Formation Paramilitaire", "sub1": 85, "sub2": 82, "sub3": 80, "sub4": 78},
    {"id": "CSAR-004", "name": "Yémen/Houthis — 3 500+ Enfants Soldats Houthis ONU Vérifiés Coalition Saoudienne Aussi Documentée UNICEF", "sub1": 80, "sub2": 77, "sub3": 75, "sub4": 73},
    {"id": "CSAR-005", "name": "Myanmar/Tatmadaw — Armée Birmane Recrutement Enfants Persistant Malgré Interdiction CPI Enquêtes 2023", "sub1": 61, "sub2": 58, "sub3": 56, "sub4": 54},
    {"id": "CSAR-006", "name": "Mali/Groupes Armés — JNIM Katiba Macina Recrutement Enfants Sahel 1 200 Cas ONU 2023 Filles Esclavage Sexuel", "sub1": 51, "sub2": 48, "sub3": 46, "sub4": 44},
    {"id": "CSAR-007", "name": "Philippines/Lumad — Enfants Autochtones Lumad Recrutement Contesté NPA Armée Droits Humains Alert", "sub1": 32, "sub2": 29, "sub3": 27, "sub4": 25},
    {"id": "CSAR-008", "name": "Allemagne/Loi Interdiction — Modèle Législatif Stricte Prohibition Recrutement Mineurs Coopération ICC Coalition Stop", "sub1": 13, "sub2": 11, "sub3":  9, "sub4":  7}
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

    estimated_child_soldier_index = round(composite / 100 * 10, 2)

    return {
        "id": entity["id"],
        "name": entity["name"],
        "sub1": entity["sub1"],
        "sub2": entity["sub2"],
        "sub3": entity["sub3"],
        "sub4": entity["sub4"],
        "composite_score": composite,
        "risk_level": risk_level,
        "estimated_child_soldier_index": estimated_child_soldier_index,
    }


def run():
    results = [compute(e) for e in ENTITIES]

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print(f"\n=== Child Soldiers & Armed Recruitment Contemporain Engine ===")
    print(f"Generated: {datetime.utcnow().isoformat()}Z")
    print(f"Avg composite: {avg_composite}")
    print(f"Distribution: {dist}")
    print()
    for r in results:
        print(
            f"  {r['id']} | {r['composite_score']:6.2f} | {r['risk_level']:8} | "
            f"index={r['estimated_child_soldier_index']} | {r['name'][:60]}"
        )

    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")

    return {
        "domain": "child-soldiers-armed-recruitment-contemporain-engine",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "entities": results,
        "avg_composite": avg_composite,
        "risk_distribution": dist,
    }


if __name__ == "__main__":
    run()
