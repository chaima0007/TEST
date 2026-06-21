#!/usr/bin/env python3
"""Albinism Persecution Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — violence physique, meurtres rituels et trafic de membres
    sub2: float  # ×0.25 — impunité judiciaire et absence de poursuites effectives
    sub3: float  # ×0.25 — stigmatisation sociale, exclusion communautaire et familiale
    sub4: float  # ×0.20 — accès aux soins, protection UV et soutien psychosocial

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_index: float = field(init=False)

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
        self.estimated_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="APR-001",
            name="Tanzanie — meurtres rituels et trafic de membres albinos parmi les plus documentés",
            sub1=92.0, sub2=85.0, sub3=88.0, sub4=80.0
        ),
        EntityScore(
            entity_id="APR-002",
            name="Malawi — vague d'attaques 2014-2018, exhumations de tombes albinos",
            sub1=88.0, sub2=82.0, sub3=84.0, sub4=76.0
        ),
        EntityScore(
            entity_id="APR-003",
            name="Mozambique — persécutions liées à la médecine traditionnelle et trafic transfrontalier",
            sub1=82.0, sub2=78.0, sub3=80.0, sub4=70.0
        ),
        EntityScore(
            entity_id="APR-004",
            name="Zambie — stigmatisation extrême et violences rituelles dans les zones rurales isolées",
            sub1=76.0, sub2=72.0, sub3=78.0, sub4=65.0
        ),
        EntityScore(
            entity_id="APR-005",
            name="Rwanda — discrimination sociale persistante malgré législation anti-discrimination",
            sub1=52.0, sub2=48.0, sub3=58.0, sub4=44.0
        ),
        EntityScore(
            entity_id="APR-006",
            name="Kenya — harcèlement communautaire et abandon scolaire des enfants albinos",
            sub1=50.0, sub2=46.0, sub3=54.0, sub4=42.0
        ),
        EntityScore(
            entity_id="APR-007",
            name="Cameroun — exclusion familiale et accès limité aux soins dermatologiques",
            sub1=32.0, sub2=28.0, sub3=35.0, sub4=24.0
        ),
        EntityScore(
            entity_id="APR-008",
            name="Afrique du Sud — cadre juridique renforcé, accès aux soins amélioré",
            sub1=14.0, sub2=10.0, sub3=12.0, sub4=16.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("ALBINISM PERSECUTION RIGHTS ENGINE — Wave 136")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:55]:<55s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    output = {
        "engine": "albinism_persecution_rights_engine",
        "wave": 136,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1": e.sub1,
                "sub2": e.sub2,
                "sub3": e.sub3,
                "sub4": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_albinism_persecution_index": e.estimated_index,
            }
            for e in entities
        ],
        "avg_composite": round(avg, 2),
        "distribution": dist,
    }
    print()
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
