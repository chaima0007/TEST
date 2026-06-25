"""
Wave 186 — Organ Trafficking & Transplant Tourism Engine
Caelum Partners — Human Rights Intelligence
"""

entities = [
    {
        "id": "OTT-001",
        "name": "Chine/Prélèvements Organes Prisonniers Conscience",
        "description": "Falun Gong Ouïghours, Tribunal Chine 2019, prélèvements forcés documentés",
        "sub1": 98, "sub2": 96, "sub3": 92, "sub4": 94,
    },
    {
        "id": "OTT-002",
        "name": "Pakistan/Trafic Reins Pauvres",
        "description": "Villages Organ, 2000 Reins/An, Vendeurs Exploités, filières établies",
        "sub1": 90, "sub2": 88, "sub3": 85, "sub4": 87,
    },
    {
        "id": "OTT-003",
        "name": "Égypte/Tourisme Transplant Illégal",
        "description": "Réfugiés Syriens Soudanais Exploités, Hôpitaux Complices, impunité",
        "sub1": 86, "sub2": 84, "sub3": 82, "sub4": 83,
    },
    {
        "id": "OTT-004",
        "name": "Kosovo/Clinique Medicus 2008",
        "description": "Meurtre Pour Organes, Procès EULEX, Impunité Partielle documentée",
        "sub1": 82, "sub2": 79, "sub3": 76, "sub4": 78,
    },
    {
        "id": "OTT-005",
        "name": "Inde/Marché Reins Informel",
        "description": "Dalits Vendeurs Contraints, Loi 1994 Contournée, réseau persistant",
        "sub1": 57, "sub2": 54, "sub3": 52, "sub4": 52,
    },
    {
        "id": "OTT-006",
        "name": "Philippines/Trafic Organes Post-Typhon",
        "description": "Situations Extrêmes Exploitation, vulnérabilité post-catastrophe",
        "sub1": 49, "sub2": 46, "sub3": 44, "sub4": 45,
    },
    {
        "id": "OTT-007",
        "name": "Interpol/Op. Lionfish",
        "description": "40 Pays Coordinés, 850 Arrestations, Lacunes Persistantes dans coordination",
        "sub1": 30, "sub2": 27, "sub3": 25, "sub4": 26,
    },
    {
        "id": "OTT-008",
        "name": "Espagne/Modèle Opt-Out Consentement",
        "description": "Taux Don Plus Élevé Monde, Trafic Minimal, modèle de référence",
        "sub1": 7, "sub2": 6, "sub3": 5, "sub4": 6,
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
    estimated_organ_trafficking_index = round(composite_score / 100 * 10, 2)

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
        "estimated_organ_trafficking_index": estimated_organ_trafficking_index,
    })

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

print("=" * 60)
print("Wave 186 — Organ Trafficking & Transplant Tourism Engine")
print("=" * 60)
for r in results:
    print(f"[{r['id']}] {r['name']}")
    print(f"  composite_score={r['composite_score']} | risk={r['risk_level']} | index={r['estimated_organ_trafficking_index']}")

print()
print(f"avg_composite: {avg_composite}")
print(f"distribution: {distribution}")

assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
    f"Distribution error: {distribution}"
print("\n✓ Distribution PASS: 4 critique / 2 élevé / 1 modéré / 1 faible")
print(f"✓ estimated_organ_trafficking_index range: {results[-1]['estimated_organ_trafficking_index']} – {results[0]['estimated_organ_trafficking_index']}")
