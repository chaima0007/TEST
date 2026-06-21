"""
Colonial Reparations & Transitional Justice Engine
Wave 127 — Caelum Partners Swarm Intelligence
Domaine : Réparations coloniales et justice transitionnelle
"""

entities = [
    {
        "id": "CRTJ-001",
        "name": "Belgique/Congo — Massacres Léopold II 10M Morts, Mains Coupées, Excuses Partielles 2020, Zéro Réparations Concrètes",
        "colonial_harm_documentation_recognition_gap_score": 95,
        "reparation_process_access_denial_score": 91,
        "stolen_assets_looted_artifacts_restitution_score": 89,
        "truth_commission_accountability_effectiveness_score": 87,
    },
    {
        "id": "CRTJ-002",
        "name": "France/Algérie — Massacres Sétif 1945 & Toussaint Rouge 1954-62, Reconnaissance Timide Macron 2017, Pas de Réparations",
        "colonial_harm_documentation_recognition_gap_score": 89,
        "reparation_process_access_denial_score": 85,
        "stolen_assets_looted_artifacts_restitution_score": 83,
        "truth_commission_accountability_effectiveness_score": 81,
    },
    {
        "id": "CRTJ-003",
        "name": "UK/Kenya & Caraïbes — Mau Mau Torture Reconnue 2013, CARICOM Réparations 10 Points, Londres Résiste",
        "colonial_harm_documentation_recognition_gap_score": 85,
        "reparation_process_access_denial_score": 81,
        "stolen_assets_looted_artifacts_restitution_score": 79,
        "truth_commission_accountability_effectiveness_score": 77,
    },
    {
        "id": "CRTJ-004",
        "name": "Pays-Bas/Indonésie — Exécutions Extrajudiciaires 1945-49, Excuses 2022 PM Rutte, Réparations Partielles Limitées",
        "colonial_harm_documentation_recognition_gap_score": 82,
        "reparation_process_access_denial_score": 78,
        "stolen_assets_looted_artifacts_restitution_score": 76,
        "truth_commission_accountability_effectiveness_score": 74,
    },
    {
        "id": "CRTJ-005",
        "name": "Allemagne/Namibie — Génocide Herero-Nama 1904-1908, Accord 2021 1.1Md€ Refusé Communautés, Processus Bloqué",
        "colonial_harm_documentation_recognition_gap_score": 55,
        "reparation_process_access_denial_score": 51,
        "stolen_assets_looted_artifacts_restitution_score": 49,
        "truth_commission_accountability_effectiveness_score": 47,
    },
    {
        "id": "CRTJ-006",
        "name": "Espagne/Amériques — Refus Total Reconnaissance, Débat Statue Colomb, Pas d'Excuses Mexique-Pérou 2019",
        "colonial_harm_documentation_recognition_gap_score": 51,
        "reparation_process_access_denial_score": 47,
        "stolen_assets_looted_artifacts_restitution_score": 45,
        "truth_commission_accountability_effectiveness_score": 43,
    },
    {
        "id": "CRTJ-007",
        "name": "Commission Vérité/Afrique du Sud — TRC 1995-2003, Reparation Grants 30K Personnes, Impunité Haute Direction ANC",
        "colonial_harm_documentation_recognition_gap_score": 27,
        "reparation_process_access_denial_score": 25,
        "stolen_assets_looted_artifacts_restitution_score": 23,
        "truth_commission_accountability_effectiveness_score": 21,
    },
    {
        "id": "CRTJ-008",
        "name": "Canada/Pensionnats — Commission Vérité 2015, 94 Appels Action, Excuses Harper 2008, Suivi Incomplet 2024",
        "colonial_harm_documentation_recognition_gap_score": 8,
        "reparation_process_access_denial_score": 6,
        "stolen_assets_looted_artifacts_restitution_score": 5,
        "truth_commission_accountability_effectiveness_score": 4,
    },
]

WEIGHTS = {
    "colonial_harm_documentation_recognition_gap_score": 0.30,
    "reparation_process_access_denial_score": 0.25,
    "stolen_assets_looted_artifacts_restitution_score": 0.25,
    "truth_commission_accountability_effectiveness_score": 0.20,
}

THRESHOLDS = {
    "critique": 60,
    "eleve": 40,
    "modere": 20,
}


def compute_composite(entity):
    return (
        entity["colonial_harm_documentation_recognition_gap_score"] * WEIGHTS["colonial_harm_documentation_recognition_gap_score"]
        + entity["reparation_process_access_denial_score"] * WEIGHTS["reparation_process_access_denial_score"]
        + entity["stolen_assets_looted_artifacts_restitution_score"] * WEIGHTS["stolen_assets_looted_artifacts_restitution_score"]
        + entity["truth_commission_accountability_effectiveness_score"] * WEIGHTS["truth_commission_accountability_effectiveness_score"]
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
        estimated_colonial_reparations_transitional_justice_index = round(composite / 100 * 10, 2)
        distribution[level] += 1
        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": round(composite, 2),
            "level": level,
            "estimated_colonial_reparations_transitional_justice_index": estimated_colonial_reparations_transitional_justice_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=" * 70)
    print("COLONIAL REPARATIONS & TRANSITIONAL JUSTICE ENGINE — Wave 127")
    print("=" * 70)
    for r in results:
        print(f"[{r['id']}] {r['level'].upper():8s} | score={r['composite_score']:5.2f} | index={r['estimated_colonial_reparations_transitional_justice_index']} | {r['name'][:60]}")
    print("-" * 70)
    print(f"avg_composite : {avg_composite}")
    print(f"Distribution  : critique={distribution['critique']} | élevé={distribution['élevé']} | modéré={distribution['modéré']} | faible={distribution['faible']}")
    expected = {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}
    ok = all(distribution[k] == expected[k] for k in expected)
    print(f"Distribution OK : {'✓' if ok else '✗ ERREUR'}")
    return results, avg_composite, distribution


if __name__ == "__main__":
    run()
