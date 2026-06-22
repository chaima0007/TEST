"""Internet Access Rights Engine — CaelumSwarm™ Wave 213"""
import json

DOMAIN = "internet_access_rights"
PREFIX = "IAR"
ACCENT_COLOR = "#051a2e"

ENTITIES = [
    {
        "id": "IAR-001",
        "name": "Corée du Nord",
        "type": "etat",
        "connectivity_gap_score": 98.0,
        "censorship_score": 99.0,
        "affordability_barrier_score": 97.0,
        "shutdown_frequency_score": 95.0,
        "description": "Internet totalement bloqué pour population, accès intranet national Kwangmyong uniquement, contrôle absolu information",
    },
    {
        "id": "IAR-002",
        "name": "Érythrée",
        "type": "etat",
        "connectivity_gap_score": 90.0,
        "censorship_score": 88.0,
        "affordability_barrier_score": 92.0,
        "shutdown_frequency_score": 86.0,
        "description": "1% population connectée, coût accès prohibitif, censure totale, État contrôle unique fournisseur EriTel",
    },
    {
        "id": "IAR-003",
        "name": "Éthiopie",
        "type": "etat",
        "connectivity_gap_score": 82.0,
        "censorship_score": 80.0,
        "affordability_barrier_score": 78.0,
        "shutdown_frequency_score": 85.0,
        "description": "Coupures internet fréquentes lors conflits Tigré/Oromo, blocage réseaux sociaux, monopole Ethio Telecom",
    },
    {
        "id": "IAR-004",
        "name": "Myanmar",
        "type": "etat",
        "connectivity_gap_score": 78.0,
        "censorship_score": 82.0,
        "affordability_barrier_score": 75.0,
        "shutdown_frequency_score": 88.0,
        "description": "Coupures massives post-coup 2021, blocage réseaux sociaux, ciblage activistes numériques, 4G coupé régions rebelles",
    },
    {
        "id": "IAR-005",
        "name": "Iran",
        "type": "etat",
        "connectivity_gap_score": 52.0,
        "censorship_score": 58.0,
        "affordability_barrier_score": 48.0,
        "shutdown_frequency_score": 55.0,
        "description": "Filtrage massif réseaux sociaux occidentaux, coupures lors protestations 2022, internet national Halal développé",
    },
    {
        "id": "IAR-006",
        "name": "Cuba",
        "type": "etat",
        "connectivity_gap_score": 50.0,
        "censorship_score": 54.0,
        "affordability_barrier_score": 56.0,
        "shutdown_frequency_score": 48.0,
        "description": "Accès très limité, coût élevé relatif salaires, blocage réseaux sociaux lors manifestations 2021, contrôle ETECSA",
    },
    {
        "id": "IAR-007",
        "name": "Inde",
        "type": "etat",
        "connectivity_gap_score": 30.0,
        "censorship_score": 28.0,
        "affordability_barrier_score": 25.0,
        "shutdown_frequency_score": 35.0,
        "description": "Leader mondial coupures internet régionales (Jammu-Cachemire), blocages ciblés lors tensions communautaires fréquents",
    },
    {
        "id": "IAR-008",
        "name": "Estonie",
        "type": "etat",
        "connectivity_gap_score": 8.0,
        "censorship_score": 6.0,
        "affordability_barrier_score": 7.0,
        "shutdown_frequency_score": 5.0,
        "description": "Meilleure pratique mondiale, internet droit constitutionnel depuis 2000, accès universel garanti, e-gouvernement modèle",
    },
]


def calculate_composite(entity: dict) -> float:
    return round(
        entity["connectivity_gap_score"] * 0.30
        + entity["censorship_score"] * 0.25
        + entity["affordability_barrier_score"] * 0.25
        + entity["shutdown_frequency_score"] * 0.20,
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
            "estimated_internet_access_rights_index": index,
            "description": entity["description"],
        })
    avg_composite = round(sum(composite_scores) / len(composite_scores), 2)
    distribution = {}
    for r in results:
        distribution[r["severity"]] = distribution.get(r["severity"], 0) + 1
    return {
        "engine": "Internet Access Rights Engine",
        "domain": DOMAIN,
        "prefix": PREFIX,
        "accent_color": ACCENT_COLOR,
        "wave": 213,
        "entities": results,
        "summary": {
            "total_entities": len(results),
            "avg_composite_score": avg_composite,
            "avg_internet_access_rights_index": round(avg_composite / 100 * 10, 2),
            "distribution": distribution,
        },
    }


if __name__ == "__main__":
    result = run_engine()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n--- VALIDATION ---")
    print(f"avg_composite: {result['summary']['avg_composite_score']}")
    print(f"distribution: {result['summary']['distribution']}")
