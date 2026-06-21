"""
post_quantum_cryptography_rights_engine.py
Wave 188 — Cryptographie Post-Quantique & Protection des Communications
"""

ENTITIES = [
    {
        "id": "PQC-001",
        "name": "Populations Sans Post-Quantum",
        "cryptographic_vulnerability_exposure_score": 93,
        "harvest_now_decrypt_later_risk_score": 97,
        "migration_timeline_urgency_score": 89,
        "rights_protection_pqc_deficit_score": 91,
    },
    {
        "id": "PQC-002",
        "name": "Systèmes Santé Non-Protégés",
        "cryptographic_vulnerability_exposure_score": 88,
        "harvest_now_decrypt_later_risk_score": 91,
        "migration_timeline_urgency_score": 86,
        "rights_protection_pqc_deficit_score": 87,
    },
    {
        "id": "PQC-003",
        "name": "Journalistes/Sources à Risque",
        "cryptographic_vulnerability_exposure_score": 84,
        "harvest_now_decrypt_later_risk_score": 88,
        "migration_timeline_urgency_score": 91,
        "rights_protection_pqc_deficit_score": 93,
    },
    {
        "id": "PQC-004",
        "name": "Infrastructures Critiques RSA",
        "cryptographic_vulnerability_exposure_score": 79,
        "harvest_now_decrypt_later_risk_score": 83,
        "migration_timeline_urgency_score": 88,
        "rights_protection_pqc_deficit_score": 76,
    },
    {
        "id": "PQC-005",
        "name": "Gouvernements Transition Lente",
        "cryptographic_vulnerability_exposure_score": 48,
        "harvest_now_decrypt_later_risk_score": 52,
        "migration_timeline_urgency_score": 62,
        "rights_protection_pqc_deficit_score": 44,
    },
    {
        "id": "PQC-006",
        "name": "NIST PQC Standards 2024",
        "cryptographic_vulnerability_exposure_score": 14,
        "harvest_now_decrypt_later_risk_score": 18,
        "migration_timeline_urgency_score": 22,
        "rights_protection_pqc_deficit_score": 16,
    },
    {
        "id": "PQC-007",
        "name": "Signal Protocol Post-Quantum",
        "cryptographic_vulnerability_exposure_score": 20,
        "harvest_now_decrypt_later_risk_score": 24,
        "migration_timeline_urgency_score": 28,
        "rights_protection_pqc_deficit_score": 18,
    },
    {
        "id": "PQC-008",
        "name": "Nations Avancées PQC",
        "cryptographic_vulnerability_exposure_score": 42,
        "harvest_now_decrypt_later_risk_score": 38,
        "migration_timeline_urgency_score": 44,
        "rights_protection_pqc_deficit_score": 36,
    },
]


def compute_composite(e):
    return (
        e["cryptographic_vulnerability_exposure_score"] * 0.30
        + e["harvest_now_decrypt_later_risk_score"] * 0.25
        + e["migration_timeline_urgency_score"] * 0.25
        + e["rights_protection_pqc_deficit_score"] * 0.20
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
            "cryptographic_vulnerability_exposure_score": e["cryptographic_vulnerability_exposure_score"],
            "harvest_now_decrypt_later_risk_score": e["harvest_now_decrypt_later_risk_score"],
            "migration_timeline_urgency_score": e["migration_timeline_urgency_score"],
            "rights_protection_pqc_deficit_score": e["rights_protection_pqc_deficit_score"],
            "estimated_pqc_rights_index": index,
        })

    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        dist[r["risk_level"]] += 1

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)

    print("=== Post-Quantum Cryptography Rights Engine — Wave 188 ===")
    for r in results:
        print(f"  {r['id']} | {r['name'][:40]:<40} | score={r['composite_score']:5.2f} | {r['risk_level']:<8} | index={r['estimated_pqc_rights_index']}")
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
