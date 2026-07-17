"""
Mining Extraction & Community Rights Engine
Wave 127 — Caelum Partners Swarm Intelligence
Domaine : Droits des communautés face à l'extraction minière
"""

entities = [
    {
        "id": "MCR-001",
        "name": "RDC/Cobalt — Mines Artisanales Kolwezi, Cyanure Rivières, Enfants Travailleurs, Communautés Expulsées Sans Compensation",
        "mining_environmental_pollution_health_score": 96,
        "land_acquisition_community_displacement_score": 92,
        "benefit_sharing_revenue_distribution_gap_score": 90,
        "environmental_permit_oversight_failure_score": 88,
    },
    {
        "id": "MCR-002",
        "name": "Pérou/Minières — Cajamarca Yanacocha Gold, Conga Project Stoppé Résistance, 4 Mineurs Tués 2012 Cerro Verde",
        "mining_environmental_pollution_health_score": 88,
        "land_acquisition_community_displacement_score": 84,
        "benefit_sharing_revenue_distribution_gap_score": 82,
        "environmental_permit_oversight_failure_score": 80,
    },
    {
        "id": "MCR-003",
        "name": "Philippines/Mines — Hacienda Luisita, Nickel Mining Palawan, Lumad Déplacés, EO 130 Militarisation Zones Minières",
        "mining_environmental_pollution_health_score": 85,
        "land_acquisition_community_displacement_score": 81,
        "benefit_sharing_revenue_distribution_gap_score": 79,
        "environmental_permit_oversight_failure_score": 77,
    },
    {
        "id": "MCR-004",
        "name": "Ghana/Galamsey — Orpaillage Illégal Rivières Offin/Pra, Eau Potable 5M Personnes, Corruption Autorités Minières",
        "mining_environmental_pollution_health_score": 82,
        "land_acquisition_community_displacement_score": 78,
        "benefit_sharing_revenue_distribution_gap_score": 76,
        "environmental_permit_oversight_failure_score": 74,
    },
    {
        "id": "MCR-005",
        "name": "Australie/Pilbara — Juukan Gorge Détruite Rio Tinto 2020, 46K Ans Patrimoine, Excuses Sans Poursuites, FPIC",
        "mining_environmental_pollution_health_score": 55,
        "land_acquisition_community_displacement_score": 51,
        "benefit_sharing_revenue_distribution_gap_score": 49,
        "environmental_permit_oversight_failure_score": 47,
    },
    {
        "id": "MCR-006",
        "name": "Chili/Lithium — Atacama Salar, Peuple Atacameño Sécheresse, SQM Contrats Non Consultés, Eau -65% Wetlands",
        "mining_environmental_pollution_health_score": 51,
        "land_acquisition_community_displacement_score": 47,
        "benefit_sharing_revenue_distribution_gap_score": 45,
        "environmental_permit_oversight_failure_score": 43,
    },
    {
        "id": "MCR-007",
        "name": "OCDE/Minerals — Guidance Due Diligence Chaînes Approvisionnement Minéraux Conflits, Application Volontaire Insuffisante",
        "mining_environmental_pollution_health_score": 27,
        "land_acquisition_community_displacement_score": 25,
        "benefit_sharing_revenue_distribution_gap_score": 23,
        "environmental_permit_oversight_failure_score": 21,
    },
    {
        "id": "MCR-008",
        "name": "Botswana/Diamonds — Debswana Partnership, Community Benefit Programme, Recettes 30% État, Modèle Partiel Référence",
        "mining_environmental_pollution_health_score": 8,
        "land_acquisition_community_displacement_score": 6,
        "benefit_sharing_revenue_distribution_gap_score": 5,
        "environmental_permit_oversight_failure_score": 4,
    },
]

WEIGHTS = {
    "mining_environmental_pollution_health_score": 0.30,
    "land_acquisition_community_displacement_score": 0.25,
    "benefit_sharing_revenue_distribution_gap_score": 0.25,
    "environmental_permit_oversight_failure_score": 0.20,
}

THRESHOLDS = {
    "critique": 60,
    "eleve": 40,
    "modere": 20,
}


def compute_composite(entity):
    return (
        entity["mining_environmental_pollution_health_score"] * WEIGHTS["mining_environmental_pollution_health_score"]
        + entity["land_acquisition_community_displacement_score"] * WEIGHTS["land_acquisition_community_displacement_score"]
        + entity["benefit_sharing_revenue_distribution_gap_score"] * WEIGHTS["benefit_sharing_revenue_distribution_gap_score"]
        + entity["environmental_permit_oversight_failure_score"] * WEIGHTS["environmental_permit_oversight_failure_score"]
    )


def classify(score):
    if score >= THRESHOLDS["critique"]:
        return "critique"
    elif score >= THRESHOLDS["eleve"]:
        return "élevé"
    elif score >= THRESHOLDS["modere"]:
        return "modéré"
    else:
        return "faible"


def run():
    results = []
    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

    for entity in entities:
        composite = compute_composite(entity)
        level = classify(composite)
        estimated_mining_extraction_community_rights_index = round(composite / 100 * 10, 2)
        distribution[level] += 1
        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": round(composite, 2),
            "level": level,
            "estimated_mining_extraction_community_rights_index": estimated_mining_extraction_community_rights_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=" * 70)
    print("MINING EXTRACTION & COMMUNITY RIGHTS ENGINE — Wave 127")
    print("=" * 70)
    for r in results:
        print(f"[{r['id']}] {r['level'].upper():8s} | score={r['composite_score']:5.2f} | index={r['estimated_mining_extraction_community_rights_index']} | {r['name'][:60]}")
    print("-" * 70)
    print(f"avg_composite : {avg_composite}")
    print(f"Distribution  : critique={distribution['critique']} | élevé={distribution['élevé']} | modéré={distribution['modéré']} | faible={distribution['faible']}")
    expected = {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}
    ok = all(distribution[k] == expected[k] for k in expected)
    print(f"Distribution OK : {'✓' if ok else '✗ ERREUR'}")
    return results, avg_composite, distribution


if __name__ == "__main__":
    run()
