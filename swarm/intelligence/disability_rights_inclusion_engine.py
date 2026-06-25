#!/usr/bin/env python3
"""
Disability Rights & Inclusion Engine — Wave 159
CaelumSwarm Intelligence Layer
"""
from dataclasses import dataclass, field
from typing import List

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_legal_accessibility: float      # Cadre légal accessibilité
    sub2_employment_discrimination: float  # Discrimination emploi
    sub3_healthcare_access: float          # Accès soins spécialisés
    sub4_social_inclusion: float           # Inclusion sociale et éducation

    @property
    def composite_score(self) -> float:
        return (self.sub1_legal_accessibility * 0.30 +
                self.sub2_employment_discrimination * 0.25 +
                self.sub3_healthcare_access * 0.25 +
                self.sub4_social_inclusion * 0.20)

    @property
    def estimated_disability_rights_inclusion_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    @property
    def level(self) -> str:
        cs = self.composite_score
        if cs >= 60: return "critique"
        elif cs >= 40: return "élevé"
        elif cs >= 20: return "modéré"
        return "faible"


ENTITIES: List[EntityScore] = [
    EntityScore("DRI-001", "Soudan du Sud (aucun cadre légal)", 92, 88, 86, 84),
    EntityScore("DRI-002", "Haïti (post-séisme, handicapés abandonnés)", 87, 83, 81, 80),
    EntityScore("DRI-003", "Inde (Persons with Disabilities Act insuffisant)", 78, 76, 74, 72),
    EntityScore("DRI-004", "Indonésie (barrières physiques + sociales)", 72, 68, 66, 64),
    EntityScore("DRI-005", "Mexique (application partielle)", 56, 53, 51, 49),
    EntityScore("DRI-006", "Brésil (LBI 2015 non appliquée)", 48, 46, 44, 42),
    EntityScore("DRI-007", "France (RQTH insuffisant)", 30, 28, 26, 24),
    EntityScore("DRI-008", "Suède (modèle universel)", 11, 10, 9, 10),
]


def run_analysis():
    print("=== Disability Rights & Inclusion Engine — Wave 159 ===\n")
    total = 0
    dist = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in ENTITIES:
        cs = e.composite_score
        total += cs
        dist[e.level] += 1
        print(f"{e.entity_id} | {e.name}")
        print(f"  composite_score={cs:.2f} | level={e.level} | estimated_disability_rights_inclusion_index={e.estimated_disability_rights_inclusion_index}")
    avg = total / len(ENTITIES)
    print(f"\navg_composite: {avg:.2f}")
    print(f"risk_distribution: {dist}")
    assert dist == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, f"Distribution incorrecte: {dist}"
    print("\n✓ Distribution validée : 4 critique / 2 élevé / 1 modéré / 1 faible")


if __name__ == "__main__":
    run_analysis()
