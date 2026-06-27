"""Food Sovereignty Rights Engine — CaelumSwarm™ Wave 213"""
import json

DOMAIN = "food_sovereignty_rights"
PREFIX = "FSR"
ACCENT_COLOR = "#0d2818"

ENTITIES = [
    {
        "id": "FSR-001",
        "name": "Monsanto/Bayer",
        "type": "corporation",
        "seed_monopoly_control_score": 92.0,
        "smallholder_displacement_score": 88.0,
        "gmo_coercion_score": 90.0,
        "food_import_dependency_score": 85.0,
        "description": "Contrôle mondial des semences OGM, brevets empêchant réutilisation, monopole pesticides liant agricultures du Sud",
    },
    {
        "id": "FSR-002",
        "name": "Syngenta",
        "type": "corporation",
        "seed_monopoly_control_score": 87.0,
        "smallholder_displacement_score": 83.0,
        "gmo_coercion_score": 85.0,
        "food_import_dependency_score": 80.0,
        "description": "Patents semences bloquant accès petits agriculteurs, herbicides liés à déplacements communautés rurales",
    },
    {
        "id": "FSR-003",
        "name": "DowDuPont/Corteva",
        "type": "corporation",
        "seed_monopoly_control_score": 84.0,
        "smallholder_displacement_score": 80.0,
        "gmo_coercion_score": 82.0,
        "food_import_dependency_score": 78.0,
        "description": "Fusion agro-chimique géante, pression sur gouvernements pour déréguler OGM, déplacement semences traditionnelles",
    },
    {
        "id": "FSR-004",
        "name": "BASF",
        "type": "corporation",
        "seed_monopoly_control_score": 80.0,
        "smallholder_displacement_score": 78.0,
        "gmo_coercion_score": 79.0,
        "food_import_dependency_score": 76.0,
        "description": "Agro-chimie imposant dépendance aux intrants, lobbying contre réglementations pesticides, impact souveraineté alimentaire",
    },
    {
        "id": "FSR-005",
        "name": "Cargill",
        "type": "corporation",
        "seed_monopoly_control_score": 60.0,
        "smallholder_displacement_score": 57.0,
        "gmo_coercion_score": 55.0,
        "food_import_dependency_score": 63.0,
        "description": "Trading alimentaire mondial concentrant marchés céréaliers, création dépendance importations pays en développement",
    },
    {
        "id": "FSR-006",
        "name": "ADM/Archer Daniels Midland",
        "type": "corporation",
        "seed_monopoly_control_score": 53.0,
        "smallholder_displacement_score": 51.0,
        "gmo_coercion_score": 49.0,
        "food_import_dependency_score": 57.0,
        "description": "Oligopole transformation céréales, pression prix affectant revenus agriculteurs locaux dans pays du Sud",
    },
    {
        "id": "FSR-007",
        "name": "FAO",
        "type": "organisation_internationale",
        "seed_monopoly_control_score": 32.0,
        "smallholder_displacement_score": 34.0,
        "gmo_coercion_score": 29.0,
        "food_import_dependency_score": 36.0,
        "description": "Tente de réguler souveraineté alimentaire mais insuffisant face aux multinationales, politiques souvent non contraignantes",
    },
    {
        "id": "FSR-008",
        "name": "La Via Campesina",
        "type": "mouvement_paysan",
        "seed_monopoly_control_score": 10.0,
        "smallholder_displacement_score": 12.0,
        "gmo_coercion_score": 8.0,
        "food_import_dependency_score": 11.0,
        "description": "Meilleure pratique mondiale droits souveraineté alimentaire, défense semences paysannes, Déclaration ONU 2018",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["seed_monopoly_control_score"] * 0.30
        + entity["smallholder_displacement_score"] * 0.25
        + entity["gmo_coercion_score"] * 0.25
        + entity["food_import_dependency_score"] * 0.20,
        2,
    )


def classify_severity(score: float) -> str:
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    else:
        return "faible"


def run_engine() -> dict:
    results = []
    composite_scores = []
    for entity in ENTITIES:
        composite = calculate_composite(entity)
        severity = classify_severity(composite)
        index = round(composite / 100 * 10, 2)
        composite_scores.append(composite)
        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "type": entity["type"],
            "composite_score": composite,
            "severity": severity,
            "estimated_food_sovereignty_rights_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Food Sovereignty Rights Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 213,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_food_sovereignty_rights_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
