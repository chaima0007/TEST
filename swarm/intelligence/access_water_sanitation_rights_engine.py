#!/usr/bin/env python3
"""
Wave 171 — Access Water Sanitation Rights Engine
Caelum Partners SPRL — CaelumSwarm Intelligence Layer
Domain: Droit à l'eau potable et assainissement (ODD 6, résolution ONU 2010)
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class WaterSanitationEntity:
    entity_id: str
    name: str
    country: str
    sub1: float  # access_gap_percentage (% population sans accès eau potable)
    sub2: float  # sanitation_deficit (déficit assainissement)
    sub3: float  # conflict_weaponization (eau utilisée comme arme conflit)
    sub4: float  # privatization_exclusion (exclusion par privatisation)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_water_rights_index: float = field(init=False)

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
        self.estimated_water_rights_index = round(self.composite_score / 100 * 10, 2)


def run_water_sanitation_engine() -> dict:
    entities = [
        # 4 critique (≥60)
        WaterSanitationEntity(
            entity_id="WSR-001",
            name="Somalie",
            country="Somalie",
            sub1=88.0,
            sub2=90.0,
            sub3=75.0,
            sub4=70.0,
        ),
        WaterSanitationEntity(
            entity_id="WSR-002",
            name="RDC",
            country="République Démocratique du Congo",
            sub1=82.0,
            sub2=85.0,
            sub3=68.0,
            sub4=72.0,
        ),
        WaterSanitationEntity(
            entity_id="WSR-003",
            name="Yémen",
            country="Yémen",
            sub1=78.0,
            sub2=72.0,
            sub3=92.0,
            sub4=65.0,
        ),
        WaterSanitationEntity(
            entity_id="WSR-004",
            name="Niger",
            country="Niger",
            sub1=80.0,
            sub2=83.0,
            sub3=55.0,
            sub4=68.0,
        ),
        # 2 élevé (40-59.9)
        WaterSanitationEntity(
            entity_id="WSR-005",
            name="Pakistan",
            country="Pakistan",
            sub1=52.0,
            sub2=58.0,
            sub3=42.0,
            sub4=45.0,
        ),
        WaterSanitationEntity(
            entity_id="WSR-006",
            name="Inde rurale",
            country="Inde",
            sub1=45.0,
            sub2=62.0,
            sub3=32.0,
            sub4=48.0,
        ),
        # 1 modéré (20-39.9)
        WaterSanitationEntity(
            entity_id="WSR-007",
            name="Pérou",
            country="Pérou",
            sub1=32.0,
            sub2=38.0,
            sub3=18.0,
            sub4=30.0,
        ),
        # 1 faible (<20)
        WaterSanitationEntity(
            entity_id="WSR-008",
            name="Pays-Bas",
            country="Pays-Bas",
            sub1=2.0,
            sub2=3.0,
            sub3=1.0,
            sub4=5.0,
        ),
    ]

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        distribution[e.risk_level] += 1

    # Assertion obligatoire
    assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Distribution invalide: {distribution}"

    avg_composite = round(sum(e.composite_score for e in entities) / len(entities), 2)
    avg_index = round(sum(e.estimated_water_rights_index for e in entities) / len(entities), 2)

    return {
        "domain": "access-water-sanitation-rights",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_water_rights_index": e.estimated_water_rights_index,
            }
            for e in entities
        ],
        "avg_composite": avg_composite,
        "avg_index": avg_index,
        "risk_distribution": distribution,
    }


if __name__ == "__main__":
    result = run_water_sanitation_engine()
    print(f"Agent: Access Water Sanitation Rights Engine Agent")
    print(f"Total entities: {len(result['entities'])}")
    print(f"Avg composite: {result['avg_composite']}")
    print(f"Avg index: {result['avg_index']}")
    print(f"Risk distribution: {result['risk_distribution']}")
    for e in result["entities"]:
        print(f"  {e['entity_id']}: {e['composite_score']} [{e['risk_level']}] — {e['estimated_water_rights_index']}")
