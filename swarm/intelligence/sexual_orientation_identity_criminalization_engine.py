"""
Sexual Orientation & Identity Criminalization Engine
Wave 127 — Caelum Partners Swarm Intelligence
Domaine : Criminalisation orientation sexuelle et identité de genre
Angle distinct de lgbtq_rights_violence_criminalization : focus sur criminalisation légale spécifique
(codes pénaux, reconnaissance genre, thérapies conversion, intégrité corporelle intersexes)
"""

entities = [
    {
        "id": "SOIC-001",
        "name": "Ouganda/Anti-Homosexuality Act — Peine Mort 2023, Prisonniers Arrêtés, USA Sanctions, Fuite Activistes, Cliniques Fermées",
        "legal_criminalization_sodomy_laws_score": 97,
        "transgender_legal_gender_recognition_gap_score": 90,
        "conversion_therapy_prohibition_gap_score": 88,
        "intersex_bodily_integrity_violations_score": 85,
    },
    {
        "id": "SOIC-002",
        "name": "Iran — Exécutions Homosexuels, 100+ Depuis 1979, Opérations Changement Sexe Financées État vs Identité Homosexuelle",
        "legal_criminalization_sodomy_laws_score": 93,
        "transgender_legal_gender_recognition_gap_score": 87,
        "conversion_therapy_prohibition_gap_score": 85,
        "intersex_bodily_integrity_violations_score": 82,
    },
    {
        "id": "SOIC-003",
        "name": "Russie — Propagande LGBT 2023 Étendue à Adultes, Mouvement Extrémiste Interdit, ONG Liquidées, Couples Fuient",
        "legal_criminalization_sodomy_laws_score": 88,
        "transgender_legal_gender_recognition_gap_score": 83,
        "conversion_therapy_prohibition_gap_score": 82,
        "intersex_bodily_integrity_violations_score": 80,
    },
    {
        "id": "SOIC-004",
        "name": "Arabie Saoudite — Peine Mort, 35 Condamnés 2019-2023, Checkpoints Vêtements, Grindr Monitoring Police",
        "legal_criminalization_sodomy_laws_score": 85,
        "transgender_legal_gender_recognition_gap_score": 80,
        "conversion_therapy_prohibition_gap_score": 79,
        "intersex_bodily_integrity_violations_score": 77,
    },
    {
        "id": "SOIC-005",
        "name": "Pologne/Hongrie — Zones LGBT-Free Pologne 2019 (annulées partiellement), Hongrie Propagande Enfants 2021, CEDH Saisie",
        "legal_criminalization_sodomy_laws_score": 55,
        "transgender_legal_gender_recognition_gap_score": 52,
        "conversion_therapy_prohibition_gap_score": 50,
        "intersex_bodily_integrity_violations_score": 48,
    },
    {
        "id": "SOIC-006",
        "name": "Kenya — Article 162 Code Pénal Britannique, 14 Ans Prison, Égalité Non-Sens Cour Suprême 2023, Activistes Ciblés",
        "legal_criminalization_sodomy_laws_score": 51,
        "transgender_legal_gender_recognition_gap_score": 48,
        "conversion_therapy_prohibition_gap_score": 46,
        "intersex_bodily_integrity_violations_score": 44,
    },
    {
        "id": "SOIC-007",
        "name": "Conseil Europe/ILGA — Rapport Annuel Criminalisation, 64 Pays Criminalisant Encore, ONU Résolutions, Standards CEDH",
        "legal_criminalization_sodomy_laws_score": 27,
        "transgender_legal_gender_recognition_gap_score": 25,
        "conversion_therapy_prohibition_gap_score": 24,
        "intersex_bodily_integrity_violations_score": 22,
    },
    {
        "id": "SOIC-008",
        "name": "Islande/Malte — Législation Trans Auto-Détermination Sans Conditions, Interdiction Thérapies Conversion, Modèle Mondial",
        "legal_criminalization_sodomy_laws_score": 5,
        "transgender_legal_gender_recognition_gap_score": 4,
        "conversion_therapy_prohibition_gap_score": 4,
        "intersex_bodily_integrity_violations_score": 3,
    },
]

WEIGHTS = {
    "legal_criminalization_sodomy_laws_score": 0.30,
    "transgender_legal_gender_recognition_gap_score": 0.25,
    "conversion_therapy_prohibition_gap_score": 0.25,
    "intersex_bodily_integrity_violations_score": 0.20,
}

THRESHOLDS = {
    "critique": 60,
    "eleve": 40,
    "modere": 20,
}


def compute_composite(entity):
    return (
        entity["legal_criminalization_sodomy_laws_score"] * WEIGHTS["legal_criminalization_sodomy_laws_score"]
        + entity["transgender_legal_gender_recognition_gap_score"] * WEIGHTS["transgender_legal_gender_recognition_gap_score"]
        + entity["conversion_therapy_prohibition_gap_score"] * WEIGHTS["conversion_therapy_prohibition_gap_score"]
        + entity["intersex_bodily_integrity_violations_score"] * WEIGHTS["intersex_bodily_integrity_violations_score"]
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
        estimated_sexual_orientation_identity_criminalization_index = round(composite / 100 * 10, 2)
        distribution[level] += 1
        results.append({
            "id": entity["id"],
            "name": entity["name"],
            "composite_score": round(composite, 2),
            "level": level,
            "estimated_sexual_orientation_identity_criminalization_index": estimated_sexual_orientation_identity_criminalization_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=" * 70)
    print("SEXUAL ORIENTATION & IDENTITY CRIMINALIZATION ENGINE — Wave 127")
    print("=" * 70)
    for r in results:
        print(f"[{r['id']}] {r['level'].upper():8s} | score={r['composite_score']:5.2f} | index={r['estimated_sexual_orientation_identity_criminalization_index']} | {r['name'][:60]}")
    print("-" * 70)
    print(f"avg_composite : {avg_composite}")
    print(f"Distribution  : critique={distribution['critique']} | élevé={distribution['élevé']} | modéré={distribution['modéré']} | faible={distribution['faible']}")
    expected = {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}
    ok = all(distribution[k] == expected[k] for k in expected)
    print(f"Distribution OK : {'✓' if ok else '✗ ERREUR'}")
    return results, avg_composite, distribution


if __name__ == "__main__":
    run()
