"""Child Marriage & Labor Engine — CaelumSwarm™ Wave 210"""
import json

DOMAIN = "child_marriage_labor"
PREFIX = "CML"
ACCENT_COLOR = "#0a2540"

ENTITIES = [
    {
        "id": "CML-001",
        "name": "Niger",
        "type": "etat",
        "child_marriage_rate_score": 92.0,
        "child_labor_exploitation_score": 90.0,
        "education_deprivation_score": 89.0,
        "legal_enforcement_gap_score": 91.0,
        "description": "Taux mariage enfants 76% le plus élevé au monde, travail enfants 50%+, accès éducation filles quasi nul zones rurales",
    },
    {
        "id": "CML-002",
        "name": "Tchad",
        "type": "etat",
        "child_marriage_rate_score": 87.0,
        "child_labor_exploitation_score": 85.0,
        "education_deprivation_score": 84.0,
        "legal_enforcement_gap_score": 86.0,
        "description": "Taux mariage enfants 52%, conflit armé aggrave exploitation, capacité légale d'application quasi inexistante",
    },
    {
        "id": "CML-003",
        "name": "République Centrafricaine",
        "type": "etat",
        "child_marriage_rate_score": 84.0,
        "child_labor_exploitation_score": 82.0,
        "education_deprivation_score": 81.0,
        "legal_enforcement_gap_score": 83.0,
        "description": "Taux mariage enfants 52%, conflit prolongé, enfants soldats et exploitation labour dans mines artisanales",
    },
    {
        "id": "CML-004",
        "name": "Mali",
        "type": "etat",
        "child_marriage_rate_score": 82.0,
        "child_labor_exploitation_score": 80.0,
        "education_deprivation_score": 79.0,
        "legal_enforcement_gap_score": 81.0,
        "description": "Taux mariage enfants 54%, crise sécuritaire sahélienne, travail enfants agriculture et orpaillage artisanal",
    },
    {
        "id": "CML-005",
        "name": "Bangladesh",
        "type": "etat",
        "child_marriage_rate_score": 57.0,
        "child_labor_exploitation_score": 55.0,
        "education_deprivation_score": 56.0,
        "legal_enforcement_gap_score": 53.0,
        "description": "Taux mariage enfants 51%, secteur garment emploie enfants, progrès législatifs insuffisamment appliqués",
    },
    {
        "id": "CML-006",
        "name": "Éthiopie",
        "type": "etat",
        "child_marriage_rate_score": 55.0,
        "child_labor_exploitation_score": 53.0,
        "education_deprivation_score": 54.0,
        "legal_enforcement_gap_score": 51.0,
        "description": "Taux mariage enfants 40%, agriculture dominante, conflit Tigray aggrave déscolarisation et exploitation enfants",
    },
    {
        "id": "CML-007",
        "name": "Inde",
        "type": "etat",
        "child_marriage_rate_score": 35.0,
        "child_labor_exploitation_score": 33.0,
        "education_deprivation_score": 32.0,
        "legal_enforcement_gap_score": 31.0,
        "description": "Progrès significatifs loi 2006, taux mariage enfants réduit à 23%, travail enfants diminué mais lacunes application persistantes",
    },
    {
        "id": "CML-008",
        "name": "Brésil",
        "type": "etat",
        "child_marriage_rate_score": 14.0,
        "child_labor_exploitation_score": 12.0,
        "education_deprivation_score": 11.0,
        "legal_enforcement_gap_score": 13.0,
        "description": "Protections légales fortes, loi 2019 interdit mariage avant 16 ans sans exception, Bolsa Familia réduit travail enfants",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["child_marriage_rate_score"] * 0.30
        + entity["child_labor_exploitation_score"] * 0.25
        + entity["education_deprivation_score"] * 0.25
        + entity["legal_enforcement_gap_score"] * 0.20,
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
            "estimated_child_marriage_labor_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Child Marriage & Labor Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 210,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_child_marriage_labor_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
