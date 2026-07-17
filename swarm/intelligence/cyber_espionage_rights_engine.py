#!/usr/bin/env python3
"""
Cyber Espionage Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random

random.seed(42)

AGENT_NAME = "Cyber Espionage Rights Engine Agent"
ACCENT_COLOR = "#0f172a"

ENTITIES = [
    # (id, state_sponsored_espionage_score, zero_day_exploit_misuse_score, covert_surveillance_ops_score, attribution_impunity_score)
    ("CER-001", 98, 97, 95, 93),  # critique — espionnage d'État massif toutes catégories
    ("CER-002", 91, 89, 88, 86),  # critique — exploitation zero-day systématique
    ("CER-003", 84, 82, 81, 79),  # critique — surveillance secrète transnationale étendue
    ("CER-004", 76, 75, 73, 71),  # critique — impunité structurelle documentée
    ("CER-005", 58, 57, 55, 53),  # élevé — espionnage ciblé journalistes et ONG
    ("CER-006", 48, 47, 45, 43),  # élevé — opérations covert partiellement documentées
    ("CER-007", 36, 35, 33, 31),  # modéré — incidents isolés, mécanismes partiels
    ("CER-008", 14, 13, 12, 10),  # faible — cadre légal robuste, incidents marginaux
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
        estimated_cyber_espionage_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_cyber_espionage_index": estimated_cyber_espionage_index,
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
