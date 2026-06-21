#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_mass_surveillance_rights_violation: float
    sub2_arbitrary_detention_terrorism_pretext: float
    sub3_due_process_fair_trial_deficit: float
    sub4_civil_society_restriction: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_anti_terrorism_counter_extremism_rights_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_mass_surveillance_rights_violation * 0.30
                + self.sub2_arbitrary_detention_terrorism_pretext * 0.25
                + self.sub3_due_process_fair_trial_deficit * 0.25
                + self.sub4_civil_society_restriction * 0.20
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
        self.estimated_anti_terrorism_counter_extremism_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="CHN_xinjiang",
            name="Chine — Sécurité Xinjiang",
            sub1_mass_surveillance_rights_violation=9.2,
            sub2_arbitrary_detention_terrorism_pretext=9.0,
            sub3_due_process_fair_trial_deficit=8.8,
            sub4_civil_society_restriction=9.1,
        ),
        EntityScore(
            entity_id="EGY_law94_2015",
            name="Égypte — Loi antiterroriste 94/2015",
            sub1_mass_surveillance_rights_violation=7.8,
            sub2_arbitrary_detention_terrorism_pretext=8.5,
            sub3_due_process_fair_trial_deficit=8.2,
            sub4_civil_society_restriction=8.0,
        ),
        EntityScore(
            entity_id="RUS_yarovaya",
            name="Russie — Loi Yarovaya",
            sub1_mass_surveillance_rights_violation=8.5,
            sub2_arbitrary_detention_terrorism_pretext=7.9,
            sub3_due_process_fair_trial_deficit=7.8,
            sub4_civil_society_restriction=8.3,
        ),
        EntityScore(
            entity_id="SAU_antiterrorism",
            name="Arabie Saoudite — Lois antiterrorisme",
            sub1_mass_surveillance_rights_violation=7.5,
            sub2_arbitrary_detention_terrorism_pretext=8.0,
            sub3_due_process_fair_trial_deficit=8.0,
            sub4_civil_society_restriction=8.2,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="TUR_post2016",
            name="Turquie — Législation post-coup 2016",
            sub1_mass_surveillance_rights_violation=6.0,
            sub2_arbitrary_detention_terrorism_pretext=6.5,
            sub3_due_process_fair_trial_deficit=6.2,
            sub4_civil_society_restriction=6.8,
        ),
        EntityScore(
            entity_id="PAK_anti_terror",
            name="Pakistan — Lois antiterroristes",
            sub1_mass_surveillance_rights_violation=5.5,
            sub2_arbitrary_detention_terrorism_pretext=6.0,
            sub3_due_process_fair_trial_deficit=5.8,
            sub4_civil_society_restriction=5.5,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="FRA_silt_renseignement",
            name="France — SILT / Renseignement",
            sub1_mass_surveillance_rights_violation=3.5,
            sub2_arbitrary_detention_terrorism_pretext=2.8,
            sub3_due_process_fair_trial_deficit=2.5,
            sub4_civil_society_restriction=2.2,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="CAN_oversight_model",
            name="Canada — Modèle de surveillance antiterroriste",
            sub1_mass_surveillance_rights_violation=1.5,
            sub2_arbitrary_detention_terrorism_pretext=1.2,
            sub3_due_process_fair_trial_deficit=1.0,
            sub4_civil_society_restriction=0.8,
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_mass_surveillance_rights_violation": e.sub1_mass_surveillance_rights_violation,
            "sub2_arbitrary_detention_terrorism_pretext": e.sub2_arbitrary_detention_terrorism_pretext,
            "sub3_due_process_fair_trial_deficit": e.sub3_due_process_fair_trial_deficit,
            "sub4_civil_society_restriction": e.sub4_civil_society_restriction,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_anti_terrorism_counter_extremism_rights_index": e.estimated_anti_terrorism_counter_extremism_rights_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "anti_terrorism_counter_extremism_rights_engine",
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
