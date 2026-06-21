#!/usr/bin/env python3
"""
Water & Sanitation Rights Engine — Wave 159
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_water_access_coverage: float  # Couverture accès eau potable
    sub2_sanitation_infrastructure: float  # Infrastructure assainissement
    sub3_affordability_index: float        # Accessibilité financière
    sub4_water_quality_safety: float       # Qualité et sécurité eau

    @property
    def composite_score(self) -> float:
        return (self.sub1_water_access_coverage * 0.30 +
                self.sub2_sanitation_infrastructure * 0.25 +
                self.sub3_affordability_index * 0.25 +
                self.sub4_water_quality_safety * 0.20)

    @property
    def estimated_water_sanitation_rights_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("WSR-001", "Somalie (accès eau <50%, conflits)", 94, 92, 90, 88),
    EntityScore("WSR-002", "République Centrafricaine (infrastructure détruite)", 89, 87, 84, 82),
    EntityScore("WSR-003", "Mali (zones rurales sahéliennes)", 82, 80, 77, 75),
    EntityScore("WSR-004", "Niger (pénurie chronique)", 74, 72, 69, 67),
    EntityScore("WSR-005", "Bangladesh (arsenic nappes)", 58, 56, 53, 50),
    EntityScore("WSR-006", "Inde (Flint-type contaminations)", 50, 47, 45, 43),
    EntityScore("WSR-007", "Mexique (accès inégal urbain/rural)", 32, 30, 28, 26),
    EntityScore("WSR-008", "Pays-Bas (eau universelle garantie)", 9, 8, 7, 8),
]


def run_analysis():
    print("=== Water & Sanitation Rights Engine — Wave 159 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_water_sanitation_rights_index={e.estimated_water_sanitation_rights_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
