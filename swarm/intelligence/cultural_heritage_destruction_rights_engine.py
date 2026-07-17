"""
Cultural Heritage Destruction Rights Engine — Wave 126
Domaine : Destruction patrimoine culturel et droits identitaires
Distribution cible : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "CHD-001",
        "name": "Syrie/ISIS",
        "description": "Palmyre Détruite 2015, Mossoul Bibliothèque Brûlée, 100K Objets Pillés, Financement Artefacts",
        "deliberate_heritage_destruction_conflict_score": 97,
        "cultural_property_looting_trafficking_score": 93,
        "minority_cultural_expression_suppression_score": 88,
        "restitution_reparation_accountability_gap_score": 91,
    },
    {
        "id": "CHD-002",
        "name": "Mali/Tombouctou",
        "description": "Manuscrits Islamiques Brûlés 2012, Mausolées Détruits Ansar Dine, CPI Première Condamnation 2016",
        "deliberate_heritage_destruction_conflict_score": 89,
        "cultural_property_looting_trafficking_score": 85,
        "minority_cultural_expression_suppression_score": 83,
        "restitution_reparation_accountability_gap_score": 87,
    },
    {
        "id": "CHD-003",
        "name": "Afghanistan/Taliban",
        "description": "Bouddhas Bamiyan 2001, Musée Kaboul Pillé, Politique Culturelle 2.0 Femmes Disparaissent Peintures",
        "deliberate_heritage_destruction_conflict_score": 86,
        "cultural_property_looting_trafficking_score": 82,
        "minority_cultural_expression_suppression_score": 84,
        "restitution_reparation_accountability_gap_score": 84,
    },
    {
        "id": "CHD-004",
        "name": "Irak/Pillage 2003",
        "description": "Musée Bagdad 15K Objets Volés, US Forces Inaction, Réseau Trafic International Christie's",
        "deliberate_heritage_destruction_conflict_score": 83,
        "cultural_property_looting_trafficking_score": 85,
        "minority_cultural_expression_suppression_score": 79,
        "restitution_reparation_accountability_gap_score": 81,
    },
    {
        "id": "CHD-005",
        "name": "Chine/Tibet",
        "description": "Monastères Dégradés, Langues Tibétaines Réduites Scolarisation, Bouddhas Remplacés Xi Jinping Images",
        "deliberate_heritage_destruction_conflict_score": 55,
        "cultural_property_looting_trafficking_score": 52,
        "minority_cultural_expression_suppression_score": 57,
        "restitution_reparation_accountability_gap_score": 49,
    },
    {
        "id": "CHD-006",
        "name": "Éthiopie/Guerre Tigré",
        "description": "Aksoum Obelisco Zone Conflit, Patrimoine UNESCO Non Protégé, Pillage Armées",
        "deliberate_heritage_destruction_conflict_score": 51,
        "cultural_property_looting_trafficking_score": 48,
        "minority_cultural_expression_suppression_score": 53,
        "restitution_reparation_accountability_gap_score": 45,
    },
    {
        "id": "CHD-007",
        "name": "UNESCO",
        "description": "Convention 1954 Haye Biens Culturels, 2nd Protocole 1999, Protocole Additionnel, Application Insuffisante CPI",
        "deliberate_heritage_destruction_conflict_score": 27,
        "cultural_property_looting_trafficking_score": 24,
        "minority_cultural_expression_suppression_score": 26,
        "restitution_reparation_accountability_gap_score": 22,
    },
    {
        "id": "CHD-008",
        "name": "France/Musée Quai Branly",
        "description": "Restitutions Bénin 2021, Modèle Législatif Biens Culturels, Processus Consultatif",
        "deliberate_heritage_destruction_conflict_score": 6,
        "cultural_property_looting_trafficking_score": 5,
        "minority_cultural_expression_suppression_score": 5,
        "restitution_reparation_accountability_gap_score": 4,
    },
]

WEIGHTS = {
    "deliberate_heritage_destruction_conflict_score": 0.30,
    "cultural_property_looting_trafficking_score": 0.25,
    "minority_cultural_expression_suppression_score": 0.25,
    "restitution_reparation_accountability_gap_score": 0.20,
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
        estimated_cultural_heritage_destruction_rights_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": composite_score,
            "level": level,
            "estimated_cultural_heritage_destruction_rights_index": estimated_cultural_heritage_destruction_rights_index,
            "sub_scores": {
                "deliberate_heritage_destruction_conflict_score": entity["deliberate_heritage_destruction_conflict_score"],
                "cultural_property_looting_trafficking_score": entity["cultural_property_looting_trafficking_score"],
                "minority_cultural_expression_suppression_score": entity["minority_cultural_expression_suppression_score"],
                "restitution_reparation_accountability_gap_score": entity["restitution_reparation_accountability_gap_score"],
            },
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    output = {
        "engine": "cultural_heritage_destruction_rights_engine",
        "domain": "Destruction patrimoine culturel et droits identitaires",
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
