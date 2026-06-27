#!/usr/bin/env python3
import json
from dataclasses import dataclass, field


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1_supply_chain_labor_violations: float
    sub2_environmental_rights_destruction: float
    sub3_due_diligence_gap: float
    sub4_remedy_access_victims: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_corporate_human_rights_due_diligence_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (
                self.sub1_supply_chain_labor_violations * 0.30
                + self.sub2_environmental_rights_destruction * 0.25
                + self.sub3_due_diligence_gap * 0.25
                + self.sub4_remedy_access_victims * 0.20
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
        self.estimated_corporate_human_rights_due_diligence_index = round(
            self.composite_score / 100 * 10, 2
        )


def run():
    entities = [
        # 4 critique (composite >= 60)
        EntityScore(
            entity_id="COD_cobalt_ev_batteries",
            name="RDC — Cobalt chaînes batteries EV",
            sub1_supply_chain_labor_violations=9.0,
            sub2_environmental_rights_destruction=8.8,
            sub3_due_diligence_gap=8.5,
            sub4_remedy_access_victims=9.2,
        ),
        EntityScore(
            entity_id="BGD_fast_fashion",
            name="Bangladesh — Fast fashion (travail forcé)",
            sub1_supply_chain_labor_violations=8.5,
            sub2_environmental_rights_destruction=7.5,
            sub3_due_diligence_gap=8.2,
            sub4_remedy_access_victims=8.8,
        ),
        EntityScore(
            entity_id="CIV_cocoa_child_labor",
            name="Côte d'Ivoire — Cacao et travail enfants",
            sub1_supply_chain_labor_violations=8.2,
            sub2_environmental_rights_destruction=7.2,
            sub3_due_diligence_gap=8.0,
            sub4_remedy_access_victims=8.5,
        ),
        EntityScore(
            entity_id="IDN_palm_oil",
            name="Indonésie — Huile de palme déforestation",
            sub1_supply_chain_labor_violations=7.5,
            sub2_environmental_rights_destruction=8.8,
            sub3_due_diligence_gap=7.8,
            sub4_remedy_access_victims=8.0,
        ),
        # 2 élevé (40 <= composite < 60)
        EntityScore(
            entity_id="THA_fishing_slavery",
            name="Thaïlande — Esclavage dans la pêche",
            sub1_supply_chain_labor_violations=5.2,
            sub2_environmental_rights_destruction=4.8,
            sub3_due_diligence_gap=5.0,
            sub4_remedy_access_victims=5.5,
        ),
        EntityScore(
            entity_id="SLE_diamonds_conflict",
            name="Sierra Leone — Diamants conflits",
            sub1_supply_chain_labor_violations=4.8,
            sub2_environmental_rights_destruction=5.0,
            sub3_due_diligence_gap=4.5,
            sub4_remedy_access_victims=5.0,
        ),
        # 1 modéré (20 <= composite < 40)
        EntityScore(
            entity_id="CHL_ARG_lithium",
            name="Chili/Argentine — Lithium et communautés",
            sub1_supply_chain_labor_violations=3.5,
            sub2_environmental_rights_destruction=4.0,
            sub3_due_diligence_gap=3.2,
            sub4_remedy_access_victims=2.8,
        ),
        # 1 faible (composite < 20)
        EntityScore(
            entity_id="APPLE_NIKE_compliance",
            name="Apple/Nike — Conformité CSDDD/UNGPs",
            sub1_supply_chain_labor_violations=1.5,
            sub2_environmental_rights_destruction=1.2,
            sub3_due_diligence_gap=1.8,
            sub4_remedy_access_victims=1.0,
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_supply_chain_labor_violations": e.sub1_supply_chain_labor_violations,
            "sub2_environmental_rights_destruction": e.sub2_environmental_rights_destruction,
            "sub3_due_diligence_gap": e.sub3_due_diligence_gap,
            "sub4_remedy_access_victims": e.sub4_remedy_access_victims,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_corporate_human_rights_due_diligence_index": e.estimated_corporate_human_rights_due_diligence_index,
        })

    avg_composite = round(sum(r["composite_score"] for r in results) / len(results), 2)
    distribution = {}
    for r in results:
        distribution[r["risk_level"]] = distribution.get(r["risk_level"], 0) + 1

    output = {
        "engine": "corporate_human_rights_due_diligence_engine",
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
