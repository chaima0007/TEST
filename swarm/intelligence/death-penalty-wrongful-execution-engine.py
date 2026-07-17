"""
Wave 186 — Death Penalty & Wrongful Execution Engine
Caelum Partners — Human Rights Intelligence
"""

entities = [
    {
        "id": "DPW-001",
        "name": "Chine/10 000 Exécutions/An Estimées",
        "description": "Opaque, Crimes Non-Violents, connexion organes, chiffres non officiels",
        "sub1": 97, "sub2": 94, "sub3": 92, "sub4": 93,
    },
    {
        "id": "DPW-002",
        "name": "Iran/Mineurs Exécutés",
        "description": "129 Depuis 1990, Convention Enfants Violée, condamnations avant 18 ans",
        "sub1": 92, "sub2": 89, "sub3": 87, "sub4": 88,
    },
    {
        "id": "DPW-003",
        "name": "Arabie Saoudite/Décapitations Publiques",
        "description": "196 Exécutions 2022, Crimes Drogue, étrangers surreprésentés",
        "sub1": 88, "sub2": 85, "sub3": 83, "sub4": 84,
    },
    {
        "id": "DPW-004",
        "name": "USA/Innocents Dans Couloir Mort",
        "description": "190 Exonérations Depuis 1973, Disparités Raciales documentées",
        "sub1": 81, "sub2": 78, "sub3": 76, "sub4": 77,
    },
    {
        "id": "DPW-005",
        "name": "Singapour/Peine Mort Trafic Drogue",
        "description": "Mandatoire, Condamnés Étrangers Majoritaires, aucune discrétion judiciaire",
        "sub1": 58, "sub2": 55, "sub3": 53, "sub4": 54,
    },
    {
        "id": "DPW-006",
        "name": "Japon/Peine Mort Secrète",
        "description": "Condamnés Notifiés Jour J, Isolement Total, opacité du système",
        "sub1": 50, "sub2": 47, "sub3": 45, "sub4": 46,
    },
    {
        "id": "DPW-007",
        "name": "UE/Abolition Totale",
        "description": "47 États Conseil Europe Aboli, Modèle Mondial, référence abolition",
        "sub1": 25, "sub2": 22, "sub3": 20, "sub4": 21,
    },
    {
        "id": "DPW-008",
        "name": "Rwanda/Abolition Post-Génocide",
        "description": "Modèle Réconciliation Sans Peine Mort, transition exceptionnelle",
        "sub1": 9, "sub2": 7, "sub3": 6, "sub4": 7,
    },
]

results = []
distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

for entity in entities:
    composite_score = (
        entity["sub1"] * 0.30
        + entity["sub2"] * 0.25
        + entity["sub3"] * 0.25
        + entity["sub4"] * 0.20
    )
    estimated_death_penalty_index = round(composite_score / 100 * 10, 2)

    if composite_score >= 60:
        risk_level = "critique"
    elif composite_score >= 40:
        risk_level = "élevé"
    elif composite_score >= 20:
        risk_level = "modéré"
    else:
        risk_level = "faible"

    distribution[risk_level] += 1

    results.append({
        "id": entity["id"],
        "name": entity["name"],
        "description": entity["description"],
        "composite_score": round(composite_score, 2),
        "risk_level": risk_level,
        "estimated_death_penalty_index": estimated_death_penalty_index,
    })

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

print("=" * 60)
print("Wave 186 — Death Penalty & Wrongful Execution Engine")
print("=" * 60)
for r in results:
    print(f"[{r['id']}] {r['name']}")
    print(f"  composite_score={r['composite_score']} | risk={r['risk_level']} | index={r['estimated_death_penalty_index']}")

print()
print(f"avg_composite: {avg_composite}")
print(f"distribution: {distribution}")

assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
    f"Distribution error: {distribution}"
print("\n✓ Distribution PASS: 4 critique / 2 élevé / 1 modéré / 1 faible")
print(f"✓ estimated_death_penalty_index range: {results[-1]['estimated_death_penalty_index']} – {results[0]['estimated_death_penalty_index']}")
