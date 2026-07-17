"""
Wave 183 — Disability Rights & Inclusive Development Engine
Caelum Partners · IDs : DBR-001 à DBR-008
Distribution : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json
from datetime import datetime

entities_raw = [
    {
        "id": "DBR-001",
        "name": "Congo/Personnes Handicapées Mines Antipersonnel — Amputés Sans Prothèses, ONG Manquent",
        "sub1": 95, "sub2": 90, "sub3": 88, "sub4": 85,
        "risk_level": "critique",
    },
    {
        "id": "DBR-002",
        "name": "Afghanistan/Femmes Handicapées Talibans — Double Discrimination, Éducation Interdite",
        "sub1": 97, "sub2": 93, "sub3": 91, "sub4": 89,
        "risk_level": "critique",
    },
    {
        "id": "DBR-003",
        "name": "Inde/Institutionnalisation Forcée Autistes — Chaînes Pratiques Traditionnelles",
        "sub1": 88, "sub2": 84, "sub3": 82, "sub4": 78,
        "risk_level": "critique",
    },
    {
        "id": "DBR-004",
        "name": "USA/Olmstead Act Non-Appliqué — Intégration Communautaire Retardée",
        "sub1": 72, "sub2": 68, "sub3": 65, "sub4": 62,
        "risk_level": "critique",
    },
    {
        "id": "DBR-005",
        "name": "Brésil/Accessibilité Zéro Favelas — 30% Population Exclu Transports",
        "sub1": 58, "sub2": 54, "sub3": 52, "sub4": 48,
        "risk_level": "élevé",
    },
    {
        "id": "DBR-006",
        "name": "Nigeria/Witchcraft Accusations Handicap Mental — Exorcismes Forcés",
        "sub1": 55, "sub2": 51, "sub3": 49, "sub4": 45,
        "risk_level": "élevé",
    },
    {
        "id": "DBR-007",
        "name": "UE/CRPD Ratification Partielle — 12 États Réserves, Progrès Modéré",
        "sub1": 35, "sub2": 30, "sub3": 28, "sub4": 25,
        "risk_level": "modéré",
    },
    {
        "id": "DBR-008",
        "name": "Japon/Universal Design Pioneer — Accessibilité Systémique",
        "sub1": 18, "sub2": 14, "sub3": 12, "sub4": 10,
        "risk_level": "faible",
    },
]

entities = []
for e in entities_raw:
    composite = round(
        e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20, 2
    )
    estimated_disability_rights_index = round(composite / 100 * 10, 2)
    entities.append({
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": e["risk_level"],
        "estimated_disability_rights_index": estimated_disability_rights_index,
    })

avg_composite = round(sum(e["composite_score"] for e in entities) / len(entities), 2)

risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
for e in entities:
    risk_distribution[e["risk_level"]] += 1

result = {
    "domain": "disability-rights-inclusive-development-engine",
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
