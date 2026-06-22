"""Corporate Impunity Rights Engine — CaelumSwarm™ Wave 213"""
import json

DOMAIN = "corporate_impunity_rights"
PREFIX = "CIR"
ACCENT_COLOR = "#1a0505"

ENTITIES = [
    {
        "id": "CIR-001",
        "name": "Shell Nigeria",
        "type": "corporation",
        "accountability_gap_score": 92.0,
        "legal_remedy_obstruction_score": 90.0,
        "profit_over_rights_score": 91.0,
        "regulatory_capture_score": 88.0,
        "description": "Pollution massive delta du Niger impunie depuis 60 ans, communautés Ogoni sans recours juridique effectif",
    },
    {
        "id": "CIR-002",
        "name": "Chevron Ecuador",
        "type": "corporation",
        "accountability_gap_score": 89.0,
        "legal_remedy_obstruction_score": 88.0,
        "profit_over_rights_score": 87.0,
        "regulatory_capture_score": 85.0,
        "description": "Contamination Amazonie équatorienne 18 milliards USD, refus exécution jugement, déplacement peuples Secoya et Siona",
    },
    {
        "id": "CIR-003",
        "name": "Rio Tinto Papua",
        "type": "corporation",
        "accountability_gap_score": 85.0,
        "legal_remedy_obstruction_score": 83.0,
        "profit_over_rights_score": 86.0,
        "regulatory_capture_score": 82.0,
        "description": "Mine cuivre Bougainville déversements catastrophiques, destruction environnement côtier, impunité complète post-fermeture",
    },
    {
        "id": "CIR-004",
        "name": "Vale Brumadinho",
        "type": "corporation",
        "accountability_gap_score": 80.0,
        "legal_remedy_obstruction_score": 78.0,
        "profit_over_rights_score": 82.0,
        "regulatory_capture_score": 76.0,
        "description": "Rupture barrage 2019, 270 morts, accord compensation insuffisant, dirigeants jamais emprisonnés malgré condamnations",
    },
    {
        "id": "CIR-005",
        "name": "Glencore",
        "type": "corporation",
        "accountability_gap_score": 57.0,
        "legal_remedy_obstruction_score": 55.0,
        "profit_over_rights_score": 58.0,
        "regulatory_capture_score": 53.0,
        "description": "Mines RDC Katanga, travail enfants documenté, corruption fonctionnaires, paiements pour éviter poursuites",
    },
    {
        "id": "CIR-006",
        "name": "Volkswagen",
        "type": "corporation",
        "accountability_gap_score": 48.0,
        "legal_remedy_obstruction_score": 50.0,
        "profit_over_rights_score": 52.0,
        "regulatory_capture_score": 46.0,
        "description": "Dieselgate impacts santé publique millions personnes, compensations limitées hors USA, lobbying anti-réglementation",
    },
    {
        "id": "CIR-007",
        "name": "BP",
        "type": "corporation",
        "accountability_gap_score": 30.0,
        "legal_remedy_obstruction_score": 28.0,
        "profit_over_rights_score": 32.0,
        "regulatory_capture_score": 26.0,
        "description": "Deepwater Horizon compensation partielle Gulf States, accord 20 milliards mais impacts long-terme non couverts",
    },
    {
        "id": "CIR-008",
        "name": "Patagonia",
        "type": "corporation",
        "accountability_gap_score": 10.0,
        "legal_remedy_obstruction_score": 9.0,
        "profit_over_rights_score": 8.0,
        "regulatory_capture_score": 12.0,
        "description": "Meilleure pratique B Corp, responsabilité entreprise modèle, transparence chaîne approvisionnement et recours effectifs",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["accountability_gap_score"] * 0.30
        + entity["legal_remedy_obstruction_score"] * 0.25
        + entity["profit_over_rights_score"] * 0.25
        + entity["regulatory_capture_score"] * 0.20,
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
            "estimated_corporate_impunity_rights_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Corporate Impunity Rights Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 213,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_corporate_impunity_rights_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
