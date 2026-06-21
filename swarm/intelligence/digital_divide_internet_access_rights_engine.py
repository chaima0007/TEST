#!/usr/bin/env python3
"""Digital Divide & Internet Access Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Infrastructure exclusion severity
    sub2: float  # Affordability barrier index
    sub3: float  # State censorship / shutdown frequency
    sub4: float  # Digital literacy gap score

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
    EntityScore("DD-001", "Sub-Saharan Rural Communities",       78.0, 80.0, 62.0, 70.0),
    EntityScore("DD-002", "Myanmar Post-Coup Internet Shutdowns",72.0, 65.0, 88.0, 68.0),
    EntityScore("DD-003", "North Korea Intranet-Only Population", 90.0, 85.0, 95.0, 60.0),
    EntityScore("DD-004", "Low-Income Urban Slum Dwellers",      65.0, 74.0, 58.0, 62.0),
    # 2 élevé (40–59)
    EntityScore("DD-005", "Indigenous Remote Communities Americas", 55.0, 50.0, 42.0, 48.0),
    EntityScore("DD-006", "Elderly Non-Digital Citizens Global",    45.0, 52.0, 40.0, 58.0),
    # 1 modéré (20–39)
    EntityScore("DD-007", "Rural Women in South Asia",            35.0, 38.0, 28.0, 30.0),
    # 1 faible (<20)
    EntityScore("DD-008", "High-Income Urban Youth Global",        10.0, 8.0,  12.0, 15.0),
]


def run():
    results = [
        {
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite(),
            "risk_level": e.risk_level(),
            "estimated_digital_divide_internet_access_rights_index": e.estimated_index(),
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
            f"→ index {r['estimated_digital_divide_internet_access_rights_index']}"
        )


if __name__ == "__main__":
    run()
