#!/usr/bin/env python3
"""
Wave 171 — Environmental Defenders Killings Engine
Caelum Partners SPRL — CaelumSwarm Intelligence Layer
Domain: Défenseurs de l'environnement assassinés / menacés (ONG Global Witness, terra firma)
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class EnvironmentalDefendersEntity:
    entity_id: str
    name: str
    country: str
    sub1: float  # killings_rate (taux meurtres défenseurs / an)
    sub2: float  # impunity_level (impunité des auteurs)
    sub3: float  # criminalization_activists (criminalisation légale militants)
    sub4: float  # legal_protection_gap (absence protection légale état)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_environmental_defenders_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20, 2
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_environmental_defenders_index = round(self.composite_score / 100 * 10, 2)


def run_environmental_defenders_engine() -> dict:
    entities = [
        # 4 critique (≥60)
        EnvironmentalDefendersEntity(
            entity_id="EDK-001",
            name="Honduras",
            country="Honduras",
            sub1=88.0,
            sub2=92.0,
            sub3=75.0,
            sub4=82.0,
        ),
        EnvironmentalDefendersEntity(
            entity_id="EDK-002",
            name="Philippines",
            country="Philippines",
            sub1=85.0,
            sub2=88.0,
            sub3=72.0,
            sub4=78.0,
        ),
        EnvironmentalDefendersEntity(
            entity_id="EDK-003",
            name="Brésil",
            country="Brésil",
            sub1=80.0,
            sub2=85.0,
            sub3=68.0,
            sub4=74.0,
        ),
        EnvironmentalDefendersEntity(
            entity_id="EDK-004",
            name="Colombie",
            country="Colombie",
            sub1=76.0,
            sub2=82.0,
            sub3=65.0,
            sub4=70.0,
        ),
        # 2 élevé (40-59.9)
        EnvironmentalDefendersEntity(
            entity_id="EDK-005",
            name="Mexique",
            country="Mexique",
            sub1=58.0,
            sub2=65.0,
            sub3=48.0,
            sub4=52.0,
        ),
        EnvironmentalDefendersEntity(
            entity_id="EDK-006",
            name="Inde",
            country="Inde",
            sub1=42.0,
            sub2=55.0,
            sub3=62.0,
            sub4=45.0,
        ),
        # 1 modéré (20-39.9)
        EnvironmentalDefendersEntity(
            entity_id="EDK-007",
            name="Kenya",
            country="Kenya",
            sub1=30.0,
            sub2=38.0,
            sub3=28.0,
            sub4=32.0,
        ),
        # 1 faible (<20)
        EnvironmentalDefendersEntity(
            entity_id="EDK-008",
            name="Costa Rica",
            country="Costa Rica",
            sub1=8.0,
            sub2=10.0,
            sub3=12.0,
            sub4=6.0,
        ),
    ]

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        distribution[e.risk_level] += 1

    # Assertion obligatoire
    assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Distribution invalide: {distribution}"

    avg_composite = round(sum(e.composite_score for e in entities) / len(entities), 2)
    avg_index = round(sum(e.estimated_environmental_defenders_index for e in entities) / len(entities), 2)

    return {
        "domain": "environmental-defenders-killings",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_environmental_defenders_index": e.estimated_environmental_defenders_index,
            }
            for e in entities
        ],
        "avg_composite": avg_composite,
        "avg_index": avg_index,
        "risk_distribution": distribution,
    }


if __name__ == "__main__":
    result = run_environmental_defenders_engine()
    print(f"Agent: Environmental Defenders Killings Engine Agent")
    print(f"Total entities: {len(result['entities'])}")
    print(f"Avg composite: {result['avg_composite']}")
    print(f"Avg index: {result['avg_index']}")
    print(f"Risk distribution: {result['risk_distribution']}")
    for e in result["entities"]:
        print(f"  {e['entity_id']}: {e['composite_score']} [{e['risk_level']}] — {e['estimated_environmental_defenders_index']}")
