"""indigenous_language_extinction_rights_engine.py — Wave 192"""

ENTITIES = [
    {
        "id": "ILE-001",
        "name": "Papouasie-Nouvelle-Guinée — 840 Langues, 200 En Extinction Critique",
        "country": "Papouasie-Nouvelle-Guinée",
        "language_speakers_decline_velocity_score": 89,
        "state_policy_cultural_erasure_score": 85,
        "digital_exclusion_endangered_language_score": 92,
        "revitalization_resource_deficit_score": 90,
        "primary_pattern": "840 langues dont 200 menacées, politique scolaire anglais-tok pisin, 0 ressources numériques langues minoritaires",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-002",
        "name": "Brésil Amazonie — 180 Langues Isolées, Déforestation Culturicide",
        "country": "Brésil",
        "language_speakers_decline_velocity_score": 93,
        "state_policy_cultural_erasure_score": 88,
        "digital_exclusion_endangered_language_score": 90,
        "revitalization_resource_deficit_score": 91,
        "primary_pattern": "180 langues amazoniennes, 50 locuteurs uniques, déforestation détruit communautés, FUNAI sous-financée",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-003",
        "name": "Sibérie Russie — 30 Langues <100 Locuteurs, Russification Forcée",
        "country": "Russie",
        "language_speakers_decline_velocity_score": 94,
        "state_policy_cultural_erasure_score": 92,
        "digital_exclusion_endangered_language_score": 88,
        "revitalization_resource_deficit_score": 89,
        "primary_pattern": "Nganassane 200 locuteurs, Ket 200 locuteurs, loi 2018 rend enseignement langues autochtones facultatif",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-004",
        "name": "Chine — Tibétain & Ouïghour, Politique Mandarin Forcé",
        "country": "Chine",
        "language_speakers_decline_velocity_score": 87,
        "state_policy_cultural_erasure_score": 95,
        "digital_exclusion_endangered_language_score": 91,
        "revitalization_resource_deficit_score": 86,
        "primary_pattern": "Écoles tibétaines internat séparent enfants parents, classes ouïghours remplacées mandarin, 100+ langues minoritaires effacées",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-005",
        "name": "Australie — Langues Aborigènes, 90% Perdues Depuis Colonisation",
        "country": "Australie",
        "language_speakers_decline_velocity_score": 58,
        "state_policy_cultural_erasure_score": 52,
        "digital_exclusion_endangered_language_score": 55,
        "revitalization_resource_deficit_score": 60,
        "primary_pattern": "250 langues → 120 actives, 13 avec enfants locuteurs, financement AIATSIS insuffisant malgré Stolen Generations excuse",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-006",
        "name": "Mexique — Langues Mayas & Nahuas, Urbanisation Accélère Déclin",
        "country": "Mexique",
        "language_speakers_decline_velocity_score": 55,
        "state_policy_cultural_erasure_score": 48,
        "digital_exclusion_endangered_language_score": 58,
        "revitalization_resource_deficit_score": 54,
        "primary_pattern": "68 langues nationales, exode rural accélère, INALI sous-doté, jeunes abandonnent langue pour espagnol mobile",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-007",
        "name": "Canada — Langues Premières Nations, TRC & Financement Partiel",
        "country": "Canada",
        "language_speakers_decline_velocity_score": 28,
        "state_policy_cultural_erasure_score": 24,
        "digital_exclusion_endangered_language_score": 30,
        "revitalization_resource_deficit_score": 26,
        "primary_pattern": "Loi langues autochtones 2019 adoptée, 500M$ financement limité, Cri & Inuktitut stabilisés, Loi TRC en attente",
        "last_updated": "2026-06-21",
    },
    {
        "id": "ILE-008",
        "name": "Nouvelle-Zélande — Te Reo Māori, Revitalisation Succès Mondial",
        "country": "Nouvelle-Zélande",
        "language_speakers_decline_velocity_score": 7,
        "state_policy_cultural_erasure_score": 5,
        "digital_exclusion_endangered_language_score": 8,
        "revitalization_resource_deficit_score": 6,
        "primary_pattern": "Langue officielle NZ, immersion Kura Kaupapa, TVNZ Māori chaîne nationale, 185K locuteurs +40% 2006-2023",
        "last_updated": "2026-06-21",
    },
]


def compute(e):
    keys = sorted([k for k in e if k.endswith("_score")])
    s = (
        e[keys[0]] * 0.30
        + e[keys[1]] * 0.25
        + e[keys[2]] * 0.25
        + e[keys[3]] * 0.20
    )
    lv = (
        "critique" if s >= 60
        else "élevé" if s >= 40
        else "modéré" if s >= 20
        else "faible"
    )
    return {
        **e,
        "composite_score": round(s, 2),
        "risk_level": lv,
        "estimated_indigenous_language_extinction_index": round(s / 100 * 10, 2),
    }


results = [compute(e) for e in ENTITIES]
dist = {
    l: sum(1 for r in results if r["risk_level"] == l)
    for l in ["critique", "élevé", "modéré", "faible"]
}
avg = sum(r["composite_score"] for r in results) / len(results)

print(f"avg_composite: {avg:.2f}")
print(f"distribution: {dist}")
for r in results:
    print(f"  {r['id']} | {r['composite_score']:.2f} | {r['risk_level']} | {r['estimated_indigenous_language_extinction_index']}")

assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
print("✓ Distribution validée")
print(f"✓ avg_composite = {avg:.2f}")
