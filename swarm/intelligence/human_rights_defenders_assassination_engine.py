#!/usr/bin/env python3
"""Human Rights Defenders Assassination Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    defender_killings_rate: float         # sub1 ×0.30
    impunity_perpetrators: float          # sub2 ×0.25
    state_complicity_index: float         # sub3 ×0.25
    witness_protection_gap: float         # sub4 ×0.20

    def composite(self) -> float:
        return round(
            self.defender_killings_rate * 0.30
            + self.impunity_perpetrators * 0.25
            + self.state_complicity_index * 0.25
            + self.witness_protection_gap * 0.20,
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

    def estimated_human_rights_defenders_assassination_index(self) -> float:
        return round(self.composite() / 100 * 10, 2)


ENTITIES: List[EntityScore] = [
    # 4 critique (composite ≥ 60)
    EntityScore("COL", "Colombia",
                defender_killings_rate=92.0,
                impunity_perpetrators=88.0,
                state_complicity_index=75.0,
                witness_protection_gap=84.0),
    EntityScore("HND", "Honduras",
                defender_killings_rate=86.0,
                impunity_perpetrators=90.0,
                state_complicity_index=82.0,
                witness_protection_gap=80.0),
    EntityScore("GTM", "Guatemala",
                defender_killings_rate=80.0,
                impunity_perpetrators=85.0,
                state_complicity_index=78.0,
                witness_protection_gap=75.0),
    EntityScore("PHL", "Philippines",
                defender_killings_rate=84.0,
                impunity_perpetrators=80.0,
                state_complicity_index=85.0,
                witness_protection_gap=72.0),
    # 2 élevé (40 ≤ composite < 60)
    EntityScore("MEX", "Mexico",
                defender_killings_rate=60.0,
                impunity_perpetrators=58.0,
                state_complicity_index=50.0,
                witness_protection_gap=55.0),
    EntityScore("IND", "India",
                defender_killings_rate=52.0,
                impunity_perpetrators=55.0,
                state_complicity_index=48.0,
                witness_protection_gap=50.0),
    # 1 modéré (20 ≤ composite < 40)
    EntityScore("TUR", "Turkey",
                defender_killings_rate=35.0,
                impunity_perpetrators=38.0,
                state_complicity_index=30.0,
                witness_protection_gap=32.0),
    # 1 faible (composite < 20)
    EntityScore("NOR", "Norway",
                defender_killings_rate=8.0,
                impunity_perpetrators=5.0,
                state_complicity_index=6.0,
                witness_protection_gap=10.0),
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
            "estimated_index": e.estimated_human_rights_defenders_assassination_index(),
        })
    composites = [r["composite_score"] for r in results]
    avg = round(statistics.mean(composites), 2)
    dist: dict = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print("Domain: human_rights_defenders_assassination")
    print(f"Avg composite: {avg}")
    print(f"Distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']} {r['name']}: {r['composite_score']} "
            f"({r['risk_level']}) — index {r['estimated_index']}"
        )


if __name__ == "__main__":
    run()
