"""
Wave 169 — Land Rights, Eviction & Indigenous Territories Engine
Index: estimated_land_rights_index (0–10)
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

import json

ENTITIES = [
    {
        "id": "LRE-001",
        "name": "Brésil Amazonie",
        "description": "Déforestation + garimpo, territoires Yanomami envahis, Lula action tardive",
        "sub1_forced_eviction_scale": 88,
        "sub2_indigenous_territorial_rights_violation": 92,
        "sub3_corporate_land_grabbing": 88,
        "sub4_legal_protection_gap": 84,
    },
    {
        "id": "LRE-002",
        "name": "RDC",
        "description": "Grandes plantations agro, déplacements communautés, impunité entreprises",
        "sub1_forced_eviction_scale": 86,
        "sub2_indigenous_territorial_rights_violation": 80,
        "sub3_corporate_land_grabbing": 84,
        "sub4_legal_protection_gap": 78,
    },
    {
        "id": "LRE-003",
        "name": "Indonésie",
        "description": "Palmier huile Kalimantan/Sumatra, Dayak/Orang Rimba expulsés",
        "sub1_forced_eviction_scale": 80,
        "sub2_indigenous_territorial_rights_violation": 82,
        "sub3_corporate_land_grabbing": 84,
        "sub4_legal_protection_gap": 76,
    },
    {
        "id": "LRE-004",
        "name": "Éthiopie",
        "description": "Villagisation Gambella, grandes fermes Dubai/Saoudiens, displacement",
        "sub1_forced_eviction_scale": 76,
        "sub2_indigenous_territorial_rights_violation": 72,
        "sub3_corporate_land_grabbing": 70,
        "sub4_legal_protection_gap": 68,
    },
    {
        "id": "LRE-005",
        "name": "Cambodge",
        "description": "Concessionnaires sucre EBA, 400K déplacés, UE sanctions partielles",
        "sub1_forced_eviction_scale": 55,
        "sub2_indigenous_territorial_rights_violation": 52,
        "sub3_corporate_land_grabbing": 56,
        "sub4_legal_protection_gap": 50,
    },
    {
        "id": "LRE-006",
        "name": "Kenya Maasai",
        "description": "Expulsions safari/tourisme, Ngorongoro héritage",
        "sub1_forced_eviction_scale": 46,
        "sub2_indigenous_territorial_rights_violation": 50,
        "sub3_corporate_land_grabbing": 44,
        "sub4_legal_protection_gap": 42,
    },
    {
        "id": "LRE-007",
        "name": "Philippines",
        "description": "FPIC bafoué, mines Mindanao, Lumad expulsions",
        "sub1_forced_eviction_scale": 28,
        "sub2_indigenous_territorial_rights_violation": 30,
        "sub3_corporate_land_grabbing": 26,
        "sub4_legal_protection_gap": 24,
    },
    {
        "id": "LRE-008",
        "name": "Bolivie",
        "description": "Consultation préalable FPIC respectée, autonomie territoriale TIPNIS",
        "sub1_forced_eviction_scale": 9,
        "sub2_indigenous_territorial_rights_violation": 8,
        "sub3_corporate_land_grabbing": 7,
        "sub4_legal_protection_gap": 6,
    },
]


def compute_scores(entities):
    results = []
    for e in entities:
        sub1 = e["sub1_forced_eviction_scale"]
        sub2 = e["sub2_indigenous_territorial_rights_violation"]
        sub3 = e["sub3_corporate_land_grabbing"]
        sub4 = e["sub4_legal_protection_gap"]

        composite_score = sub1 * 0.30 + sub2 * 0.25 + sub3 * 0.25 + sub4 * 0.20

        if composite_score >= 60:
            severity = "critique"
        elif composite_score >= 40:
            severity = "élevé"
        elif composite_score >= 20:
            severity = "modéré"
        else:
            severity = "faible"

        estimated_land_rights_index = round(composite_score / 100 * 10, 2)

        results.append({
            "id": e["id"],
            "name": e["name"],
            "description": e["description"],
            "sub1_forced_eviction_scale": sub1,
            "sub2_indigenous_territorial_rights_violation": sub2,
            "sub3_corporate_land_grabbing": sub3,
            "sub4_legal_protection_gap": sub4,
            "composite_score": round(composite_score, 2),
            "severity": severity,
            "estimated_land_rights_index": estimated_land_rights_index,
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
    print("WAVE 169 — Land Rights, Eviction & Indigenous Territories Engine")
    print("=" * 70)

    for r in results:
        print(
            f"[{r['id']}] {r['name']:<30} "
            f"composite={r['composite_score']:>6.2f}  "
            f"index={r['estimated_land_rights_index']:>5.2f}  "
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
