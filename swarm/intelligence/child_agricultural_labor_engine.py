"""Child Agricultural Labor Engine — CaelumSwarm™ Wave 195"""

import json

DOMAIN = "child_agricultural_labor"
PREFIX = "CAL"
ACCENT_COLOR = "#ea580c"  # orange brûlé

ENTITIES = [
    {
        "id": "CAL_001",
        "name": "Nestlé SA",
        "country": "CH/CI",
        "sector": "Food & Beverage",
        "child_labor_prevalence_score": 90,
        "hazardous_conditions_score": 88,
        "education_access_denial_score": 86,
        "remediation_effort_score": 82,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Cacao Côte d'Ivoire — 1.56M enfants dans chaîne cacao"
    },
    {
        "id": "CAL_002",
        "name": "Cargill Incorporated",
        "country": "US/BR",
        "sector": "Agribusiness",
        "child_labor_prevalence_score": 88,
        "hazardous_conditions_score": 85,
        "education_access_denial_score": 84,
        "remediation_effort_score": 81,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Tabac Zimbabwe & canne à sucre Brésil — travail enfants non déclaré"
    },
    {
        "id": "CAL_003",
        "name": "Barry Callebaut AG",
        "country": "CH/GH",
        "sector": "Chocolate & Cocoa",
        "child_labor_prevalence_score": 86,
        "hazardous_conditions_score": 83,
        "education_access_denial_score": 82,
        "remediation_effort_score": 79,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Ghana/Côte d'Ivoire — gaps d'audit certifications, sous-déclaration systémique"
    },
    {
        "id": "CAL_004",
        "name": "JDE Peet's NV",
        "country": "NL/KE",
        "sector": "Coffee & Beverages",
        "child_labor_prevalence_score": 84,
        "hazardous_conditions_score": 80,
        "education_access_denial_score": 81,
        "remediation_effort_score": 77,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Café Kenya & Éthiopie — enfants collecteurs de cerises, pas de traçabilité"
    },
    {
        "id": "CAL_005",
        "name": "Thai Union Group PCL",
        "country": "TH",
        "sector": "Seafood Processing",
        "child_labor_prevalence_score": 62,
        "hazardous_conditions_score": 56,
        "education_access_denial_score": 54,
        "remediation_effort_score": 52,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Pêche Thaïlande — mineurs migrants sur bateaux, conditions dangereuses"
    },
    {
        "id": "CAL_006",
        "name": "Sucromiles SA Colombia",
        "country": "CO",
        "sector": "Sugar & Agribusiness",
        "child_labor_prevalence_score": 58,
        "hazardous_conditions_score": 52,
        "education_access_denial_score": 50,
        "remediation_effort_score": 48,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Canne à sucre Valle del Cauca — enfants coupeurs exposés aux machettes et chaleur"
    },
    {
        "id": "CAL_007",
        "name": "Rainforest Alliance",
        "country": "US/INT",
        "sector": "Certification Body",
        "child_labor_prevalence_score": 34,
        "hazardous_conditions_score": 30,
        "education_access_denial_score": 29,
        "remediation_effort_score": 28,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Certification partielle — lacunes vérification terrain, couverture insuffisante chaîne"
    },
    {
        "id": "CAL_008",
        "name": "Fairtrade Foundation",
        "country": "GB/INT",
        "sector": "Fair Trade Certification",
        "child_labor_prevalence_score": 16,
        "hazardous_conditions_score": 14,
        "education_access_denial_score": 14,
        "remediation_effort_score": 14,
        "composite_score": 0,
        "severity": "",
        "estimated_child_agricultural_labor_index": 0,
        "key_violation": "Meilleure pratique sectorielle — standards éducation & protection enfance intégrés"
    },
]


def calculate_composite(entity):
    return round(
        entity["child_labor_prevalence_score"] * 0.30 +
        entity["hazardous_conditions_score"] * 0.25 +
        entity["education_access_denial_score"] * 0.25 +
        entity["remediation_effort_score"] * 0.20,
        2
    )


def classify_severity(score):
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    return "faible"


def run_engine():
    results = []
    for entity in ENTITIES:
        composite = calculate_composite(entity)
        entity["composite_score"] = composite
        entity["severity"] = classify_severity(composite)
        entity["estimated_child_agricultural_labor_index"] = round(composite / 100 * 10, 2)
        results.append(entity)

    severities = [e["severity"] for e in results]
    avg = round(sum(e["composite_score"] for e in results) / len(results), 2)

    output = {
        "engine": "child_agricultural_labor_engine",
        "domain": DOMAIN,
        "wave": 195,
        "accent_color": ACCENT_COLOR,
        "entities": results,
        "summary": {
            "total_entities": 8,
            "critique": severities.count("critique"),
            "élevé": severities.count("élevé"),
            "modéré": severities.count("modéré"),
            "faible": severities.count("faible"),
            "avg_composite": avg,
            "distribution_valid": (
                severities.count("critique") == 4
                and severities.count("élevé") == 2
                and severities.count("modéré") == 1
                and severities.count("faible") == 1
            )
        }
    }
    return output


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    s = result["summary"]
    print(f"\n=== CHILD AGRICULTURAL LABOR ENGINE ===")
    print(f"Distribution: {s['critique']}c/{s['élevé']}é/{s['modéré']}m/{s['faible']}f — Valid: {s['distribution_valid']}")
    print(f"avg_composite: {s['avg_composite']}")
    for e in result["entities"]:
        print(f"  [{e['severity'].upper():8}] {e['name']:<30} composite={e['composite_score']} index={e['estimated_child_agricultural_labor_index']}")
