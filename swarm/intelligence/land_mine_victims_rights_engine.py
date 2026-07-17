#!/usr/bin/env python3
"""
Land Mine Victims Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Land Mine Victims Rights Engine Agent"
ACCENT = "#92400e"

ENTITIES = [
    ("LMV-001", 99, 98, 97, 96),
    ("LMV-002", 95, 93, 91, 89),
    ("LMV-003", 87, 85, 83, 81),
    ("LMV-004", 78, 76, 74, 72),
    ("LMV-005", 58, 56, 54, 52),
    ("LMV-006", 49, 47, 45, 43),
    ("LMV-007", 30, 28, 26, 24),
    ("LMV-008", 9, 7, 6, 5),
]


def calculate_composite(active_mine_contamination_score,
                         victim_assistance_gap_score,
                         clearance_funding_gap_score,
                         mine_ban_non_compliance_score):
    return round(
        active_mine_contamination_score * 0.30
        + victim_assistance_gap_score * 0.25
        + clearance_funding_gap_score * 0.25
        + mine_ban_non_compliance_score * 0.20,
        2,
    )


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
        estimated_land_mine_victims_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "active_mine_contamination_score": s1,
            "victim_assistance_gap_score": s2,
            "clearance_funding_gap_score": s3,
            "mine_ban_non_compliance_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_land_mine_victims_index": estimated_land_mine_victims_index,
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
            f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}] "
            f"— estimated_land_mine_victims_index={r['estimated_land_mine_victims_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
