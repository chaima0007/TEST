#!/usr/bin/env python3
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_language_suppression: float
    sub2_cultural_destruction: float
    sub3_education_rights_gap: float
    sub4_media_representation_deficit: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_minority_language_cultural_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_language_suppression * 0.30
                + self.sub2_cultural_destruction * 0.25
                + self.sub3_education_rights_gap * 0.25
                + self.sub4_media_representation_deficit * 0.20
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
        self.estimated_minority_language_cultural_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="CN",
            name="Chine (Ouïghours/Tibétains)",
            sub1_language_suppression=8.5,
            sub2_cultural_destruction=8.8,
            sub3_education_rights_gap=8.2,
            sub4_media_representation_deficit=8.6,
        ),
        EntityScore(
            entity_id="MM",
            name="Myanmar (Rohingyas)",
            sub1_language_suppression=8.0,
            sub2_cultural_destruction=8.5,
            sub3_education_rights_gap=8.3,
            sub4_media_representation_deficit=7.8,
        ),
        EntityScore(
            entity_id="TR",
            name="Turquie (Kurdes)",
            sub1_language_suppression=7.5,
            sub2_cultural_destruction=7.2,
            sub3_education_rights_gap=7.0,
            sub4_media_representation_deficit=7.4,
        ),
        EntityScore(
            entity_id="IR",
            name="Iran (Kurdes/Baloutches)",
            sub1_language_suppression=7.2,
            sub2_cultural_destruction=7.0,
            sub3_education_rights_gap=6.8,
            sub4_media_representation_deficit=7.1,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="RU",
            name="Russie (peuples indigènes)",
            sub1_language_suppression=5.5,
            sub2_cultural_destruction=5.2,
            sub3_education_rights_gap=5.0,
            sub4_media_representation_deficit=5.3,
        ),
        EntityScore(
            entity_id="IN",
            name="Inde (minorités du nord-est)",
            sub1_language_suppression=4.8,
            sub2_cultural_destruction=4.5,
            sub3_education_rights_gap=5.1,
            sub4_media_representation_deficit=4.7,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="FR",
            name="France (langues régionales)",
            sub1_language_suppression=3.0,
            sub2_cultural_destruction=2.5,
            sub3_education_rights_gap=3.2,
            sub4_media_representation_deficit=2.8,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="CA",
            name="Canada (langues autochtones en rétablissement)",
            sub1_language_suppression=1.2,
            sub2_cultural_destruction=1.0,
            sub3_education_rights_gap=1.5,
            sub4_media_representation_deficit=1.1,
        ),
    ]

    results = []
    for e in entities:
        results.append(
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_language_suppression": e.sub1_language_suppression,
                "sub2_cultural_destruction": e.sub2_cultural_destruction,
                "sub3_education_rights_gap": e.sub3_education_rights_gap,
                "sub4_media_representation_deficit": e.sub4_media_representation_deficit,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_minority_language_cultural_rights_index": e.estimated_minority_language_cultural_rights_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "minority_language_cultural_rights_engine",
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
