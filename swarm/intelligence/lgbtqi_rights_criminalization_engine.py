#!/usr/bin/env python3
"""
Wave 171 — LGBTQI+ Rights Criminalization Engine
Caelum Partners SPRL — CaelumSwarm Intelligence Layer
Domain: Criminalisation et persécution des personnes LGBTQI+
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class LGBTQIRightsEntity:
    entity_id: str
    name: str
    country: str
    sub1: float  # criminalization_severity (peine mort ou prison > 10 ans)
    sub2: float  # state_violence_persecution (violence policière, camps conversion)
    sub3: float  # legal_protection_absence (absence lois anti-discrimination)
    sub4: float  # social_violence_impunity (violence sociale impunie)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_lgbtqi_persecution_index: float = field(init=False)

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
        self.estimated_lgbtqi_persecution_index = round(self.composite_score / 100 * 10, 2)


def run_lgbtqi_rights_engine() -> dict:
    entities = [
        # 4 critique (≥60)
        LGBTQIRightsEntity(
            entity_id="LRC-001",
            name="Iran",
            country="Iran",
            sub1=95.0,
            sub2=90.0,
            sub3=92.0,
            sub4=85.0,
        ),
        LGBTQIRightsEntity(
            entity_id="LRC-002",
            name="Arabie Saoudite",
            country="Arabie Saoudite",
            sub1=90.0,
            sub2=85.0,
            sub3=95.0,
            sub4=80.0,
        ),
        LGBTQIRightsEntity(
            entity_id="LRC-003",
            name="Nigeria",
            country="Nigeria",
            sub1=85.0,
            sub2=75.0,
            sub3=88.0,
            sub4=82.0,
        ),
        LGBTQIRightsEntity(
            entity_id="LRC-004",
            name="Ouganda",
            country="Ouganda",
            sub1=88.0,
            sub2=72.0,
            sub3=85.0,
            sub4=78.0,
        ),
        # 2 élevé (40-59.9)
        LGBTQIRightsEntity(
            entity_id="LRC-005",
            name="Russie",
            country="Russie",
            sub1=52.0,
            sub2=62.0,
            sub3=58.0,
            sub4=55.0,
        ),
        LGBTQIRightsEntity(
            entity_id="LRC-006",
            name="Égypte",
            country="Égypte",
            sub1=48.0,
            sub2=58.0,
            sub3=55.0,
            sub4=60.0,
        ),
        # 1 modéré (20-39.9)
        LGBTQIRightsEntity(
            entity_id="LRC-007",
            name="Jamaïque",
            country="Jamaïque",
            sub1=38.0,
            sub2=28.0,
            sub3=35.0,
            sub4=32.0,
        ),
        # 1 faible (<20)
        LGBTQIRightsEntity(
            entity_id="LRC-008",
            name="Canada",
            country="Canada",
            sub1=2.0,
            sub2=3.0,
            sub3=1.0,
            sub4=4.0,
        ),
    ]

    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}
    for e in entities:
        distribution[e.risk_level] += 1

    # Assertion obligatoire
    assert distribution == {"critique": 4, "élevé": 2, "modéré": 1, "faible": 1}, \
        f"Distribution invalide: {distribution}"

    avg_composite = round(sum(e.composite_score for e in entities) / len(entities), 2)
    avg_index = round(sum(e.estimated_lgbtqi_persecution_index for e in entities) / len(entities), 2)

    return {
        "domain": "lgbtqi-rights-criminalization",
        "generated_at": datetime.utcnow().isoformat(),
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "country": e.country,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_lgbtqi_persecution_index": e.estimated_lgbtqi_persecution_index,
            }
            for e in entities
        ],
        "avg_composite": avg_composite,
        "avg_index": avg_index,
        "risk_distribution": distribution,
    }


if __name__ == "__main__":
    result = run_lgbtqi_rights_engine()
    print(f"Agent: LGBTQI+ Rights Criminalization Engine Agent")
    print(f"Total entities: {len(result['entities'])}")
    print(f"Avg composite: {result['avg_composite']}")
    print(f"Avg index: {result['avg_index']}")
    print(f"Risk distribution: {result['risk_distribution']}")
    for e in result["entities"]:
        print(f"  {e['entity_id']}: {e['composite_score']} [{e['risk_level']}] — {e['estimated_lgbtqi_persecution_index']}")
