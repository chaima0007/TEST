#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_state_persecution_religious: float
    sub2_blasphemy_apostasy_laws: float
    sub3_minority_religion_discrimination: float
    sub4_forced_conversion_risk: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_freedom_religion_belief_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_state_persecution_religious * 0.30
                + self.sub2_blasphemy_apostasy_laws * 0.25
                + self.sub3_minority_religion_discrimination * 0.25
                + self.sub4_forced_conversion_risk * 0.20
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
        self.estimated_freedom_religion_belief_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite_score >= 60)
        EntityScore(
            entity_id="CHN",
            name="Chine",
            sub1_state_persecution_religious=9.0,
            sub2_blasphemy_apostasy_laws=7.5,
            sub3_minority_religion_discrimination=8.8,
            sub4_forced_conversion_risk=8.2,
        ),
        EntityScore(
            entity_id="IRN",
            name="Iran",
            sub1_state_persecution_religious=8.5,
            sub2_blasphemy_apostasy_laws=9.0,
            sub3_minority_religion_discrimination=7.8,
            sub4_forced_conversion_risk=8.0,
        ),
        EntityScore(
            entity_id="SAU",
            name="Arabie Saoudite",
            sub1_state_persecution_religious=8.2,
            sub2_blasphemy_apostasy_laws=9.2,
            sub3_minority_religion_discrimination=7.6,
            sub4_forced_conversion_risk=7.5,
        ),
        EntityScore(
            entity_id="MMR",
            name="Myanmar",
            sub1_state_persecution_religious=8.2,
            sub2_blasphemy_apostasy_laws=7.2,
            sub3_minority_religion_discrimination=8.5,
            sub4_forced_conversion_risk=8.5,
        ),
        # 2 élevé (40 <= composite_score < 60)
        EntityScore(
            entity_id="PAK",
            name="Pakistan",
            sub1_state_persecution_religious=5.5,
            sub2_blasphemy_apostasy_laws=6.5,
            sub3_minority_religion_discrimination=5.8,
            sub4_forced_conversion_risk=5.5,
        ),
        EntityScore(
            entity_id="NGA",
            name="Nigeria",
            sub1_state_persecution_religious=5.8,
            sub2_blasphemy_apostasy_laws=5.5,
            sub3_minority_religion_discrimination=5.8,
            sub4_forced_conversion_risk=6.0,
        ),
        # 1 modéré (20 <= composite_score < 40)
        EntityScore(
            entity_id="IND",
            name="Inde",
            sub1_state_persecution_religious=3.8,
            sub2_blasphemy_apostasy_laws=3.2,
            sub3_minority_religion_discrimination=4.2,
            sub4_forced_conversion_risk=3.8,
        ),
        # 1 faible (composite_score < 20)
        EntityScore(
            entity_id="NOR",
            name="Norvège",
            sub1_state_persecution_religious=0.8,
            sub2_blasphemy_apostasy_laws=0.6,
            sub3_minority_religion_discrimination=0.9,
            sub4_forced_conversion_risk=0.5,
        ),
    ]

    results = []
    for e in entities:
        results.append(
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_freedom_religion_belief_index": e.estimated_freedom_religion_belief_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "freedom_religion_belief_engine",
        "wave": 150,
        "total_entities": len(results),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
