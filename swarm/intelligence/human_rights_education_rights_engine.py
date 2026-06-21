#!/usr/bin/env python3
"""Human Rights Education Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Curriculum censorship severity
    sub2: float  # Teacher persecution index
    sub3: float  # Access restriction score
    sub4: float  # Civil society suppression level

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
    EntityScore("HRE-001", "North Korea State Education System",       95.0, 90.0, 92.0, 88.0),
    EntityScore("HRE-002", "Taliban-Controlled Afghanistan",           85.0, 80.0, 88.0, 78.0),
    EntityScore("HRE-003", "Eritrea Authoritarian Curriculum Control", 78.0, 72.0, 70.0, 68.0),
    EntityScore("HRE-004", "Belarus Post-2020 Education Crackdown",    68.0, 65.0, 62.0, 72.0),
    # 2 élevé (40–59)
    EntityScore("HRE-005", "Russia Post-Invasion Curriculum Revision", 55.0, 48.0, 50.0, 58.0),
    EntityScore("HRE-006", "Ethiopia Conflict-Zone Schools",           50.0, 52.0, 48.0, 42.0),
    # 1 modéré (20–39)
    EntityScore("HRE-007", "Central American Prison Rights Education",  30.0, 28.0, 35.0, 25.0),
    # 1 faible (<20)
    EntityScore("HRE-008", "Nordic Countries Human Rights Curricula",   8.0,  6.0,  10.0, 12.0),
]


def run():
    results = [
        {
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite(),
            "risk_level": e.risk_level(),
            "estimated_human_rights_education_rights_index": e.estimated_index(),
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
            f"→ index {r['estimated_human_rights_education_rights_index']}"
        )


if __name__ == "__main__":
    run()
