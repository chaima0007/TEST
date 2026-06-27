#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_stateless_population_scale: float
    sub2_legal_recognition_gap: float
    sub3_documentation_access_deficit: float
    sub4_arbitrary_deprivation_risk: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_statelessness_citizenship_deprivation_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_stateless_population_scale * 0.30
                + self.sub2_legal_recognition_gap * 0.25
                + self.sub3_documentation_access_deficit * 0.25
                + self.sub4_arbitrary_deprivation_risk * 0.20
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
        self.estimated_statelessness_citizenship_deprivation_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="MMR_rohingya",
            name="Myanmar — Rohingyas (800k apatrides)",
            sub1_stateless_population_scale=9.5,
            sub2_legal_recognition_gap=9.2,
            sub3_documentation_access_deficit=9.0,
            sub4_arbitrary_deprivation_risk=9.5,
        ),
        EntityScore(
            entity_id="KWT_bidoun",
            name="Koweït — Bidouns sans nationalité",
            sub1_stateless_population_scale=8.0,
            sub2_legal_recognition_gap=8.5,
            sub3_documentation_access_deficit=8.2,
            sub4_arbitrary_deprivation_risk=8.8,
        ),
        EntityScore(
            entity_id="DOM_haitian_origin",
            name="République Dominicaine — Dominicains d'origine haïtienne",
            sub1_stateless_population_scale=7.8,
            sub2_legal_recognition_gap=8.2,
            sub3_documentation_access_deficit=8.0,
            sub4_arbitrary_deprivation_risk=8.5,
        ),
        EntityScore(
            entity_id="BTN_nepali_bhutanese",
            name="Bhoutan — Bhoutanais népalais expulsés",
            sub1_stateless_population_scale=7.5,
            sub2_legal_recognition_gap=7.8,
            sub3_documentation_access_deficit=8.0,
            sub4_arbitrary_deprivation_risk=8.2,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="KEN_nubians",
            name="Kenya — Nubiens et reconnaissance citoyenneté",
            sub1_stateless_population_scale=5.5,
            sub2_legal_recognition_gap=6.2,
            sub3_documentation_access_deficit=6.5,
            sub4_arbitrary_deprivation_risk=5.8,
        ),
        EntityScore(
            entity_id="SAH_sahel_undocumented",
            name="Sahel — Populations sans-papiers transfrontalières",
            sub1_stateless_population_scale=6.0,
            sub2_legal_recognition_gap=5.8,
            sub3_documentation_access_deficit=6.2,
            sub4_arbitrary_deprivation_risk=5.5,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="LVA_non_citizens",
            name="Lettonie — Non-citoyens (statut résiduel post-URSS)",
            sub1_stateless_population_scale=3.2,
            sub2_legal_recognition_gap=3.8,
            sub3_documentation_access_deficit=2.5,
            sub4_arbitrary_deprivation_risk=2.8,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="UNHCR_reduction_model",
            name="UNHCR — Modèle de réduction de l'apatridie",
            sub1_stateless_population_scale=1.0,
            sub2_legal_recognition_gap=1.2,
            sub3_documentation_access_deficit=0.8,
            sub4_arbitrary_deprivation_risk=0.5,
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_stateless_population_scale": e.sub1_stateless_population_scale,
            "sub2_legal_recognition_gap": e.sub2_legal_recognition_gap,
            "sub3_documentation_access_deficit": e.sub3_documentation_access_deficit,
            "sub4_arbitrary_deprivation_risk": e.sub4_arbitrary_deprivation_risk,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_statelessness_citizenship_deprivation_index": e.estimated_statelessness_citizenship_deprivation_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "statelessness_citizenship_deprivation_engine",
        "wave": 151,
        "total_entities": len(results),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run()
