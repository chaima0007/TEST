#!/usr/bin/env python3
"""Toxic Waste Environmental Racism Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — proximité décharges toxiques / sites industriels polluants dans communautés marginalisées
    sub2: float  # ×0.25 — impunité des entreprises et défaillance réglementaire de l'État
    sub3: float  # ×0.25 — impacts sanitaires documentés et accès aux soins des populations exposées
    sub4: float  # ×0.20 — capacité de recours juridique et représentation des victimes

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
            entity_id="TWR-001",
            name="Nigeria (Delta du Niger) — déversements pétroliers Shell/Chevron, communautés Ogoni et Ijaw",
            sub1=95.0, sub2=90.0, sub3=88.0, sub4=85.0
        ),
        EntityScore(
            entity_id="TWR-002",
            name="Ghana (Agbogbloshie) — décharge e-waste, travailleurs informels et plomb atmosphérique",
            sub1=88.0, sub2=84.0, sub3=86.0, sub4=78.0
        ),
        EntityScore(
            entity_id="TWR-003",
            name="États-Unis (Cancer Alley, Louisiane) — complexe pétrochimique, communautés noires rurales",
            sub1=80.0, sub2=75.0, sub3=82.0, sub4=70.0
        ),
        EntityScore(
            entity_id="TWR-004",
            name="Inde (Bhopal, Madhya Pradesh) — héritage Union Carbide, contamination chronique post-1984",
            sub1=78.0, sub2=80.0, sub3=76.0, sub4=72.0
        ),
        EntityScore(
            entity_id="TWR-005",
            name="Zambie (Copperbelt) — contamination au plomb et au cuivre autour des mines Glencore",
            sub1=55.0, sub2=52.0, sub3=58.0, sub4=46.0
        ),
        EntityScore(
            entity_id="TWR-006",
            name="Brésil (Complexe de Cubatão) — pollution industrielle, communautés riveraines pauvres",
            sub1=50.0, sub2=48.0, sub3=52.0, sub4=44.0
        ),
        EntityScore(
            entity_id="TWR-007",
            name="Roumanie (Copsa Mica) — héritage industriel soviet, minorité rom surexposée",
            sub1=32.0, sub2=30.0, sub3=28.0, sub4=26.0
        ),
        EntityScore(
            entity_id="TWR-008",
            name="Pays-Bas (Rotterdam) — exposition portuaire, cadre réglementaire UE protecteur",
            sub1=14.0, sub2=10.0, sub3=12.0, sub4=18.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("TOXIC WASTE ENVIRONMENTAL RACISM RIGHTS ENGINE — Wave 136")
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
        "engine": "toxic_waste_environmental_racism_rights_engine",
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
                "estimated_toxic_waste_environmental_racism_index": e.estimated_index,
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
