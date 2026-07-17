#!/usr/bin/env python3
"""
Press Freedom & Journalist Protection Engine — Wave 159
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_legal_framework: float      # Cadre légal protection presse
    sub2_physical_safety: float       # Sécurité physique journalistes
    sub3_digital_surveillance: float  # Surveillance numérique
    sub4_self_censorship_index: float # Auto-censure et pression

    @property
    def composite_score(self) -> float:
        return (self.sub1_legal_framework * 0.30 +
                self.sub2_physical_safety * 0.25 +
                self.sub3_digital_surveillance * 0.25 +
                self.sub4_self_censorship_index * 0.20)

    @property
    def estimated_press_freedom_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("PFJ-001", "Corée du Nord (journalisme d'État)", 95, 92, 94, 88),
    EntityScore("PFJ-002", "Érythrée (censure totale)", 90, 87, 85, 83),
    EntityScore("PFJ-003", "Chine (Great Firewall + RSF)", 84, 81, 88, 78),
    EntityScore("PFJ-004", "Russie (loi 'désinformation' 2022)", 78, 74, 76, 68),
    EntityScore("PFJ-005", "Turquie (3e emprisonnements)", 58, 55, 52, 51),
    EntityScore("PFJ-006", "Iran (journalistes web)", 51, 48, 54, 44),
    EntityScore("PFJ-007", "Inde (presse régionale)", 33, 30, 35, 26),
    EntityScore("PFJ-008", "Finlande (RSF classement #1)", 8, 10, 9, 11),
]


def run_analysis():
    print("=== Press Freedom & Journalist Protection Engine — Wave 159 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_press_freedom_index={e.estimated_press_freedom_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
