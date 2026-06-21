#!/usr/bin/env python3
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_water_access_deficit: float
    sub2_sanitation_gap: float
    sub3_water_quality_contamination: float
    sub4_legal_recognition_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_water_sanitation_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_water_access_deficit * 0.30
                + self.sub2_sanitation_gap * 0.25
                + self.sub3_water_quality_contamination * 0.25
                + self.sub4_legal_recognition_gap * 0.20
            ) * 10,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_water_sanitation_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="CD",
            name="RDC (République démocratique du Congo)",
            sub1_water_access_deficit=8.8,
            sub2_sanitation_gap=9.0,
            sub3_water_quality_contamination=8.5,
            sub4_legal_recognition_gap=8.3,
        ),
        EntityScore(
            entity_id="NE",
            name="Niger",
            sub1_water_access_deficit=8.5,
            sub2_sanitation_gap=8.8,
            sub3_water_quality_contamination=8.0,
            sub4_legal_recognition_gap=8.2,
        ),
        EntityScore(
            entity_id="HT",
            name="Haïti",
            sub1_water_access_deficit=8.0,
            sub2_sanitation_gap=8.3,
            sub3_water_quality_contamination=8.5,
            sub4_legal_recognition_gap=7.8,
        ),
        EntityScore(
            entity_id="ET",
            name="Éthiopie",
            sub1_water_access_deficit=7.5,
            sub2_sanitation_gap=8.0,
            sub3_water_quality_contamination=7.2,
            sub4_legal_recognition_gap=7.5,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="NG",
            name="Nigeria",
            sub1_water_access_deficit=5.8,
            sub2_sanitation_gap=6.0,
            sub3_water_quality_contamination=5.5,
            sub4_legal_recognition_gap=5.3,
        ),
        EntityScore(
            entity_id="PK",
            name="Pakistan",
            sub1_water_access_deficit=5.2,
            sub2_sanitation_gap=5.5,
            sub3_water_quality_contamination=5.8,
            sub4_legal_recognition_gap=4.8,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="IN",
            name="Inde rurale",
            sub1_water_access_deficit=3.5,
            sub2_sanitation_gap=3.8,
            sub3_water_quality_contamination=3.2,
            sub4_legal_recognition_gap=3.0,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="DK",
            name="Danemark (modèle WASH)",
            sub1_water_access_deficit=0.5,
            sub2_sanitation_gap=0.4,
            sub3_water_quality_contamination=0.3,
            sub4_legal_recognition_gap=0.6,
        ),
    ]

    results = []
    for e in entities:
        results.append(
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_water_access_deficit": e.sub1_water_access_deficit,
                "sub2_sanitation_gap": e.sub2_sanitation_gap,
                "sub3_water_quality_contamination": e.sub3_water_quality_contamination,
                "sub4_legal_recognition_gap": e.sub4_legal_recognition_gap,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_water_sanitation_rights_index": e.estimated_water_sanitation_rights_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "water_sanitation_rights_engine",
        "wave": 149,
        "total_entities": len(results),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
