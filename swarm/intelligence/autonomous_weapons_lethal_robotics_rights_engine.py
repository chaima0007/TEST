#!/usr/bin/env python3
"""Autonomous Weapons Lethal Robotics Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    laws_deployment_rate: float           # sub1 ×0.30 — Lethal Autonomous Weapons Systems deployment
    accountability_gap: float             # sub2 ×0.25 — absence of command accountability
    civilian_harm_incidents: float        # sub3 ×0.25 — civilian harm from autonomous strikes
    treaty_refusal_index: float           # sub4 ×0.20 — refusal to engage with LAWS ban treaties

    def composite(self) -> float:
        return round(
            self.laws_deployment_rate * 0.30
            + self.accountability_gap * 0.25
            + self.civilian_harm_incidents * 0.25
            + self.treaty_refusal_index * 0.20,
            2,
        )

    def risk_level(self) -> str:
        c = self.composite()
        if c >= 60:
            return "critique"
        if c >= 40:
            return "élevé"
        if c >= 20:
            return "modéré"
        return "faible"

    def estimated_autonomous_weapons_lethal_robotics_rights_index(self) -> float:
        return round(self.composite() / 100 * 10, 2)


ENTITIES: List[EntityScore] = [
    # 4 critique (composite ≥ 60)
    EntityScore("USA", "United States",
                laws_deployment_rate=85.0,
                accountability_gap=78.0,
                civilian_harm_incidents=72.0,
                treaty_refusal_index=90.0),
    EntityScore("CHN", "China",
                laws_deployment_rate=88.0,
                accountability_gap=85.0,
                civilian_harm_incidents=70.0,
                treaty_refusal_index=88.0),
    EntityScore("RUS", "Russia",
                laws_deployment_rate=82.0,
                accountability_gap=88.0,
                civilian_harm_incidents=80.0,
                treaty_refusal_index=85.0),
    EntityScore("ISR", "Israel",
                laws_deployment_rate=80.0,
                accountability_gap=75.0,
                civilian_harm_incidents=85.0,
                treaty_refusal_index=78.0),
    # 2 élevé (40 ≤ composite < 60)
    EntityScore("KOR", "South Korea",
                laws_deployment_rate=58.0,
                accountability_gap=52.0,
                civilian_harm_incidents=40.0,
                treaty_refusal_index=55.0),
    EntityScore("GBR", "United Kingdom",
                laws_deployment_rate=50.0,
                accountability_gap=48.0,
                civilian_harm_incidents=38.0,
                treaty_refusal_index=60.0),
    # 1 modéré (20 ≤ composite < 40)
    EntityScore("DEU", "Germany",
                laws_deployment_rate=28.0,
                accountability_gap=32.0,
                civilian_harm_incidents=20.0,
                treaty_refusal_index=30.0),
    # 1 faible (composite < 20)
    EntityScore("AUT", "Austria",
                laws_deployment_rate=10.0,
                accountability_gap=12.0,
                civilian_harm_incidents=8.0,
                treaty_refusal_index=5.0),
]


def run():
    results = []
    for e in ENTITIES:
        c = e.composite()
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": c,
            "risk_level": e.risk_level(),
            "estimated_index": e.estimated_autonomous_weapons_lethal_robotics_rights_index(),
        })
    composites = [r["composite_score"] for r in results]
    avg = round(statistics.mean(composites), 2)
    dist: dict = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print("Domain: autonomous_weapons_lethal_robotics_rights")
    print(f"Avg composite: {avg}")
    print(f"Distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']} {r['name']}: {r['composite_score']} "
            f"({r['risk_level']}) — index {r['estimated_index']}"
        )


if __name__ == "__main__":
    run()
