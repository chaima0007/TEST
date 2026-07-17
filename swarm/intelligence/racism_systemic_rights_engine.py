#!/usr/bin/env python3
"""
Racism Systemic Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random

random.seed(42)

AGENT_NAME = "Racism Systemic Rights Engine Agent"
ACCENT_COLOR = "#991b1b"

ENTITIES = [
    # (id, structural_discrimination_score, racial_profiling_score, economic_racial_exclusion_score, hate_crime_impunity_score)
    ("RSR-001", 99, 98, 96, 94),  # critique — discrimination institutionnelle systémique documentée
    ("RSR-002", 92, 90, 88, 86),  # critique — profilage racial généralisé forces de l'ordre
    ("RSR-003", 84, 82, 80, 78),  # critique — exclusion économique raciale structurelle
    ("RSR-004", 75, 73, 71, 69),  # critique — impunité crimes de haine persistante
    ("RSR-005", 58, 56, 54, 52),  # élevé — discrimination partielle, recours limités
    ("RSR-006", 48, 46, 44, 42),  # élevé — profilage documenté, réformes insuffisantes
    ("RSR-007", 36, 34, 32, 30),  # modéré — incidents isolés, cadre légal partiel
    ("RSR-008", 13, 11, 10,  8),  # faible — mécanismes anti-discrimination effectifs
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
        estimated_racism_systemic_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_racism_systemic_index": estimated_racism_systemic_index,
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
