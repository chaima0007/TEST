"""
Wave 169 — Arbitrary Detention & Political Prisoners Engine
Index: estimated_arbitrary_detention_index (0–10)
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "ADP-001",
        "name": "Chine Xinjiang",
        "description": "1M+ internés camps formation, procès inexistants, surveillance totale",
        "sub1_detention_scale_political": 97,
        "sub2_due_process_violation": 95,
        "sub3_torture_ill_treatment": 93,
        "sub4_international_monitoring_obstruction": 96,
    },
    {
        "id": "ADP-002",
        "name": "Corée du Nord",
        "description": "Goulags politiques, 3 générations punies, 80K-120K détenus",
        "sub1_detention_scale_political": 94,
        "sub2_due_process_violation": 96,
        "sub3_torture_ill_treatment": 95,
        "sub4_international_monitoring_obstruction": 92,
    },
    {
        "id": "ADP-003",
        "name": "Russie",
        "description": "Opposants depuis 2022, Navalny mort, milliers détenus manifestants",
        "sub1_detention_scale_political": 82,
        "sub2_due_process_violation": 80,
        "sub3_torture_ill_treatment": 78,
        "sub4_international_monitoring_obstruction": 76,
    },
    {
        "id": "ADP-004",
        "name": "Iran",
        "description": "Depuis 2009 Green Movement, 2022 Mahsa Amini, 15K+ détenus",
        "sub1_detention_scale_political": 74,
        "sub2_due_process_violation": 72,
        "sub3_torture_ill_treatment": 76,
        "sub4_international_monitoring_obstruction": 70,
    },
    {
        "id": "ADP-005",
        "name": "Venezuela Maduro",
        "description": "Opposants, journalistes, militaires dissidents, 300+ pol.",
        "sub1_detention_scale_political": 56,
        "sub2_due_process_violation": 54,
        "sub3_torture_ill_treatment": 52,
        "sub4_international_monitoring_obstruction": 50,
    },
    {
        "id": "ADP-006",
        "name": "Belarus Loukachenko",
        "description": "15K+ post-2020, torture systématique, Viasna",
        "sub1_detention_scale_political": 48,
        "sub2_due_process_violation": 50,
        "sub3_torture_ill_treatment": 54,
        "sub4_international_monitoring_obstruction": 46,
    },
    {
        "id": "ADP-007",
        "name": "Egypte",
        "description": "60K+ prisonniers politiques estimés, processus judiciaires limités",
        "sub1_detention_scale_political": 30,
        "sub2_due_process_violation": 28,
        "sub3_torture_ill_treatment": 32,
        "sub4_international_monitoring_obstruction": 26,
    },
    {
        "id": "ADP-008",
        "name": "Finlande",
        "description": "0 prisonnier politique, accès CICR total, HRC monitoring ouvert",
        "sub1_detention_scale_political": 5,
        "sub2_due_process_violation": 4,
        "sub3_torture_ill_treatment": 3,
        "sub4_international_monitoring_obstruction": 4,
    },
]


def compute_scores(entities):
    results = []
    for e in entities:
        sub1 = e["sub1_detention_scale_political"]
        sub2 = e["sub2_due_process_violation"]
        sub3 = e["sub3_torture_ill_treatment"]
        sub4 = e["sub4_international_monitoring_obstruction"]

        composite_score = sub1 * 0.30 + sub2 * 0.25 + sub3 * 0.25 + sub4 * 0.20

        if composite_score >= 60:
            severity = "critique"
        elif composite_score >= 40:
            severity = "élevé"
        elif composite_score >= 20:
            severity = "modéré"
        else:
            severity = "faible"

        estimated_arbitrary_detention_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": e["id"],
            "name": e["name"],
            "description": e["description"],
            "sub1_detention_scale_political": sub1,
            "sub2_due_process_violation": sub2,
            "sub3_torture_ill_treatment": sub3,
            "sub4_international_monitoring_obstruction": sub4,
            "composite_score": round(composite_score, 2),
            "severity": severity,
            "estimated_arbitrary_detention_index": estimated_arbitrary_detention_index,
        })
    return results


def validate_distribution(results):
    counts = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for r in results:
        counts[r["severity"]] += 1
    expected = {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}
    ok = counts == expected
    return ok, counts


def main():
    results = compute_scores(ENTITIES)
    avg_composite = sum(r["composite_score"] for r in results) / len(results)

    print("=" * 70)
    print("WAVE 169 — Arbitrary Detention & Political Prisoners Engine")
    print("=" * 70)

    for r in results:
        print(
            f"[{r['id']}] {r['name']:<30} "
            f"composite={r['composite_score']:>6.2f}  "
            f"index={r['estimated_arbitrary_detention_index']:>5.2f}  "
            f"[{r['severity']}]"
        )

    print("-" * 70)
    print(f"avg_composite = {avg_composite:.2f}")

    ok, counts = validate_distribution(results)
    print(f"Distribution: {counts}")
    if ok:
        print("✓ Distribution 4 critique / 2 élevé / 1 modéré / 1 faible — OK")
    else:
        print("✗ Distribution incorrecte!")

    print("=" * 70)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return results


if __name__ == "__main__":
    main()
