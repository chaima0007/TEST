#!/usr/bin/env python3
"""
Sexual & Reproductive Health Rights Engine — Wave 160
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_abortion_access: float
    sub2_contraception_availability: float
    sub3_maternal_mortality: float
    sub4_legal_criminalization: float

    @property
    def composite_score(self) -> float:
        return (self.sub1_abortion_access * 0.30 +
                self.sub2_contraception_availability * 0.25 +
                self.sub3_maternal_mortality * 0.25 +
                self.sub4_legal_criminalization * 0.20)

    @property
    def estimated_srh_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("SRH-001", "El Salvador (avortement totalement interdit)", 93, 89, 88, 90),
    EntityScore("SRH-002", "Nicaragua (criminalisation totale)", 90, 85, 84, 85),
    EntityScore("SRH-003", "Pologne (ban quasi-total post-2021)", 78, 72, 72, 73),
    EntityScore("SRH-004", "USA — Texas/Idaho (SB8 trigger laws)", 70, 64, 63, 65),
    EntityScore("SRH-005", "Maroc (avortement illégal sauf exception)", 56, 50, 50, 50),
    EntityScore("SRH-006", "Inde (mortalité maternelle rurale)", 46, 45, 46, 43),
    EntityScore("SRH-007", "Allemagne (§218 vestige)", 29, 27, 28, 28),
    EntityScore("SRH-008", "Pays-Bas (accès universel)", 9, 8, 9, 10),
]


def run_analysis():
    print("=== Sexual & Reproductive Health Rights Engine — Wave 160 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_srh_rights_index={e.estimated_srh_rights_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
