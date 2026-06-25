"""
Nomadic Pastoralist Peoples Rights Engine — Wave 126
Domaine : Droits des peuples nomades et pastoraux
Distribution cible : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "NPR-001",
        "name": "Sahel/Peuls",
        "description": "Massacres Peuls Mali-Burkina-Niger 2019-2023, Bourgou Accès Bloqué, Armées & Djihadistes Ciblage",
        "territorial_access_denial_sedentarization_score": 94,
        "livestock_land_dispossession_conflict_score": 90,
        "cultural_identity_legal_recognition_gap_score": 88,
        "climate_change_mobility_rights_impact_score": 86,
    },
    {
        "id": "NPR-002",
        "name": "Kenya/Masai",
        "description": "Ngorongoro 2023 Expulsions 100K Masai, Zones Touristiques, Pacte Non-Consulté, Violence Gardes",
        "territorial_access_denial_sedentarization_score": 90,
        "livestock_land_dispossession_conflict_score": 86,
        "cultural_identity_legal_recognition_gap_score": 85,
        "climate_change_mobility_rights_impact_score": 83,
    },
    {
        "id": "NPR-003",
        "name": "Éthiopie/Afar-Somali",
        "description": "Conflits Interethniques Pâturages, Réforme Foncière Sélective, 800K Déplacés 2021",
        "territorial_access_denial_sedentarization_score": 87,
        "livestock_land_dispossession_conflict_score": 83,
        "cultural_identity_legal_recognition_gap_score": 82,
        "climate_change_mobility_rights_impact_score": 80,
    },
    {
        "id": "NPR-004",
        "name": "Mongolie/Herders",
        "description": "Mines Charbon Détruisent Pâturages, Dzud Climatiques, Exode Urbain Forcé Oulan-Bator",
        "territorial_access_denial_sedentarization_score": 83,
        "livestock_land_dispossession_conflict_score": 79,
        "cultural_identity_legal_recognition_gap_score": 78,
        "climate_change_mobility_rights_impact_score": 76,
    },
    {
        "id": "NPR-005",
        "name": "Iran/Bakhtiari",
        "description": "Transhumance Bloquée Frontières Administratives, Saisie Bétail, Modernisation Forcée",
        "territorial_access_denial_sedentarization_score": 56,
        "livestock_land_dispossession_conflict_score": 52,
        "cultural_identity_legal_recognition_gap_score": 51,
        "climate_change_mobility_rights_impact_score": 49,
    },
    {
        "id": "NPR-006",
        "name": "Inde/Gurjars",
        "description": "Forêts Protégées Excluent Pasteurs, Wildlife Protection Act vs Droits Pastoraux, Conflit",
        "territorial_access_denial_sedentarization_score": 52,
        "livestock_land_dispossession_conflict_score": 48,
        "cultural_identity_legal_recognition_gap_score": 47,
        "climate_change_mobility_rights_impact_score": 45,
    },
    {
        "id": "NPR-007",
        "name": "UA/Politique Pastorale",
        "description": "Cadre Politique Pastorale Africain 2010, PFAP, Application Insuffisante États",
        "territorial_access_denial_sedentarization_score": 28,
        "livestock_land_dispossession_conflict_score": 25,
        "cultural_identity_legal_recognition_gap_score": 24,
        "climate_change_mobility_rights_impact_score": 22,
    },
    {
        "id": "NPR-008",
        "name": "Tanzanie/WMA",
        "description": "Wildlife Management Areas Inclusives, Masai Co-gestion Ressources, Modèle Partiel",
        "territorial_access_denial_sedentarization_score": 7,
        "livestock_land_dispossession_conflict_score": 5,
        "cultural_identity_legal_recognition_gap_score": 5,
        "climate_change_mobility_rights_impact_score": 4,
    },
]

WEIGHTS = {
    "territorial_access_denial_sedentarization_score": 0.30,
    "livestock_land_dispossession_conflict_score": 0.25,
    "cultural_identity_legal_recognition_gap_score": 0.25,
    "climate_change_mobility_rights_impact_score": 0.20,
}

THRESHOLDS = {
    "critique": 60,
    "élevé": 40,
    "modéré": 20,
}


def compute_composite(entity: dict) -> float:
    score = 0.0
    for key, weight in WEIGHTS.items():
        score += entity[key] * weight
    return round(score, 2)


def classify(score: float) -> str:
    if score >= THRESHOLDS["critique"]:
        return "critique"
    elif score >= THRESHOLDS["élevé"]:
        return "élevé"
    elif score >= THRESHOLDS["modéré"]:
        return "modéré"
    else:
        return "faible"


def run_engine():
    results = []
    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

    for entity in ENTITIES:
        composite_score = compute_composite(entity)
        level = classify(composite_score)
        distribution[level] += 1
        estimated_nomadic_pastoralist_peoples_rights_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": composite_score,
            "level": level,
            "estimated_nomadic_pastoralist_peoples_rights_index": estimated_nomadic_pastoralist_peoples_rights_index,
            "sub_scores": {
                "territorial_access_denial_sedentarization_score": entity["territorial_access_denial_sedentarization_score"],
                "livestock_land_dispossession_conflict_score": entity["livestock_land_dispossession_conflict_score"],
                "cultural_identity_legal_recognition_gap_score": entity["cultural_identity_legal_recognition_gap_score"],
                "climate_change_mobility_rights_impact_score": entity["climate_change_mobility_rights_impact_score"],
            },
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    output = {
        "engine": "nomadic_pastoralist_peoples_rights_engine",
        "domain": "Droits des peuples nomades et pastoraux",
        "wave": 126,
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\navg_composite: {avg_composite}")
    print(f"Distribution: {distribution}")

    # Validate distribution
    assert distribution["critique"] == 4, f"Expected 4 critique, got {distribution['critique']}"
    assert distribution["élevé"] == 2, f"Expected 2 élevé, got {distribution['élevé']}"
    assert distribution["modéré"] == 1, f"Expected 1 modéré, got {distribution['modéré']}"
    assert distribution["faible"] == 1, f"Expected 1 faible, got {distribution['faible']}"
    print("\nDistribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible ✓")

    return output


if __name__ == "__main__":
    run_engine()
