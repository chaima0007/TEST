"""
offshore_tax_haven_rights_engine.py — Wave 193
Paradis fiscaux offshore & impact sur les droits humains
"""

ENTITIES = [
    {
        "id": "OTH-001",
        "name": "Îles Caïmans — 0% Impôt, 100K Entreprises, Services Publics Mondiaux Saignés",
        "tax_avoidance_scale_score": 94,
        "public_service_underfunding_score": 91,
        "inequality_amplification_score": 89,
        "corporate_transparency_deficit_score": 92,
    },
    {
        "id": "OTH-002",
        "name": "Luxembourg — Rulings Fiscaux Secrets, 4000 Entreprises Fortune 500",
        "tax_avoidance_scale_score": 88,
        "public_service_underfunding_score": 85,
        "inequality_amplification_score": 87,
        "corporate_transparency_deficit_score": 90,
    },
    {
        "id": "OTH-003",
        "name": "Îles Vierges Britanniques — 400K Sociétés Écrans, Corruption & Trafic",
        "tax_avoidance_scale_score": 92,
        "public_service_underfunding_score": 88,
        "inequality_amplification_score": 91,
        "corporate_transparency_deficit_score": 94,
    },
    {
        "id": "OTH-004",
        "name": "Suisse — Secret Bancaire Résiduel, Évasion Milliardaires Globaux",
        "tax_avoidance_scale_score": 85,
        "public_service_underfunding_score": 78,
        "inequality_amplification_score": 86,
        "corporate_transparency_deficit_score": 82,
    },
    {
        "id": "OTH-005",
        "name": "Dubai/EAU — Golden Visa Oligarques, Sanctionnés Russes & Blanchiment",
        "tax_avoidance_scale_score": 58,
        "public_service_underfunding_score": 55,
        "inequality_amplification_score": 60,
        "corporate_transparency_deficit_score": 62,
    },
    {
        "id": "OTH-006",
        "name": "Singapour — Hub Asie Évasion Fiscale, Familles Riches Chinoises & Indiennes",
        "tax_avoidance_scale_score": 55,
        "public_service_underfunding_score": 48,
        "inequality_amplification_score": 58,
        "corporate_transparency_deficit_score": 52,
    },
    {
        "id": "OTH-007",
        "name": "Irlande — Taux 12.5%, Apple 13B€ Remboursé, GAFA Optimisation",
        "tax_avoidance_scale_score": 30,
        "public_service_underfunding_score": 25,
        "inequality_amplification_score": 28,
        "corporate_transparency_deficit_score": 22,
    },
    {
        "id": "OTH-008",
        "name": "Danemark — Pilier 2 OCDE 15% Adopté, Registre Bénéficiaires Publics",
        "tax_avoidance_scale_score": 7,
        "public_service_underfunding_score": 5,
        "inequality_amplification_score": 6,
        "corporate_transparency_deficit_score": 8,
    },
]


def compute(e):
    s = (
        e["tax_avoidance_scale_score"] * 0.30
        + e["public_service_underfunding_score"] * 0.25
        + e["inequality_amplification_score"] * 0.25
        + e["corporate_transparency_deficit_score"] * 0.20
    )
    lv = "critique" if s >= 60 else "élevé" if s >= 40 else "modéré" if s >= 20 else "faible"
    return {**e, "composite_score": round(s, 2), "risk_level": lv,
            "estimated_offshore_tax_haven_rights_index": round(s / 100 * 10, 2)}


results = [compute(e) for e in ENTITIES]
dist = {l: sum(1 for r in results if r["risk_level"] == l)
        for l in ["critique", "élevé", "modéré", "faible"]}
avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

if __name__ == "__main__":
    print(f"avg_composite: {avg}")
    print(f"distribution: {dist}")
    for r in results:
        print(f"  {r['id']} | {r['composite_score']:.2f} | {r['risk_level']} | {r['estimated_offshore_tax_haven_rights_index']}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée")
    print(f"✓ avg_composite = {avg}")
