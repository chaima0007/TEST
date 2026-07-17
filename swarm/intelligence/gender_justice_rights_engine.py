#!/usr/bin/env python3
"""
Gender Justice Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""

AGENT_NAME = "Gender Justice Rights Engine Agent"
ACCENT = "#db2777"

ENTITIES = [
    ("GJR-001", 99, 97, 96, 94),
    ("GJR-002", 93, 91, 89, 87),
    ("GJR-003", 86, 83, 81, 79),
    ("GJR-004", 79, 76, 74, 72),
    ("GJR-005", 60, 58, 56, 54),
    ("GJR-006", 52, 50, 48, 46),
    ("GJR-007", 32, 30, 28, 26),
    ("GJR-008", 12, 10,  8,  6),
]

# Sub-scores:
#   s1 = gender_based_violence_impunity_score   (×0.30)
#   s2 = femicide_rate_score                    (×0.25)
#   s3 = legal_gender_discrimination_score      (×0.25)
#   s4 = gender_justice_access_gap_score        (×0.20)


def calculate_composite(s1, s2, s3, s4):
    return round(s1 * 0.30 + s2 * 0.25 + s3 * 0.25 + s4 * 0.20, 2)


def classify_risk(score):
    if score >= 60:
        return "critique"
    elif score >= 40:
        return "élevé"
    elif score >= 20:
        return "modéré"
    return "faible"


def run_engine():
    results = []
    for (eid, s1, s2, s3, s4) in ENTITIES:
        composite = calculate_composite(s1, s2, s3, s4)
        risk = classify_risk(composite)
        estimated_gender_justice_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "gender_based_violence_impunity_score": s1,
            "femicide_rate_score": s2,
            "legal_gender_discrimination_score": s3,
            "gender_justice_access_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_gender_justice_index": estimated_gender_justice_index,
        })

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']}: {r['composite_score']} "
            f"[{r['risk_level']}] "
            f"estimated_gender_justice_index={r['estimated_gender_justice_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
