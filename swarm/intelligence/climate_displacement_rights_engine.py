#!/usr/bin/env python3
"""
Climate Displacement Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random

random.seed(42)

AGENT_NAME = "Climate Displacement Rights Engine Agent"
ACCENT_COLOR = "#15803d"

ENTITIES = [
    # (id, climate_forced_migration_score, sea_level_displacement_score, drought_land_loss_score, climate_refugee_protection_gap_score)
    ("CDR-001", 99, 97, 95, 93),  # critique — déplacements climatiques massifs documentés
    ("CDR-002", 91, 89, 87, 85),  # critique — montée des eaux, populations entières déplacées
    ("CDR-003", 83, 81, 79, 77),  # critique — sécheresses extrêmes, pertes agricoles critiques
    ("CDR-004", 75, 73, 71, 69),  # critique — vide juridique protection réfugiés climatiques
    ("CDR-005", 58, 56, 54, 52),  # élevé — déplacements saisonniers récurrents
    ("CDR-006", 49, 47, 45, 43),  # élevé — vulnérabilité côtière partielle
    ("CDR-007", 35, 33, 31, 29),  # modéré — risques émergents, adaptation partielle
    ("CDR-008", 13, 11, 10,  8),  # faible — résilience climatique et protection juridique effectives
]


def calculate_composite(sub1, sub2, sub3, sub4):
    return round(sub1 * 0.30 + sub2 * 0.25 + sub3 * 0.25 + sub4 * 0.20, 2)


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
    for entity in ENTITIES:
        eid, s1, s2, s3, s4 = entity
        composite = calculate_composite(s1, s2, s3, s4)
        risk = classify_risk(composite)
        estimated_climate_displacement_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_climate_displacement_index": estimated_climate_displacement_index,
        })

    avg = round(sum(r["composite_score"] for r in results) / len(results), 2)
    dist = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1

    print(f"Agent: {AGENT_NAME}")
    print(f"Avg composite: {avg}")
    print(f"Risk distribution: {dist}")
    for r in results:
        print(f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}]")

    return results


if __name__ == "__main__":
    run_engine()
