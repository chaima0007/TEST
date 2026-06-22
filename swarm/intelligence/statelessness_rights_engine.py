"""Statelessness Rights Engine — CaelumSwarm™ Wave 210"""
import json

DOMAIN = "statelessness_rights"
PREFIX = "STR"
ACCENT_COLOR = "#2a1f3d"

ENTITIES = [
    {
        "id": "STR-001",
        "name": "Myanmar / Rohingya",
        "type": "population_apatride",
        "stateless_population_score": 92.0,
        "documentation_denial_score": 89.0,
        "legal_limbo_score": 90.0,
        "discrimination_vulnerability_score": 87.0,
        "description": "600 000 Rohingyas apatrides, citoyenneté refusée depuis 1982, génocide reconnu ICJ 2019, camps UNHCR Bangladesh",
    },
    {
        "id": "STR-002",
        "name": "Kuwait / Bidun",
        "type": "population_apatride",
        "stateless_population_score": 89.0,
        "documentation_denial_score": 87.0,
        "legal_limbo_score": 88.0,
        "discrimination_vulnerability_score": 85.0,
        "description": "100 000 Bidun sans nationalité, zéro droits légaux, arrestations arbitraires, exclusion totale services publics",
    },
    {
        "id": "STR-003",
        "name": "République Dominicaine",
        "type": "etat",
        "stateless_population_score": 84.0,
        "documentation_denial_score": 82.0,
        "legal_limbo_score": 83.0,
        "discrimination_vulnerability_score": 80.0,
        "description": "Décision TC168/13 dénaturalise 200 000 descendants haïtiens rétroactivement, expulsions sans procédure légale",
    },
    {
        "id": "STR-004",
        "name": "Thaïlande / Tribus des collines",
        "type": "population_apatride",
        "stateless_population_score": 80.0,
        "documentation_denial_score": 78.0,
        "legal_limbo_score": 79.0,
        "discrimination_vulnerability_score": 76.0,
        "description": "400 000 membres tribus montagnardes sans nationalité, accès refusé santé/éducation/emploi, vulnérabilité traite",
    },
    {
        "id": "STR-005",
        "name": "Arabie Saoudite",
        "type": "etat",
        "stateless_population_score": 60.0,
        "documentation_denial_score": 58.0,
        "legal_limbo_score": 57.0,
        "discrimination_vulnerability_score": 56.0,
        "description": "Système kafala crée vulnérabilité apatridie travailleurs migrants, procédure naturalisation opaque et discriminatoire",
    },
    {
        "id": "STR-006",
        "name": "Côte d'Ivoire",
        "type": "etat",
        "stateless_population_score": 57.0,
        "documentation_denial_score": 55.0,
        "legal_limbo_score": 56.0,
        "discrimination_vulnerability_score": 53.0,
        "description": "700 000 apatrides post-conflit, communautés nordistes sans documents, crise ivoirité persistante",
    },
    {
        "id": "STR-007",
        "name": "Népal",
        "type": "etat",
        "stateless_population_score": 37.0,
        "documentation_denial_score": 35.0,
        "legal_limbo_score": 34.0,
        "discrimination_vulnerability_score": 33.0,
        "description": "Loi citoyenneté discriminatoire basée sur père, femmes et enfants de mères seules exclus, réformes en cours",
    },
    {
        "id": "STR-008",
        "name": "Estonie",
        "type": "etat",
        "stateless_population_score": 18.0,
        "documentation_denial_score": 16.0,
        "legal_limbo_score": 15.0,
        "discrimination_vulnerability_score": 17.0,
        "description": "Meilleure pratique UNHCR, programme naturalisation russophone, statut alien réduit, accords intégration UE",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["stateless_population_score"] * 0.30
        + entity["documentation_denial_score"] * 0.25
        + entity["legal_limbo_score"] * 0.25
        + entity["discrimination_vulnerability_score"] * 0.20,
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
            "estimated_statelessness_rights_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Statelessness Rights Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 210,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_statelessness_rights_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
