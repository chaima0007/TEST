"""
quantum_surveillance_privacy_rights_engine.py
Wave 188 — Surveillance Quantique & Droit à la Vie Privée
"""

ENTITIES = [
    {
        "id": "QSP-001",
        "name": "Chine/Quantum Radar & Satellite",
        "quantum_surveillance_capability_score": 94,
        "privacy_rights_protection_deficit_score": 96,
        "legal_framework_quantum_gap_score": 91,
        "civilian_oversight_accountability_score": 88,
    },
    {
        "id": "QSP-002",
        "name": "USA/NSA Quantum",
        "quantum_surveillance_capability_score": 91,
        "privacy_rights_protection_deficit_score": 78,
        "legal_framework_quantum_gap_score": 82,
        "civilian_oversight_accountability_score": 69,
    },
    {
        "id": "QSP-003",
        "name": "Russie/FSB Quantum",
        "quantum_surveillance_capability_score": 78,
        "privacy_rights_protection_deficit_score": 89,
        "legal_framework_quantum_gap_score": 84,
        "civilian_oversight_accountability_score": 82,
    },
    {
        "id": "QSP-004",
        "name": "Israël/Unit 8200 Quantum",
        "quantum_surveillance_capability_score": 86,
        "privacy_rights_protection_deficit_score": 91,
        "legal_framework_quantum_gap_score": 79,
        "civilian_oversight_accountability_score": 73,
    },
    {
        "id": "QSP-005",
        "name": "UE/GDPR Quantum Gap",
        "quantum_surveillance_capability_score": 52,
        "privacy_rights_protection_deficit_score": 48,
        "legal_framework_quantum_gap_score": 57,
        "civilian_oversight_accountability_score": 41,
    },
    {
        "id": "QSP-006",
        "name": "Inde/DRDO Quantum",
        "quantum_surveillance_capability_score": 47,
        "privacy_rights_protection_deficit_score": 58,
        "legal_framework_quantum_gap_score": 52,
        "civilian_oversight_accountability_score": 44,
    },
    {
        "id": "QSP-007",
        "name": "Canada/Quantum Valley",
        "quantum_surveillance_capability_score": 38,
        "privacy_rights_protection_deficit_score": 26,
        "legal_framework_quantum_gap_score": 31,
        "civilian_oversight_accountability_score": 22,
    },
    {
        "id": "QSP-008",
        "name": "ISO/IEC Quantum Privacy",
        "quantum_surveillance_capability_score": 12,
        "privacy_rights_protection_deficit_score": 8,
        "legal_framework_quantum_gap_score": 15,
        "civilian_oversight_accountability_score": 10,
    },
]


def compute_composite(e):
    return (
        e["quantum_surveillance_capability_score"] * 0.30
        + e["privacy_rights_protection_deficit_score"] * 0.25
        + e["legal_framework_quantum_gap_score"] * 0.25
        + e["civilian_oversight_accountability_score"] * 0.20
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
            "quantum_surveillance_capability_score": e["quantum_surveillance_capability_score"],
            "privacy_rights_protection_deficit_score": e["privacy_rights_protection_deficit_score"],
            "legal_framework_quantum_gap_score": e["legal_framework_quantum_gap_score"],
            "civilian_oversight_accountability_score": e["civilian_oversight_accountability_score"],
            "estimated_quantum_surveillance_rights_index": index,
        })

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=== Quantum Surveillance Privacy Rights Engine — Wave 188 ===")
    for r in results:
        print(f"  {r['id']} | {r['name'][:40]:<40} | score={r['composite_score']:5.2f} | {r['risk_level']:<8} | index={r['estimated_quantum_surveillance_rights_index']}")
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
