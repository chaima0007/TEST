#!/usr/bin/env python3
"""
Right to Science Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Right to Science Rights Engine Agent"
ACCENT = "#0c4a6e"

ENTITIES = [
    ("RTS-001", 98, 97, 96, 95),
    ("RTS-002", 93, 91, 90, 88),
    ("RTS-003", 85, 83, 82, 80),
    ("RTS-004", 77, 75, 73, 71),
    ("RTS-005", 58, 56, 54, 52),
    ("RTS-006", 49, 47, 46, 44),
    ("RTS-007", 31, 29, 27, 25),
    ("RTS-008", 11, 9, 8, 6),
]


def calculate_composite(open_access_denial_score, research_censorship_score,
                        technology_transfer_block_score, scientist_persecution_score):
    return round(
        open_access_denial_score * 0.30
        + research_censorship_score * 0.25
        + technology_transfer_block_score * 0.25
        + scientist_persecution_score * 0.20,
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
        estimated_right_to_science_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "open_access_denial_score": s1,
            "research_censorship_score": s2,
            "technology_transfer_block_score": s3,
            "scientist_persecution_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_right_to_science_index": estimated_right_to_science_index,
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
            f"  {r['entity_id']}: {r['composite_score']} [{r['risk_level']}]"
            f" — estimated_right_to_science_index={r['estimated_right_to_science_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
