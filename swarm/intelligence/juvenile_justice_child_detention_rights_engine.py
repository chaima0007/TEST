#!/usr/bin/env python3
"""Juvenile Justice Child Detention Rights Engine — Caelum Partners Swarm Intelligence"""
from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — détention d'enfants en conflit avec la loi (préventive, longue durée, mixte adultes)
    sub2: float  # ×0.25 — manque d'alternatives à la détention et absence de tribunaux spécialisés
    sub3: float  # ×0.25 — conditions de détention (violence, abus, éducation, santé mentale)
    sub4: float  # ×0.20 — accès à la représentation juridique et recours effectifs pour mineurs

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
            entity_id="JJD-001",
            name="Philippines — détention massive d'enfants, guerre anti-drogue et centres surpeuplés",
            sub1=90.0, sub2=88.0, sub3=86.0, sub4=82.0
        ),
        EntityScore(
            entity_id="JJD-002",
            name="États-Unis — détention d'enfants migrants, centres privatisés, isolement cellulaire",
            sub1=84.0, sub2=80.0, sub3=82.0, sub4=78.0
        ),
        EntityScore(
            entity_id="JJD-003",
            name="Pakistan — enfants détenus avec adultes, torture documentée, système féodal informel",
            sub1=82.0, sub2=85.0, sub3=80.0, sub4=76.0
        ),
        EntityScore(
            entity_id="JJD-004",
            name="Kenya — détention préventive prolongée de mineurs, manque de tribunaux pour enfants",
            sub1=76.0, sub2=78.0, sub3=74.0, sub4=70.0
        ),
        EntityScore(
            entity_id="JJD-005",
            name="Brésil (FEBEM/CASE) — violences institutionnelles dans centres socio-éducatifs",
            sub1=55.0, sub2=52.0, sub3=58.0, sub4=48.0
        ),
        EntityScore(
            entity_id="JJD-006",
            name="Inde — détention arbitraire de mineurs tribaux et Dalits, accès défenseur rare",
            sub1=52.0, sub2=50.0, sub3=54.0, sub4=46.0
        ),
        EntityScore(
            entity_id="JJD-007",
            name="France — quartiers mineurs surpeuplés, durées de détention provisoire en hausse",
            sub1=30.0, sub2=28.0, sub3=26.0, sub4=24.0
        ),
        EntityScore(
            entity_id="JJD-008",
            name="Norvège — justice restaurative, alternatives systématiques, recours indépendants",
            sub1=10.0, sub2=8.0, sub3=10.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("JUVENILE JUSTICE CHILD DETENTION RIGHTS ENGINE — Wave 136")
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
        "engine": "juvenile_justice_child_detention_rights_engine",
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
                "estimated_juvenile_justice_child_detention_index": e.estimated_index,
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
