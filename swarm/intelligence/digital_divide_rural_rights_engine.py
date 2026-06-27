#!/usr/bin/env python3
"""
Digital Divide Rural Rights Engine — CaelumSwarm™
EU CSDDD 2024/1760 Compliance Intelligence
"""
import random
random.seed(42)

AGENT_NAME = "Digital Divide Rural Rights Engine Agent"
ACCENT = "#166534"
PREFIX = "DDR"

ENTITIES = [
    ("DDR-001", 98, 97, 96, 92),
    ("DDR-002", 90, 89, 88, 84),
    ("DDR-003", 82, 81, 80, 76),
    ("DDR-004", 74, 73, 72, 68),
    ("DDR-005", 59, 58, 57, 53),
    ("DDR-006", 51, 50, 49, 45),
    ("DDR-007", 32, 31, 30, 26),
    ("DDR-008", 12, 11, 10, 6),
]


def calculate_composite(rural_internet_access_gap_score,
                        digital_skills_exclusion_score,
                        public_service_digital_exclusion_score,
                        infrastructure_investment_gap_score):
    return round(
        rural_internet_access_gap_score * 0.30
        + digital_skills_exclusion_score * 0.25
        + public_service_digital_exclusion_score * 0.25
        + infrastructure_investment_gap_score * 0.20,
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
        estimated_digital_divide_rural_index = round(composite / 100 * 10, 2)
        results.append({
            "entity_id": eid,
            "rural_internet_access_gap_score": s1,
            "digital_skills_exclusion_score": s2,
            "public_service_digital_exclusion_score": s3,
            "infrastructure_investment_gap_score": s4,
            "composite_score": composite,
            "risk_level": risk,
            "estimated_digital_divide_rural_index": estimated_digital_divide_rural_index,
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
            f" — estimated_digital_divide_rural_index={r['estimated_digital_divide_rural_index']}"
        )
    return results


if __name__ == "__main__":
    run_engine()
