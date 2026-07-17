"""
statelessness_document_rights_engine.py — Wave 193
Apatridie, accès aux documents & droits civils fondamentaux
"""

ENTITIES = [
    {
        "id": "SDR-001",
        "name": "Myanmar — Rohingyas 1M Apatrides, Génocide Documentaire & Juridique",
        "stateless_population_scale_score": 95,
        "documentation_access_denial_score": 96,
        "legal_protection_framework_gap_score": 94,
        "political_will_resolution_deficit_score": 92,
    },
    {
        "id": "SDR-002",
        "name": "Côte d'Ivoire — 700K Apatrides Post-Conflit, Enfants Sans Acte de Naissance",
        "stateless_population_scale_score": 88,
        "documentation_access_denial_score": 90,
        "legal_protection_framework_gap_score": 87,
        "political_will_resolution_deficit_score": 85,
    },
    {
        "id": "SDR-003",
        "name": "Bangladesh — Bihari 300K Apatrides 50 Ans, Camps Génération Perdue",
        "stateless_population_scale_score": 85,
        "documentation_access_denial_score": 88,
        "legal_protection_framework_gap_score": 86,
        "political_will_resolution_deficit_score": 90,
    },
    {
        "id": "SDR-004",
        "name": "Kuwait — Bidun 100K Résidents Sans Citoyenneté Depuis 1961",
        "stateless_population_scale_score": 82,
        "documentation_access_denial_score": 85,
        "legal_protection_framework_gap_score": 80,
        "political_will_resolution_deficit_score": 88,
    },
    {
        "id": "SDR-005",
        "name": "République Dominicaine — Dénationalisation Haïtiens, Arrêt TC 168-13",
        "stateless_population_scale_score": 55,
        "documentation_access_denial_score": 58,
        "legal_protection_framework_gap_score": 62,
        "political_will_resolution_deficit_score": 55,
    },
    {
        "id": "SDR-006",
        "name": "Thaïlande — Peuples Montagnards 500K Sans Papiers, Bouddhistes Exclus",
        "stateless_population_scale_score": 52,
        "documentation_access_denial_score": 55,
        "legal_protection_framework_gap_score": 50,
        "political_will_resolution_deficit_score": 58,
    },
    {
        "id": "SDR-007",
        "name": "Ukraine — Réfugiés Post-Guerre, Enregistrement Civil Ukrainien Partiel",
        "stateless_population_scale_score": 28,
        "documentation_access_denial_score": 25,
        "legal_protection_framework_gap_score": 30,
        "political_will_resolution_deficit_score": 22,
    },
    {
        "id": "SDR-008",
        "name": "Lettonie — Résolution Apatridie Soviet, Naturalisation Facilitée Récente",
        "stateless_population_scale_score": 10,
        "documentation_access_denial_score": 8,
        "legal_protection_framework_gap_score": 6,
        "political_will_resolution_deficit_score": 9,
    },
]


def compute(e):
    s = (
        e["stateless_population_scale_score"] * 0.30
        + e["documentation_access_denial_score"] * 0.25
        + e["legal_protection_framework_gap_score"] * 0.25
        + e["political_will_resolution_deficit_score"] * 0.20
    )
    lv = "critique" if s >= 60 else "élevé" if s >= 40 else "modéré" if s >= 20 else "faible"
    return {**e, "composite_score": round(s, 2), "risk_level": lv,
            "estimated_statelessness_document_rights_index": round(s / 100 * 10, 2)}


results = [compute(e) for e in ENTITIES]
dist = {l: sum(1 for r in results if r["risk_level"] == l)
        for l in ["critique", "élevé", "modéré", "faible"]}
avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

if __name__ == "__main__":
    print(f"avg_composite: {avg}")
    print(f"distribution: {dist}")
    for r in results:
        print(f"  {r['id']} | {r['composite_score']:.2f} | {r['risk_level']} | {r['estimated_statelessness_document_rights_index']}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée")
    print(f"✓ avg_composite = {avg}")
