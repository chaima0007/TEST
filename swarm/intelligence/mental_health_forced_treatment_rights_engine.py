#!/usr/bin/env python3
"""Mental Health Forced Treatment Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass
from typing import List
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    involuntary_commitment_rate: float      # sub1 ×0.30
    electroconvulsive_without_consent: float  # sub2 ×0.25
    legal_safeguards_absence: float          # sub3 ×0.25
    community_alternatives_gap: float        # sub4 ×0.20

    def composite(self) -> float:
        return round(
            self.involuntary_commitment_rate * 0.30
            + self.electroconvulsive_without_consent * 0.25
            + self.legal_safeguards_absence * 0.25
            + self.community_alternatives_gap * 0.20,
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

    def estimated_mental_health_forced_treatment_index(self) -> float:
        return round(self.composite() / 100 * 10, 2)


ENTITIES: List[EntityScore] = [
    # 4 critique (composite ≥ 60)
    EntityScore("RUS", "Russia",
                involuntary_commitment_rate=88.0,
                electroconvulsive_without_consent=82.0,
                legal_safeguards_absence=85.0,
                community_alternatives_gap=78.0),
    EntityScore("CHN", "China",
                involuntary_commitment_rate=85.0,
                electroconvulsive_without_consent=79.0,
                legal_safeguards_absence=88.0,
                community_alternatives_gap=72.0),
    EntityScore("UZB", "Uzbekistan",
                involuntary_commitment_rate=80.0,
                electroconvulsive_without_consent=74.0,
                legal_safeguards_absence=82.0,
                community_alternatives_gap=70.0),
    EntityScore("KAZ", "Kazakhstan",
                involuntary_commitment_rate=76.0,
                electroconvulsive_without_consent=70.0,
                legal_safeguards_absence=78.0,
                community_alternatives_gap=65.0),
    # 2 élevé (40 ≤ composite < 60)
    EntityScore("ROU", "Romania",
                involuntary_commitment_rate=58.0,
                electroconvulsive_without_consent=50.0,
                legal_safeguards_absence=55.0,
                community_alternatives_gap=48.0),
    EntityScore("BGR", "Bulgaria",
                involuntary_commitment_rate=55.0,
                electroconvulsive_without_consent=47.0,
                legal_safeguards_absence=52.0,
                community_alternatives_gap=44.0),
    # 1 modéré (20 ≤ composite < 40)
    EntityScore("BRA", "Brazil",
                involuntary_commitment_rate=35.0,
                electroconvulsive_without_consent=30.0,
                legal_safeguards_absence=32.0,
                community_alternatives_gap=28.0),
    # 1 faible (composite < 20)
    EntityScore("NLD", "Netherlands",
                involuntary_commitment_rate=18.0,
                electroconvulsive_without_consent=12.0,
                legal_safeguards_absence=10.0,
                community_alternatives_gap=14.0),
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
            "estimated_index": e.estimated_mental_health_forced_treatment_index(),
        })
    composites = [r["composite_score"] for r in results]
    avg = round(statistics.mean(composites), 2)
    dist: dict = {}
    for r in results:
        dist[r["risk_level"]] = dist.get(r["risk_level"], 0) + 1
    print("Domain: mental_health_forced_treatment_rights")
    print(f"Avg composite: {avg}")
    print(f"Distribution: {dist}")
    for r in results:
        print(
            f"  {r['entity_id']} {r['name']}: {r['composite_score']} "
            f"({r['risk_level']}) — index {r['estimated_index']}"
        )


if __name__ == "__main__":
    run()
