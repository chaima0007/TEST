#!/usr/bin/env python3
"""
Migration Governance Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""

AGENT_NAME = "Migration Governance Rights Engine Agent"
ACCENT = "#0284c7"

ENTITIES = [
    ("MGR-001", 99, 97, 96, 94),
    ("MGR-002", 93, 91, 89, 87),
    ("MGR-003", 86, 83, 81, 79),
    ("MGR-004", 79, 76, 74, 72),
    ("MGR-005", 60, 58, 56, 54),
    ("MGR-006", 52, 50, 48, 46),
    ("MGR-007", 32, 30, 28, 26),
    ("MGR-008", 12, 10,  8,  6),
]

# Sub-scores:
#   s1 = border_violence_score               (×0.30)
#   s2 = detention_migration_rights_score    (×0.25)
#   s3 = family_separation_score             (×0.25)
#   s4 = asylum_procedure_failure_score      (×0.20)


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
        estimated_migration_governance_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "border_violence_score": s1,
            "detention_migration_rights_score": s2,
            "family_separation_score": s3,
            "asylum_procedure_failure_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_migration_governance_index": estimated_migration_governance_index,
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
            f"estimated_migration_governance_index={r['estimated_migration_governance_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
