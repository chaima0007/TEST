"""
Wave 169 — Trafficking, Forced Labor & Modern Slavery Engine
Index: estimated_modern_slavery_index (0–10)
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "TFM-001",
        "name": "Corée du Nord",
        "description": "Travail forcé d'État export, usines Chine/Russie, 50K-100K workers",
        "sub1_victim_scale_exploitation": 96,
        "sub2_trafficking_network_impunity": 95,
        "sub3_labor_exploitation_supply_chain": 94,
        "sub4_victim_protection_gap": 90,
    },
    {
        "id": "TFM-002",
        "name": "Qatar FIFA2022",
        "description": "Kafala, 6500 morts travailleurs migrants, réformes insuffisantes",
        "sub1_victim_scale_exploitation": 88,
        "sub2_trafficking_network_impunity": 84,
        "sub3_labor_exploitation_supply_chain": 90,
        "sub4_victim_protection_gap": 82,
    },
    {
        "id": "TFM-003",
        "name": "Libye",
        "description": "Marchés aux esclaves 2017, migrants subsahariens, impunité milices",
        "sub1_victim_scale_exploitation": 85,
        "sub2_trafficking_network_impunity": 88,
        "sub3_labor_exploitation_supply_chain": 80,
        "sub4_victim_protection_gap": 84,
    },
    {
        "id": "TFM-004",
        "name": "Inde briqueteries/pêche",
        "description": "Bonded labour, 8M+ en servitude dette, lois peu appliquées",
        "sub1_victim_scale_exploitation": 78,
        "sub2_trafficking_network_impunity": 72,
        "sub3_labor_exploitation_supply_chain": 76,
        "sub4_victim_protection_gap": 70,
    },
    {
        "id": "TFM-005",
        "name": "Mexique",
        "description": "Femmes trafiquées cartels, corridors Centramérique-USA",
        "sub1_victim_scale_exploitation": 56,
        "sub2_trafficking_network_impunity": 54,
        "sub3_labor_exploitation_supply_chain": 50,
        "sub4_victim_protection_gap": 52,
    },
    {
        "id": "TFM-006",
        "name": "Thaïlande industrie pêche",
        "description": "Travailleurs migrants piégés, ILO rapports",
        "sub1_victim_scale_exploitation": 48,
        "sub2_trafficking_network_impunity": 46,
        "sub3_labor_exploitation_supply_chain": 50,
        "sub4_victim_protection_gap": 44,
    },
    {
        "id": "TFM-007",
        "name": "Roumanie/Bulgarie",
        "description": "Trafic intra-UE, jeunes femmes, dispositifs partiels",
        "sub1_victim_scale_exploitation": 28,
        "sub2_trafficking_network_impunity": 26,
        "sub3_labor_exploitation_supply_chain": 24,
        "sub4_victim_protection_gap": 22,
    },
    {
        "id": "TFM-008",
        "name": "Suède modèle",
        "description": "Loi 1999 criminalise acheteur, réduction prouvée, réintégration",
        "sub1_victim_scale_exploitation": 8,
        "sub2_trafficking_network_impunity": 6,
        "sub3_labor_exploitation_supply_chain": 7,
        "sub4_victim_protection_gap": 5,
    },
]


def compute_scores(entities):
    results = []
    for e in entities:
        sub1 = e["sub1_victim_scale_exploitation"]
        sub2 = e["sub2_trafficking_network_impunity"]
        sub3 = e["sub3_labor_exploitation_supply_chain"]
        sub4 = e["sub4_victim_protection_gap"]

        composite_score = sub1 * 0.30 + sub2 * 0.25 + sub3 * 0.25 + sub4 * 0.20

        if composite_score >= 60:
            severity = "critique"
        elif composite_score >= 40:
            severity = "élevé"
        elif composite_score >= 20:
            severity = "modéré"
        else:
            severity = "faible"

        estimated_modern_slavery_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": e["id"],
            "name": e["name"],
            "description": e["description"],
            "sub1_victim_scale_exploitation": sub1,
            "sub2_trafficking_network_impunity": sub2,
            "sub3_labor_exploitation_supply_chain": sub3,
            "sub4_victim_protection_gap": sub4,
            "composite_score": round(composite_score, 2),
            "severity": severity,
            "estimated_modern_slavery_index": estimated_modern_slavery_index,
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
    print("WAVE 169 — Trafficking, Forced Labor & Modern Slavery Engine")
    print("=" * 70)

    for r in results:
        print(
            f"[{r['id']}] {r['name']:<30} "
            f"composite={r['composite_score']:>6.2f}  "
            f"index={r['estimated_modern_slavery_index']:>5.2f}  "
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
