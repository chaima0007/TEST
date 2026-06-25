#!/usr/bin/env python3
"""
Religious Freedom & Persecution Engine — Wave 160
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_legal_restrictions: float
    sub2_state_persecution: float
    sub3_societal_violence: float
    sub4_minority_protection: float

    @property
    def composite_score(self) -> float:
        return (self.sub1_legal_restrictions * 0.30 +
                self.sub2_state_persecution * 0.25 +
                self.sub3_societal_violence * 0.25 +
                self.sub4_minority_protection * 0.20)

    @property
    def estimated_religious_freedom_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("RFP-001", "Chine (Ouïghours + Falun Gong + chrétiens)", 96, 94, 91, 90),
    EntityScore("RFP-002", "Corée du Nord (religion interdite)", 95, 92, 88, 88),
    EntityScore("RFP-003", "Arabie Saoudite (blasphème/apostasie)", 88, 85, 80, 82),
    EntityScore("RFP-004", "Myanmar (minorités bouddhistes + chrétiens)", 75, 72, 70, 70),
    EntityScore("RFP-005", "Pakistan (loi blasphème 295-C)", 60, 56, 54, 52),
    EntityScore("RFP-006", "Égypte (coptes discriminés)", 50, 48, 47, 46),
    EntityScore("RFP-007", "France (laïcité conflictuelle)", 28, 25, 26, 24),
    EntityScore("RFP-008", "Canada (pluralisme religieux)", 12, 10, 11, 10),
]


def run_analysis():
    print("=== Religious Freedom & Persecution Engine — Wave 160 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_religious_freedom_index={e.estimated_religious_freedom_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
