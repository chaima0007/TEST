"""Gig Workers Platform Economy Engine — CaelumSwarm™ Wave 196"""
import json

DOMAIN = "gig_workers_platform_economy"
PREFIX = "GWP"
ACCENT_COLOR = "#0369a1"

ENTITIES = [
    {
        "id": "GWP-001",
        "name": "Uber Technologies Inc",
        "type": "critique",
        "description": "Classification erronée des conducteurs, Proposition 22 Californie, absence de droits salariaux",
        "misclassification_score": 92,
        "social_protection_denial_score": 88,
        "algorithmic_control_opacity_score": 84,
        "income_instability_score": 80,
    },
    {
        "id": "GWP-002",
        "name": "Deliveroo Holdings plc",
        "type": "critique",
        "description": "Livreurs statut autoentrepreneur, accidents mortels non couverts, absence d'assurance professionnelle",
        "misclassification_score": 88,
        "social_protection_denial_score": 85,
        "algorithmic_control_opacity_score": 80,
        "income_instability_score": 78,
    },
    {
        "id": "GWP-003",
        "name": "Gig Work / Amazon Flex",
        "type": "critique",
        "description": "Surveillance algorithmique intensive, résiliation sans recours, pression de performance opaque",
        "misclassification_score": 86,
        "social_protection_denial_score": 82,
        "algorithmic_control_opacity_score": 84,
        "income_instability_score": 76,
    },
    {
        "id": "GWP-004",
        "name": "Glovo App SL",
        "type": "critique",
        "description": "Accidents mortels de livreurs en Espagne et Italie non couverts, faux autoentreprenariat reconnu par tribunaux",
        "misclassification_score": 82,
        "social_protection_denial_score": 79,
        "algorithmic_control_opacity_score": 74,
        "income_instability_score": 70,
    },
    {
        "id": "GWP-005",
        "name": "Lyft Inc",
        "type": "élevé",
        "description": "Modèle similaire à Uber, protections inférieures aux standards européens (Bolt), lobbying contre reclassification",
        "misclassification_score": 64,
        "social_protection_denial_score": 60,
        "algorithmic_control_opacity_score": 56,
        "income_instability_score": 54,
    },
    {
        "id": "GWP-006",
        "name": "Fiverr International",
        "type": "élevé",
        "description": "Travailleurs mondiaux sans protections sociales, délais de paiement, commissions élevées, absence de contrats",
        "misclassification_score": 56,
        "social_protection_denial_score": 54,
        "algorithmic_control_opacity_score": 50,
        "income_instability_score": 50,
    },
    {
        "id": "GWP-007",
        "name": "Etsy Inc",
        "type": "modéré",
        "description": "Artisans indépendants, politique en cours d'amélioration, frais de commission croissants contestés",
        "misclassification_score": 32,
        "social_protection_denial_score": 30,
        "algorithmic_control_opacity_score": 28,
        "income_instability_score": 30,
    },
    {
        "id": "GWP-008",
        "name": "Fairwork Foundation",
        "type": "faible",
        "description": "ONG de notation des conditions des gig workers, acteur de référence pour les standards équitables",
        "misclassification_score": 14,
        "social_protection_denial_score": 12,
        "algorithmic_control_opacity_score": 14,
        "income_instability_score": 12,
    },
]


def calculate_composite(entity: dict) -> float:
    """Calcule le composite : sub1×0.30 + sub2×0.25 + sub3×0.25 + sub4×0.20"""
    composite = (
        entity["misclassification_score"] * 0.30
        + entity["social_protection_denial_score"] * 0.25
        + entity["algorithmic_control_opacity_score"] * 0.25
        + entity["income_instability_score"] * 0.20
    )
    return round(composite, 2)


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
    severity_counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

    for entity in ENTITIES:
        composite_score = calculate_composite(entity)
        severity = classify_severity(composite_score)
        gig_index = round(composite_score / 100 * 10, 2)

        result = {
            "id": entity["id"],
            "name": entity["name"],
            "declared_type": entity["type"],
            "computed_severity": severity,
            "sub_scores": {
                "misclassification_score": entity["misclassification_score"],
                "social_protection_denial_score": entity["social_protection_denial_score"],
                "algorithmic_control_opacity_score": entity["algorithmic_control_opacity_score"],
                "income_instability_score": entity["income_instability_score"],
            },
            "composite_score": composite_score,
            "estimated_gig_workers_platform_economy_index": gig_index,
            "description": entity["description"],
        }
        results.append(result)
        severity_counts[severity] += 1

    composites = [r["composite_score"] for r in results]
    avg_composite = round(sum(composites) / len(composites), 4)

    return {
        "engine": "Gig Workers Platform Economy Engine",
        "wave": 196,
        "swarm": "CaelumSwarm™",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "entity_count": len(results),
        "severity_distribution": severity_counts,
        "avg_composite": avg_composite,
        "entities": results,
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
