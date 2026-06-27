"""Toxic Waste Environmental Health Engine — CaelumSwarm™ Wave 196"""
import json

DOMAIN = "toxic_waste_environmental_health"
PREFIX = "TWE"
ACCENT_COLOR = "#b45309"

ENTITIES = [
    {
        "id": "TWE-001",
        "name": "Dow Chemical Company",
        "type": "corporate",
        "toxic_contamination_score": 91,
        "community_health_impact_score": 88,
        "cleanup_liability_evasion_score": 85,
        "regulatory_compliance_failure_score": 82,
        "description": "Contamination PFAS/dioxine, responsabilité Bhopal via Union Carbide, sites Superfund multiples",
    },
    {
        "id": "TWE-002",
        "name": "Chevron Corporation",
        "type": "corporate",
        "toxic_contamination_score": 88,
        "community_health_impact_score": 86,
        "cleanup_liability_evasion_score": 83,
        "regulatory_compliance_failure_score": 78,
        "description": "Lago Agrio Équateur — déversements massifs Texaco/Chevron, 30 milliards USD dommages réclamés",
    },
    {
        "id": "TWE-003",
        "name": "Trafigura Group",
        "type": "corporate",
        "toxic_contamination_score": 86,
        "community_health_impact_score": 83,
        "cleanup_liability_evasion_score": 80,
        "regulatory_compliance_failure_score": 77,
        "description": "Déversement déchets toxiques Abidjan 2006, des milliers de victimes en Côte d'Ivoire",
    },
    {
        "id": "TWE-004",
        "name": "Syngenta AG",
        "type": "corporate",
        "toxic_contamination_score": 82,
        "community_health_impact_score": 79,
        "cleanup_liability_evasion_score": 77,
        "regulatory_compliance_failure_score": 76,
        "description": "Pesticides atrazine — contamination nappe phréatique, perturbateur endocrinien avéré",
    },
    {
        "id": "TWE-005",
        "name": "Veolia Environment",
        "type": "enterprise",
        "toxic_contamination_score": 60,
        "community_health_impact_score": 56,
        "cleanup_liability_evasion_score": 55,
        "regulatory_compliance_failure_score": 54,
        "description": "Gestion déchets industriels, incidents de traitement multiples, controverses contractuelles",
    },
    {
        "id": "TWE-006",
        "name": "Waste Management Inc",
        "type": "enterprise",
        "toxic_contamination_score": 55,
        "community_health_impact_score": 52,
        "cleanup_liability_evasion_score": 50,
        "regulatory_compliance_failure_score": 49,
        "description": "Décharges situées dans des communautés défavorisées, justice environnementale contestée",
    },
    {
        "id": "TWE-007",
        "name": "SUEZ Group",
        "type": "municipal",
        "toxic_contamination_score": 31,
        "community_health_impact_score": 29,
        "cleanup_liability_evasion_score": 27,
        "regulatory_compliance_failure_score": 27,
        "description": "Amélioration progressive des pratiques, certifications environnementales en cours d'obtention",
    },
    {
        "id": "TWE-008",
        "name": "Interface Inc",
        "type": "foundation",
        "toxic_contamination_score": 14,
        "community_health_impact_score": 13,
        "cleanup_liability_evasion_score": 12,
        "regulatory_compliance_failure_score": 12,
        "description": "Leader mondial de la durabilité, Mission Zéro, processus de production à impact négatif",
    },
]


def calculate_composite(entity):
    """composite = sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20"""
    score = (
        entity["toxic_contamination_score"] * 0.30
        + entity["community_health_impact_score"] * 0.25
        + entity["cleanup_liability_evasion_score"] * 0.25
        + entity["regulatory_compliance_failure_score"] * 0.20
    )
    return round(score, 2)


def classify_severity(score):
    """Seuils : critique≥60, élevé≥40, modéré≥20, faible<20"""
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    else:
        return "faible"


def run_engine():
    results = []
    composite_scores = []

    for entity in ENTITIES:
        composite_score = calculate_composite(entity)
        severity = classify_severity(composite_score)
        estimated_index = round(composite_score / 100 * 10, 2)

        composite_scores.append(composite_score)

        results.append(
            {
                "id": entity["id"],
                "name": entity["name"],
                "type": entity["type"],
                "sub_scores": {
                    "toxic_contamination_score": entity["toxic_contamination_score"],
                    "community_health_impact_score": entity["community_health_impact_score"],
                    "cleanup_liability_evasion_score": entity["cleanup_liability_evasion_score"],
                    "regulatory_compliance_failure_score": entity["regulatory_compliance_failure_score"],
                },
                "composite_score": composite_score,
                "severity": severity,
                "estimated_toxic_waste_environmental_health_index": estimated_index,
                "description": entity["description"],
            }
        )

    avg_composite = round(sum(composite_scores) / len(composite_scores), 4)

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        distribution[r["severity"]] += 1

    return {
        "engine": "Toxic Waste Environmental Health Engine",
        "wave": 196,
        "swarm": "CaelumSwarm™",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
