#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_overcrowding_conditions: float
    sub2_torture_ill_treatment: float
    sub3_medical_legal_access_deficit: float
    sub4_rehabilitation_rights_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_prison_conditions_detainee_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_overcrowding_conditions * 0.30
                + self.sub2_torture_ill_treatment * 0.25
                + self.sub3_medical_legal_access_deficit * 0.25
                + self.sub4_rehabilitation_rights_gap * 0.20
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
        self.estimated_prison_conditions_detainee_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite_score >= 60)
        EntityScore(
            entity_id="VEN",
            name="Venezuela",
            sub1_overcrowding_conditions=8.5,
            sub2_torture_ill_treatment=8.8,
            sub3_medical_legal_access_deficit=8.2,
            sub4_rehabilitation_rights_gap=7.9,
        ),
        EntityScore(
            entity_id="LBY",
            name="Libye",
            sub1_overcrowding_conditions=8.2,
            sub2_torture_ill_treatment=8.6,
            sub3_medical_legal_access_deficit=8.4,
            sub4_rehabilitation_rights_gap=7.8,
        ),
        EntityScore(
            entity_id="RUS",
            name="Russie",
            sub1_overcrowding_conditions=7.0,
            sub2_torture_ill_treatment=8.0,
            sub3_medical_legal_access_deficit=7.5,
            sub4_rehabilitation_rights_gap=7.2,
        ),
        EntityScore(
            entity_id="ETH",
            name="Éthiopie",
            sub1_overcrowding_conditions=7.8,
            sub2_torture_ill_treatment=7.6,
            sub3_medical_legal_access_deficit=7.4,
            sub4_rehabilitation_rights_gap=6.8,
        ),
        # 2 élevé (40 <= composite_score < 60)
        EntityScore(
            entity_id="SLV",
            name="El Salvador",
            sub1_overcrowding_conditions=6.0,
            sub2_torture_ill_treatment=5.8,
            sub3_medical_legal_access_deficit=5.5,
            sub4_rehabilitation_rights_gap=5.2,
        ),
        EntityScore(
            entity_id="PHL",
            name="Philippines",
            sub1_overcrowding_conditions=5.8,
            sub2_torture_ill_treatment=5.0,
            sub3_medical_legal_access_deficit=5.2,
            sub4_rehabilitation_rights_gap=4.8,
        ),
        # 1 modéré (20 <= composite_score < 40)
        EntityScore(
            entity_id="USA",
            name="États-Unis",
            sub1_overcrowding_conditions=3.5,
            sub2_torture_ill_treatment=3.2,
            sub3_medical_legal_access_deficit=2.8,
            sub4_rehabilitation_rights_gap=3.0,
        ),
        # 1 faible (composite_score < 20)
        EntityScore(
            entity_id="DNK",
            name="Danemark",
            sub1_overcrowding_conditions=0.6,
            sub2_torture_ill_treatment=0.4,
            sub3_medical_legal_access_deficit=0.5,
            sub4_rehabilitation_rights_gap=0.3,
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
                "estimated_prison_conditions_detainee_rights_index": e.estimated_prison_conditions_detainee_rights_index,
            }
        )

    avg_composite = round(
        sum(r["composite_score"] for r in results) / len(results), 2
    )
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "prison_conditions_detainee_rights_engine",
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
