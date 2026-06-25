"""Forced Marriage Rights Engine — CaelumSwarm™ Wave 210"""
import json

DOMAIN = "forced_marriage_rights"
PREFIX = "FMR"
ACCENT_COLOR = "#1e3a2f"

ENTITIES = [
    {
        "id": "FMR-001",
        "name": "UNICEF",
        "type": "organisation_internationale",
        "forced_marriage_prevalence_score": 82.0,
        "legal_protection_gap_score": 80.0,
        "victim_support_deficit_score": 81.0,
        "cultural_impunity_score": 78.0,
        "description": "Rapporte 650M femmes mariées enfants, crise globale persistante malgré engagements SDG",
    },
    {
        "id": "FMR-002",
        "name": "Girls Not Brides",
        "type": "ong",
        "forced_marriage_prevalence_score": 85.0,
        "legal_protection_gap_score": 83.0,
        "victim_support_deficit_score": 84.0,
        "cultural_impunity_score": 81.0,
        "description": "Coalition 1400 ONG, documente mariages forcés dans 100+ pays, contexte mondial sévère",
    },
    {
        "id": "FMR-003",
        "name": "Human Rights Watch",
        "type": "ong",
        "forced_marriage_prevalence_score": 79.0,
        "legal_protection_gap_score": 77.0,
        "victim_support_deficit_score": 78.0,
        "cultural_impunity_score": 75.0,
        "description": "Documente mariages forcés au Yémen, Bangladesh, Afrique subsaharienne et Moyen-Orient",
    },
    {
        "id": "FMR-004",
        "name": "Pakistan",
        "type": "etat",
        "forced_marriage_prevalence_score": 88.0,
        "legal_protection_gap_score": 85.0,
        "victim_support_deficit_score": 82.0,
        "cultural_impunity_score": 86.0,
        "description": "Taux mariage enfants 21%, loi 2014 peu appliquée, impunité culturelle persistante dans zones rurales",
    },
    {
        "id": "FMR-005",
        "name": "Bangladesh",
        "type": "etat",
        "forced_marriage_prevalence_score": 57.0,
        "legal_protection_gap_score": 54.0,
        "victim_support_deficit_score": 55.0,
        "cultural_impunity_score": 52.0,
        "description": "Taux mariage enfants 51%, loi 2017 avec exceptions, progrès limités dans districts ruraux",
    },
    {
        "id": "FMR-006",
        "name": "Niger",
        "type": "etat",
        "forced_marriage_prevalence_score": 60.0,
        "legal_protection_gap_score": 57.0,
        "victim_support_deficit_score": 58.0,
        "cultural_impunity_score": 55.0,
        "description": "Taux mariage enfants 76%, le plus élevé au monde, lacunes légales majeures et normes sociales",
    },
    {
        "id": "FMR-007",
        "name": "Canada",
        "type": "etat",
        "forced_marriage_prevalence_score": 34.0,
        "legal_protection_gap_score": 31.0,
        "victim_support_deficit_score": 29.0,
        "cultural_impunity_score": 27.0,
        "description": "Protections légales solides mais lacunes dans communautés diaspora, criminalisation 2015 peu connue",
    },
    {
        "id": "FMR-008",
        "name": "Islande",
        "type": "etat",
        "forced_marriage_prevalence_score": 14.0,
        "legal_protection_gap_score": 12.0,
        "victim_support_deficit_score": 11.0,
        "cultural_impunity_score": 13.0,
        "description": "Meilleure pratique mondiale, cadre légal complet, âge minimum mariage 18 ans strict, faible impunité",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["forced_marriage_prevalence_score"] * 0.30
        + entity["legal_protection_gap_score"] * 0.25
        + entity["victim_support_deficit_score"] * 0.25
        + entity["cultural_impunity_score"] * 0.20,
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
            "estimated_forced_marriage_rights_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Forced Marriage Rights Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 210,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_forced_marriage_rights_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
