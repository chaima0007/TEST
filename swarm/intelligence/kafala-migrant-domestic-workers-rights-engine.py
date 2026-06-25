"""
Wave 183 — Kafala & Migrant Domestic Workers Rights Engine
Caelum Partners · IDs : KMD-001 à KMD-008
Distribution : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json
from datetime import datetime

entities_raw = [
    {
        "id": "KMD-001",
        "name": "Arabie Saoudite/Kafala 2.5M Travailleurs — Passeports Confisqués, Esclavage Légal",
        "sub1": 96, "sub2": 93, "sub3": 91, "sub4": 88,
        "risk_level": "critique",
    },
    {
        "id": "KMD-002",
        "name": "Qatar/Coupe 2022 Migrants Morts — 6 500 Morts Chantier",
        "sub1": 98, "sub2": 95, "sub3": 92, "sub4": 90,
        "risk_level": "critique",
    },
    {
        "id": "KMD-003",
        "name": "Liban/Travailleuses Éthiopiennes — Vidéos Abandons Aéroport, Suicide Prévalent",
        "sub1": 90, "sub2": 86, "sub3": 84, "sub4": 80,
        "risk_level": "critique",
    },
    {
        "id": "KMD-004",
        "name": "UAE/Philippines OFW Exploitation — Salaires Volés, Aucun Recours Légal",
        "sub1": 75, "sub2": 71, "sub3": 68, "sub4": 65,
        "risk_level": "critique",
    },
    {
        "id": "KMD-005",
        "name": "Jordanie/Réforme Kafala Partielle — 660K Travailleurs, Améliorations Limitées",
        "sub1": 57, "sub2": 53, "sub3": 50, "sub4": 47,
        "risk_level": "élevé",
    },
    {
        "id": "KMD-006",
        "name": "Bahreïn/Corridor Migration — Réformes 2021 Inégalement Appliquées",
        "sub1": 52, "sub2": 48, "sub3": 46, "sub4": 42,
        "risk_level": "élevé",
    },
    {
        "id": "KMD-007",
        "name": "Oman/Kafala Progressif — Changement Patronal Autorisé Partiellement",
        "sub1": 34, "sub2": 30, "sub3": 28, "sub4": 24,
        "risk_level": "modéré",
    },
    {
        "id": "KMD-008",
        "name": "Canada/Caregiver Pathway — Droits Résidence Domestiques Étrangers",
        "sub1": 17, "sub2": 13, "sub3": 11, "sub4": 9,
        "risk_level": "faible",
    },
]

entities = []
for e in entities_raw:
    composite = round(
        e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20, 2
    )
    estimated_kafala_migrant_index = round(composite / 100 * 10, 2)
    entities.append({
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": e["risk_level"],
        "estimated_kafala_migrant_index": estimated_kafala_migrant_index,
    })

avg_composite = round(sum(e["composite_score"] for e in entities) / len(entities), 2)

risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
for e in entities:
    risk_distribution[e["risk_level"]] += 1

result = {
    "domain": "kafala-migrant-domestic-workers-rights-engine",
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "entities": entities,
    "avg_composite": avg_composite,
    "risk_distribution": risk_distribution,
}

print(json.dumps(result, indent=2, ensure_ascii=False))
print(f"\navg_composite: {avg_composite}")
print(f"risk_distribution: {risk_distribution}")

# Assertions distribution obligatoire
assert risk_distribution["critique"] == 4, f"Expected 4 critique, got {risk_distribution['critique']}"
assert risk_distribution["élevé"] == 2, f"Expected 2 élevé, got {risk_distribution['élevé']}"
assert risk_distribution["modéré"] == 1, f"Expected 1 modéré, got {risk_distribution['modéré']}"
assert risk_distribution["faible"] == 1, f"Expected 1 faible, got {risk_distribution['faible']}"

# Assertions seuils
for e in entities:
    s = e["composite_score"]
    lvl = e["risk_level"]
    if lvl == "critique":
        assert s >= 60, f"{e['id']} critique but score {s} < 60"
    elif lvl == "élevé":
        assert 40 <= s < 60, f"{e['id']} élevé but score {s} not in [40,60)"
    elif lvl == "modéré":
        assert 20 <= s < 40, f"{e['id']} modéré but score {s} not in [20,40)"
    elif lvl == "faible":
        assert s < 20, f"{e['id']} faible but score {s} >= 20"

print("\nAll assertions passed.")
