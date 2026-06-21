#!/usr/bin/env python3
"""
Housing Rights & Eviction Engine — Wave 160
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_forced_eviction_rate: float
    sub2_housing_affordability: float
    sub3_legal_protection: float
    sub4_homeless_population: float

    @property
    def composite_score(self) -> float:
        return (self.sub1_forced_eviction_rate * 0.30 +
                self.sub2_housing_affordability * 0.25 +
                self.sub3_legal_protection * 0.25 +
                self.sub4_homeless_population * 0.20)

    @property
    def estimated_housing_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("HRE-001", "Kenya (évictions informelles Nairobi)", 91, 87, 85, 88),
    EntityScore("HRE-002", "Philippines (démolitions urbaines)", 85, 80, 82, 81),
    EntityScore("HRE-003", "Zimbabwe (Murambatsvina legacy)", 80, 76, 74, 78),
    EntityScore("HRE-004", "Inde (Adivasi expulsions)", 70, 67, 65, 70),
    EntityScore("HRE-005", "USA (crise logement Los Angeles)", 56, 55, 52, 53),
    EntityScore("HRE-006", "Brésil (favelas Rio)", 49, 47, 46, 46),
    EntityScore("HRE-007", "France (saturation hébergement)", 30, 29, 27, 30),
    EntityScore("HRE-008", "Finlande (Housing First)", 10, 9, 11, 10),
]


def run_analysis():
    print("=== Housing Rights & Eviction Engine — Wave 160 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_housing_rights_index={e.estimated_housing_rights_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
