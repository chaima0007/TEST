"""
quantum_supremacy_arms_race_engine.py
Wave 188 — Course à la Suprématie Quantique & Droits Humains
"""

ENTITIES = [
    {
        "id": "QSA-001",
        "name": "Chine/Quantum Leap",
        "quantum_military_advantage_weaponization_score": 91,
        "technological_monopoly_access_inequality_score": 87,
        "international_cooperation_deficit_score": 89,
        "human_rights_quantum_impact_score": 84,
    },
    {
        "id": "QSA-002",
        "name": "USA/IBM-Google Race",
        "quantum_military_advantage_weaponization_score": 86,
        "technological_monopoly_access_inequality_score": 79,
        "international_cooperation_deficit_score": 72,
        "human_rights_quantum_impact_score": 68,
    },
    {
        "id": "QSA-003",
        "name": "Course Militaire Quantum",
        "quantum_military_advantage_weaponization_score": 94,
        "technological_monopoly_access_inequality_score": 83,
        "international_cooperation_deficit_score": 91,
        "human_rights_quantum_impact_score": 88,
    },
    {
        "id": "QSA-004",
        "name": "Monopolisation Brevets",
        "quantum_military_advantage_weaponization_score": 62,
        "technological_monopoly_access_inequality_score": 93,
        "international_cooperation_deficit_score": 84,
        "human_rights_quantum_impact_score": 79,
    },
    {
        "id": "QSA-005",
        "name": "UE/Quantum Flagship",
        "quantum_military_advantage_weaponization_score": 38,
        "technological_monopoly_access_inequality_score": 52,
        "international_cooperation_deficit_score": 44,
        "human_rights_quantum_impact_score": 41,
    },
    {
        "id": "QSA-006",
        "name": "Pays Émergents Exclus",
        "quantum_military_advantage_weaponization_score": 42,
        "technological_monopoly_access_inequality_score": 58,
        "international_cooperation_deficit_score": 52,
        "human_rights_quantum_impact_score": 48,
    },
    {
        "id": "QSA-007",
        "name": "Canada/Quantum Safe",
        "quantum_military_advantage_weaponization_score": 22,
        "technological_monopoly_access_inequality_score": 28,
        "international_cooperation_deficit_score": 18,
        "human_rights_quantum_impact_score": 24,
    },
    {
        "id": "QSA-008",
        "name": "CERN/Quantum Science",
        "quantum_military_advantage_weaponization_score": 9,
        "technological_monopoly_access_inequality_score": 12,
        "international_cooperation_deficit_score": 6,
        "human_rights_quantum_impact_score": 8,
    },
]


def compute_composite(e):
    return (
        e["quantum_military_advantage_weaponization_score"] * 0.30
        + e["technological_monopoly_access_inequality_score"] * 0.25
        + e["international_cooperation_deficit_score"] * 0.25
        + e["human_rights_quantum_impact_score"] * 0.20
    )


def risk_level(score):
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    else:
        return "faible"


def main():
    results = []
    for e in ENTITIES:
        composite = round(compute_composite(e), 2)
        level = risk_level(composite)
        index = round(composite / 100 * 10, 2)
        results.append({
            "id": e["id"],
            "name": e["name"],
            "composite_score": composite,
            "risk_level": level,
            "quantum_military_advantage_weaponization_score": e["quantum_military_advantage_weaponization_score"],
            "technological_monopoly_access_inequality_score": e["technological_monopoly_access_inequality_score"],
            "international_cooperation_deficit_score": e["international_cooperation_deficit_score"],
            "human_rights_quantum_impact_score": e["human_rights_quantum_impact_score"],
            "estimated_quantum_supremacy_rights_index": index,
        })

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=== Quantum Supremacy Arms Race Engine — Wave 188 ===")
    for r in results:
        print(f"  {r['id']} | {r['name'][:40]:<40} | score={r['composite_score']:5.2f} | {r['risk_level']:<8} | index={r['estimated_quantum_supremacy_rights_index']}")
    print(f"\navg_composite: {avg}")
    print(f"distribution: {dist}")
    assert dist["critique"] == 4, f"Expected 4 critique, got {dist['critique']}"
    assert dist["élevé"] == 2, f"Expected 2 élevé, got {dist['élevé']}"
    assert dist["modéré"] == 1, f"Expected 1 modéré, got {dist['modéré']}"
    assert dist["faible"] == 1, f"Expected 1 faible, got {dist['faible']}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")
    print(f"✓ avg_composite = {avg}")
    return results


if __name__ == "__main__":
    main()
