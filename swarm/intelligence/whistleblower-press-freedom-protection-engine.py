"""
Wave 183 — Whistleblower & Press Freedom Protection Engine
Caelum Partners · IDs : WPF-001 à WPF-008
Distribution : 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json
from datetime import datetime

entities_raw = [
    {
        "id": "WPF-001",
        "name": "Mexique/Journalistes Cartels — 15 Tués 2023, Mécanisme Protection Inefficace",
        "sub1": 93, "sub2": 89, "sub3": 87, "sub4": 84,
        "risk_level": "critique",
    },
    {
        "id": "WPF-002",
        "name": "Russie/Loi Anti-Fake News — Journalistes 15 Ans Prison, Médias Indépendants Fermés",
        "sub1": 97, "sub2": 94, "sub3": 92, "sub4": 90,
        "risk_level": "critique",
    },
    {
        "id": "WPF-003",
        "name": "Philippines/Rodrigo Duterte Rappler — Maria Ressa Nobel Harcelée",
        "sub1": 86, "sub2": 82, "sub3": 80, "sub4": 76,
        "risk_level": "critique",
    },
    {
        "id": "WPF-004",
        "name": "Éthiopie/Tigray War Media Blackout — Internet Coupé, Journalistes Expulsés",
        "sub1": 74, "sub2": 70, "sub3": 67, "sub4": 63,
        "risk_level": "critique",
    },
    {
        "id": "WPF-005",
        "name": "UE/SLAPP Lois Bâillon — 570 Cas Documentés, PME Journalisme Menacées",
        "sub1": 56, "sub2": 52, "sub3": 50, "sub4": 46,
        "risk_level": "élevé",
    },
    {
        "id": "WPF-006",
        "name": "USA/Julian Assange 12 Ans Extradition — Espionnage Act, Précédent Dangereux",
        "sub1": 53, "sub2": 49, "sub3": 47, "sub4": 43,
        "risk_level": "élevé",
    },
    {
        "id": "WPF-007",
        "name": "France/Protection Sources Partielle — Loi 2010 Insuffisante, Whistleblowers UE Exposés",
        "sub1": 33, "sub2": 29, "sub3": 27, "sub4": 23,
        "risk_level": "modéré",
    },
    {
        "id": "WPF-008",
        "name": "Islande/International Modern Media Institute — Meilleure Protection Lances-Alertes",
        "sub1": 16, "sub2": 12, "sub3": 10, "sub4": 8,
        "risk_level": "faible",
    },
]

entities = []
for e in entities_raw:
    composite = round(
        e["sub1"] * 0.30 + e["sub2"] * 0.25 + e["sub3"] * 0.25 + e["sub4"] * 0.20, 2
    )
    estimated_press_freedom_index = round(composite / 100 * 10, 2)
    entities.append({
        "id": e["id"],
        "name": e["name"],
        "composite_score": composite,
        "risk_level": e["risk_level"],
        "estimated_press_freedom_index": estimated_press_freedom_index,
    })

avg_composite = round(sum(e["composite_score"] for e in entities) / len(entities), 2)

risk_distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
for e in entities:
    risk_distribution[e["risk_level"]] += 1

result = {
    "domain": "whistleblower-press-freedom-protection-engine",
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
