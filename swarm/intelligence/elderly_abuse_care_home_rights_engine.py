#!/usr/bin/env python3
"""Elderly Abuse & Care Home Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Physical/psychological abuse prevalence
    sub2: float  # Regulatory oversight deficiency
    sub3: float  # Financial exploitation index
    sub4: float  # Isolation & neglect severity

    def composite(self) -> float:
        return round(self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20, 2)

    def risk_level(self) -> str:
        c = self.composite()
        if c >= 60: return "critique"
        if c >= 40: return "élevé"
        if c >= 20: return "modéré"
        return "faible"

    def estimated_index(self) -> float:
        return round(self.composite() / 100 * 10, 2)


ENTITIES: List[EntityScore] = [
    # 4 critique (≥60)
    EntityScore("EAC-001", "Unregulated Private Care Homes Central Africa",    80.0, 85.0, 72.0, 78.0),
    EntityScore("EAC-002", "Post-COVID Locked-Down UK Nursing Homes",          72.0, 65.0, 60.0, 80.0),
    EntityScore("EAC-003", "Understaffed Eastern European State Facilities",   70.0, 68.0, 62.0, 72.0),
    EntityScore("EAC-004", "South Asian Family Violence Against Elderly",      68.0, 60.0, 65.0, 70.0),
    # 2 élevé (40–59)
    EntityScore("EAC-005", "Latin American Informal Elder Care Networks",      52.0, 48.0, 55.0, 45.0),
    EntityScore("EAC-006", "US For-Profit Care Home Sector",                   48.0, 42.0, 58.0, 40.0),
    # 1 modéré (20–39)
    EntityScore("EAC-007", "Rural Japan Isolated Elderly Population",          28.0, 32.0, 25.0, 38.0),
    # 1 faible (<20)
    EntityScore("EAC-008", "Nordic Regulated Publicly-Funded Care Homes",      10.0, 8.0,  12.0, 14.0),
]


def run():
    results = [
        {
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite(),
            "risk_level": e.risk_level(),
            "estimated_elderly_abuse_care_home_rights_index": e.estimated_index(),
        }
        for e in ENTITIES
    ]
    avg = round(statistics.mean([r["composite_score"] for r in results]), 2)
    dist: dict = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print(f"Avg composite: {avg} | Distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']} {r['name']}: "
            f"{r['composite_score']} ({r['risk_level']}) "
            f"→ index {r['estimated_elderly_abuse_care_home_rights_index']}"
        )


if __name__ == "__main__":
    run()
