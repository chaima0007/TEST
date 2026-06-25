"""
deepfake_synthetic_media_rights_engine.py — Wave 193
Deepfakes, médias synthétiques & droits à l'identité numérique
"""

ENTITIES = [
    {
        "id": "DSM-001",
        "name": "Chine — Deepfakes Propagande État, Dissidents Ciblés & Fausses Preuves",
        "deepfake_identity_theft_scale_score": 91,
        "victim_redress_legal_deficit_score": 90,
        "state_weaponization_synthetic_media_score": 96,
        "platform_accountability_gap_score": 88,
    },
    {
        "id": "DSM-002",
        "name": "Russie — Opérations Influence IA, Fabrication Preuves Judiciaires",
        "deepfake_identity_theft_scale_score": 88,
        "victim_redress_legal_deficit_score": 92,
        "state_weaponization_synthetic_media_score": 94,
        "platform_accountability_gap_score": 86,
    },
    {
        "id": "DSM-003",
        "name": "Inde — Deepfake Pornographie Non-Consentie, 95% Victimes Femmes",
        "deepfake_identity_theft_scale_score": 90,
        "victim_redress_legal_deficit_score": 88,
        "state_weaponization_synthetic_media_score": 72,
        "platform_accountability_gap_score": 91,
    },
    {
        "id": "DSM-004",
        "name": "USA — Élections Deepfake, Absence Loi Fédérale, Big Tech Autorégulation",
        "deepfake_identity_theft_scale_score": 82,
        "victim_redress_legal_deficit_score": 75,
        "state_weaponization_synthetic_media_score": 68,
        "platform_accountability_gap_score": 85,
    },
    {
        "id": "DSM-005",
        "name": "Corée du Sud — Crise Deepfake Telegram, 80% Victimes Mineures",
        "deepfake_identity_theft_scale_score": 58,
        "victim_redress_legal_deficit_score": 52,
        "state_weaponization_synthetic_media_score": 38,
        "platform_accountability_gap_score": 60,
    },
    {
        "id": "DSM-006",
        "name": "Nigeria — Fraude Vocale IA, Arnaques Familiales & Romance Scams",
        "deepfake_identity_theft_scale_score": 55,
        "victim_redress_legal_deficit_score": 58,
        "state_weaponization_synthetic_media_score": 42,
        "platform_accountability_gap_score": 52,
    },
    {
        "id": "DSM-007",
        "name": "UE — AI Act Deepfake Watermarking, Protection Partielle En Cours",
        "deepfake_identity_theft_scale_score": 26,
        "victim_redress_legal_deficit_score": 22,
        "state_weaponization_synthetic_media_score": 12,
        "platform_accountability_gap_score": 30,
    },
    {
        "id": "DSM-008",
        "name": "Pays-Bas — C2PA Standard, Watermarking Obligatoire, Victimes Protégées",
        "deepfake_identity_theft_scale_score": 8,
        "victim_redress_legal_deficit_score": 6,
        "state_weaponization_synthetic_media_score": 4,
        "platform_accountability_gap_score": 10,
    },
]


def compute(e):
    s = (
        e["deepfake_identity_theft_scale_score"] * 0.30
        + e["victim_redress_legal_deficit_score"] * 0.25
        + e["state_weaponization_synthetic_media_score"] * 0.25
        + e["platform_accountability_gap_score"] * 0.20
    )
    lv = "critique" if s >= 60 else "élevé" if s >= 40 else "modéré" if s >= 20 else "faible"
    return {**e, "composite_score": round(s, 2), "risk_level": lv,
            "estimated_deepfake_synthetic_media_rights_index": round(s / 100 * 10, 2)}


results = [compute(e) for e in ENTITIES]
dist = {l: sum(1 for r in results if r["risk_level"] == l)
        for l in ["critique", "élevé", "modéré", "faible"]}
avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

if __name__ == "__main__":
    print(f"avg_composite: {avg}")
    print(f"distribution: {dist}")
    for r in results:
        print(f"  {r['id']} | {r['composite_score']:.2f} | {r['risk_level']} | {r['estimated_deepfake_synthetic_media_rights_index']}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("✓ Distribution validée")
    print(f"✓ avg_composite = {avg}")
