#!/usr/bin/env python3
import json
from dataclasses import dataclass, field
from typing import List


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_forced_eviction_scale: float
    sub2_homelessness_rate: float
    sub3_legal_protection_housing: float
    sub4_affordability_crisis: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_housing_forced_eviction_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_forced_eviction_scale * 0.30
                + self.sub2_homelessness_rate * 0.25
                + self.sub3_legal_protection_housing * 0.25
                + self.sub4_affordability_crisis * 0.20
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
        self.estimated_housing_forced_eviction_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="ZW",
            name="Zimbabwe",
            sub1_forced_eviction_scale=8.8,
            sub2_homelessness_rate=8.5,
            sub3_legal_protection_housing=8.6,
            sub4_affordability_crisis=8.2,
        ),
        EntityScore(
            entity_id="KH",
            name="Cambodge",
            sub1_forced_eviction_scale=8.2,
            sub2_homelessness_rate=7.8,
            sub3_legal_protection_housing=8.0,
            sub4_affordability_crisis=7.6,
        ),
        EntityScore(
            entity_id="ET",
            name="Éthiopie (déplacés internes)",
            sub1_forced_eviction_scale=7.8,
            sub2_homelessness_rate=8.0,
            sub3_legal_protection_housing=7.5,
            sub4_affordability_crisis=7.7,
        ),
        EntityScore(
            entity_id="KE",
            name="Kenya (bidonvilles)",
            sub1_forced_eviction_scale=7.5,
            sub2_homelessness_rate=7.3,
            sub3_legal_protection_housing=7.2,
            sub4_affordability_crisis=7.0,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="BR",
            name="Brésil (favelas)",
            sub1_forced_eviction_scale=5.5,
            sub2_homelessness_rate=5.2,
            sub3_legal_protection_housing=4.8,
            sub4_affordability_crisis=5.6,
        ),
        EntityScore(
            entity_id="IN",
            name="Inde (démolitions urbaines)",
            sub1_forced_eviction_scale=5.2,
            sub2_homelessness_rate=5.0,
            sub3_legal_protection_housing=4.5,
            sub4_affordability_crisis=5.0,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="US",
            name="États-Unis (sans-abri urbains)",
            sub1_forced_eviction_scale=3.2,
            sub2_homelessness_rate=3.5,
            sub3_legal_protection_housing=2.8,
            sub4_affordability_crisis=3.8,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="SE",
            name="Suède (modèle logement social)",
            sub1_forced_eviction_scale=0.8,
            sub2_homelessness_rate=1.0,
            sub3_legal_protection_housing=0.5,
            sub4_affordability_crisis=1.2,
        ),
    ]

    results = []
    for e in entities:
        results.append(
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_forced_eviction_scale": e.sub1_forced_eviction_scale,
                "sub2_homelessness_rate": e.sub2_homelessness_rate,
                "sub3_legal_protection_housing": e.sub3_legal_protection_housing,
                "sub4_affordability_crisis": e.sub4_affordability_crisis,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_housing_forced_eviction_rights_index": e.estimated_housing_forced_eviction_rights_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "housing_forced_eviction_rights_engine",
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
