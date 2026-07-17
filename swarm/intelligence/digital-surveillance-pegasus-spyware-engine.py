"""
Wave 186 — Digital Surveillance & Pegasus Spyware Rights Engine
Caelum Partners — Human Rights Intelligence
"""

entities = [
    {
        "id": "DSP-001",
        "name": "Mexique/Pegasus Journalistes Défenseurs",
        "description": "50 000 Numéros Ciblés, Cartel Nexus, surveillance systémique documentée",
        "sub1": 95, "sub2": 93, "sub3": 91, "sub4": 92,
    },
    {
        "id": "DSP-002",
        "name": "Arabie Saoudite/Jamal Khashoggi Pegasus",
        "description": "Assassinat Prémédité Surveillance, NSO Group, cas emblématique",
        "sub1": 93, "sub2": 90, "sub3": 88, "sub4": 89,
    },
    {
        "id": "DSP-003",
        "name": "Inde/Opposition Activistes Ciblés",
        "description": "300 Numéros Vérifiés, Déni Gouvernement, Citizen Lab confirmation",
        "sub1": 89, "sub2": 86, "sub3": 84, "sub4": 85,
    },
    {
        "id": "DSP-004",
        "name": "Azerbaïdjan/Journalistes Emprisonnés Pegasus",
        "description": "Ilham Aliyev Surveillance Totale, médias indépendants ciblés",
        "sub1": 84, "sub2": 81, "sub3": 79, "sub4": 80,
    },
    {
        "id": "DSP-005",
        "name": "France/Macron Ciblé Maroc",
        "description": "Enquête Ouverte, NSO Group Restrictions UE, cas diplomatique majeur",
        "sub1": 56, "sub2": 53, "sub3": 51, "sub4": 52,
    },
    {
        "id": "DSP-006",
        "name": "EU/FinFisher Hacking Team",
        "description": "États Membres Utilisateurs, Parlement Enquête 2022, régulation insuffisante",
        "sub1": 48, "sub2": 45, "sub3": 43, "sub4": 44,
    },
    {
        "id": "DSP-007",
        "name": "USA/NSO Group Blacklist 2021",
        "description": "Commerce Dept. Sanctions, Apple Poursuite, cadre juridique en construction",
        "sub1": 31, "sub2": 28, "sub3": 26, "sub4": 27,
    },
    {
        "id": "DSP-008",
        "name": "UE/Règlement IA & Surveillance",
        "description": "GDPR Extension, Interdiction Partielle, meilleure protection régionale",
        "sub1": 11, "sub2": 9, "sub3": 8, "sub4": 9,
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
    estimated_surveillance_rights_index = round(composite_score / 100 * 10, 2)

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
        "estimated_surveillance_rights_index": estimated_surveillance_rights_index,
    })

avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)

print("=" * 60)
print("Wave 186 — Digital Surveillance & Pegasus Spyware Rights Engine")
print("=" * 60)
for r in results:
    print(f"[{r['id']}] {r['name']}")
    print(f"  composite_score={r['composite_score']} | risk={r['risk_level']} | index={r['estimated_surveillance_rights_index']}")

print()
print(f"avg_composite: {avg_composite}")
print(f"distribution: {distribution}")

assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
    f"Distribution error: {distribution}"
print("\n✓ Distribution PASS: 4 critique / 2 élevé / 1 modéré / 1 faible")
print(f"✓ estimated_surveillance_rights_index range: {results[-1]['estimated_surveillance_rights_index']} – {results[0]['estimated_surveillance_rights_index']}")
