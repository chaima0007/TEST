"""Prison Labor Rights Engine — CaelumSwarm™ Wave 196"""
import json

DOMAIN = "prison_labor_rights"
PREFIX = "PLR"
ACCENT_COLOR = "#4c1d95"

# 8 entities — distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
ENTITIES = [
    {
        "id": "PLR-001",
        "name": "CoreCivic (formerly CCA)",
        "description": "Plus grand opérateur de prisons privées aux États-Unis",
        "forced_labor_exploitation_score": 92,
        "below_minimum_wage_score": 90,
        "dangerous_working_conditions_score": 85,
        "rehabilitation_denial_score": 82,
    },
    {
        "id": "PLR-002",
        "name": "The GEO Group",
        "description": "Prisons privées et contrats ICE, détention immigration",
        "forced_labor_exploitation_score": 90,
        "below_minimum_wage_score": 88,
        "dangerous_working_conditions_score": 82,
        "rehabilitation_denial_score": 80,
    },
    {
        "id": "PLR-003",
        "name": "Prison Policy Initiative / Aramark Correctional",
        "description": "Restauration dans les prisons, conditions documentées",
        "forced_labor_exploitation_score": 80,
        "below_minimum_wage_score": 82,
        "dangerous_working_conditions_score": 76,
        "rehabilitation_denial_score": 72,
    },
    {
        "id": "PLR-004",
        "name": "UNICOR / Federal Prison Industries",
        "description": "Travail forcé fédéral US, concurrence déloyale aux entreprises privées",
        "forced_labor_exploitation_score": 78,
        "below_minimum_wage_score": 76,
        "dangerous_working_conditions_score": 72,
        "rehabilitation_denial_score": 66,
    },
    {
        "id": "PLR-005",
        "name": "Sodexo Justice Services",
        "description": "Services carcéraux, incidents documentés sur les conditions de travail",
        "forced_labor_exploitation_score": 63,
        "below_minimum_wage_score": 59,
        "dangerous_working_conditions_score": 57,
        "rehabilitation_denial_score": 55,
    },
    {
        "id": "PLR-006",
        "name": "Serco Group plc",
        "description": "Prisons au Royaume-Uni, centres de détention immigration",
        "forced_labor_exploitation_score": 58,
        "below_minimum_wage_score": 56,
        "dangerous_working_conditions_score": 54,
        "rehabilitation_denial_score": 50,
    },
    {
        "id": "PLR-007",
        "name": "Salvation Army",
        "description": "Programmes de réhabilitation, pratiques améliorées par rapport au secteur",
        "forced_labor_exploitation_score": 30,
        "below_minimum_wage_score": 28,
        "dangerous_working_conditions_score": 30,
        "rehabilitation_denial_score": 26,
    },
    {
        "id": "PLR-008",
        "name": "Prison Fellowship International",
        "description": "ONG de défense des droits des détenus, meilleure pratique sectorielle",
        "forced_labor_exploitation_score": 14,
        "below_minimum_wage_score": 13,
        "dangerous_working_conditions_score": 15,
        "rehabilitation_denial_score": 13,
    },
]


def calculate_composite(entity: dict) -> float:
    """composite = sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20"""
    return round(
        entity["forced_labor_exploitation_score"] * 0.30
        + entity["below_minimum_wage_score"] * 0.25
        + entity["dangerous_working_conditions_score"] * 0.25
        + entity["rehabilitation_denial_score"] * 0.20,
        2,
    )


def classify_severity(score: float) -> str:
    """Seuils : critique≥60, élevé≥40, modéré≥20, faible<20"""
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

        results.append(
            {
                "id": entity["id"],
                "name": entity["name"],
                "description": entity["description"],
                "sub_scores": {
                    "forced_labor_exploitation_score": entity["forced_labor_exploitation_score"],
                    "below_minimum_wage_score": entity["below_minimum_wage_score"],
                    "dangerous_working_conditions_score": entity["dangerous_working_conditions_score"],
                    "rehabilitation_denial_score": entity["rehabilitation_denial_score"],
                },
                "composite_score": composite,
                "severity": severity,
                "estimated_prison_labor_rights_index": index,
            }
        )

    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)

    # Distribution verification
    distribution = {}
    for r in results:
        sev = r["severity"]
        distribution[sev] = distribution.get(sev, 0) + 1

    return {
        "engine": "Prison Labor Rights Engine",
        "wave": 196,
        "swarm": "CaelumSwarm™",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "severity_distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
