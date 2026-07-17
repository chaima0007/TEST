"""
Prison Privatization Profit Rights Engine — Wave 126
Domaine : Privatisation des prisons et droits des détenus
Distribution cible : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "PPR-001",
        "name": "USA/CCA-CoreCivic",
        "description": "130K Détenus Prisons Privées, Quotas Remplissage 90%, Lobbying Anti-Réforme, ICE Centres",
        "private_prison_profit_incentive_recidivism_score": 95,
        "labor_exploitation_prison_industrial_complex_score": 91,
        "healthcare_denial_private_contractor_score": 89,
        "oversight_accountability_private_facility_gap_score": 87,
    },
    {
        "id": "PPR-002",
        "name": "Australie/Serco",
        "description": "Centre Détention Manus & Nauru, Conditions Dégradantes, Morts Amir Pouyan 2014, Opacité",
        "private_prison_profit_incentive_recidivism_score": 89,
        "labor_exploitation_prison_industrial_complex_score": 85,
        "healthcare_denial_private_contractor_score": 87,
        "oversight_accountability_private_facility_gap_score": 83,
    },
    {
        "id": "PPR-003",
        "name": "UK/G4S Prisons",
        "description": "Esclandre HMP Birmingham 2016, Sous-effectif Chronique, Violences +50%, Contrats Renouvelés",
        "private_prison_profit_incentive_recidivism_score": 85,
        "labor_exploitation_prison_industrial_complex_score": 81,
        "healthcare_denial_private_contractor_score": 83,
        "oversight_accountability_private_facility_gap_score": 79,
    },
    {
        "id": "PPR-004",
        "name": "Israël/Détention Migrants",
        "description": "Holot Centre Fermé, Saharonim Prisons, Asylum Seekers Eritréens/Soudanais Indéfini",
        "private_prison_profit_incentive_recidivism_score": 82,
        "labor_exploitation_prison_industrial_complex_score": 78,
        "healthcare_denial_private_contractor_score": 80,
        "oversight_accountability_private_facility_gap_score": 76,
    },
    {
        "id": "PPR-005",
        "name": "Brésil/PPP Carcéral",
        "description": "Partenariats Public-Privé Prisons, Facções Pénètrent Systèmes, Contrôle Insuffisant",
        "private_prison_profit_incentive_recidivism_score": 55,
        "labor_exploitation_prison_industrial_complex_score": 51,
        "healthcare_denial_private_contractor_score": 53,
        "oversight_accountability_private_facility_gap_score": 49,
    },
    {
        "id": "PPR-006",
        "name": "Afrique du Sud/G4S",
        "description": "Incidents Violences Détenus, Rapport JICS Alarmant, Réforme Lente",
        "private_prison_profit_incentive_recidivism_score": 51,
        "labor_exploitation_prison_industrial_complex_score": 47,
        "healthcare_denial_private_contractor_score": 49,
        "oversight_accountability_private_facility_gap_score": 45,
    },
    {
        "id": "PPR-007",
        "name": "ONU/SMR",
        "description": "Standard Minimum Règles, Principes Tokyo, Application Inégale Prisons Privées/Publiques",
        "private_prison_profit_incentive_recidivism_score": 27,
        "labor_exploitation_prison_industrial_complex_score": 25,
        "healthcare_denial_private_contractor_score": 23,
        "oversight_accountability_private_facility_gap_score": 21,
    },
    {
        "id": "PPR-008",
        "name": "Costa Rica/Public Prisons",
        "description": "Zéro Privatisation, ILANUD Standard, Réhabilitation Publique, Récidive -25%",
        "private_prison_profit_incentive_recidivism_score": 6,
        "labor_exploitation_prison_industrial_complex_score": 4,
        "healthcare_denial_private_contractor_score": 5,
        "oversight_accountability_private_facility_gap_score": 3,
    },
]

WEIGHTS = {
    "private_prison_profit_incentive_recidivism_score": 0.30,
    "labor_exploitation_prison_industrial_complex_score": 0.25,
    "healthcare_denial_private_contractor_score": 0.25,
    "oversight_accountability_private_facility_gap_score": 0.20,
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
        estimated_prison_privatization_profit_rights_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": composite_score,
            "level": level,
            "estimated_prison_privatization_profit_rights_index": estimated_prison_privatization_profit_rights_index,
            "sub_scores": {
                "private_prison_profit_incentive_recidivism_score": entity["private_prison_profit_incentive_recidivism_score"],
                "labor_exploitation_prison_industrial_complex_score": entity["labor_exploitation_prison_industrial_complex_score"],
                "healthcare_denial_private_contractor_score": entity["healthcare_denial_private_contractor_score"],
                "oversight_accountability_private_facility_gap_score": entity["oversight_accountability_private_facility_gap_score"],
            },
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    output = {
        "engine": "prison_privatization_profit_rights_engine",
        "domain": "Privatisation des prisons et droits des détenus",
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
