from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — discrimination institutionnelle / politiques âgistes
    sub2: float  # ×0.25 — violences et maltraitances envers les personnes âgées
    sub3: float  # ×0.25 — exclusion socio-économique / retraite / pauvreté
    sub4: float  # ×0.20 — accès aux soins / abandon médical

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
            entity_id="ERA-001",
            name="Japon — isolement des seniors et suicides liés à l'âge",
            sub1=78.0, sub2=74.0, sub3=80.0, sub4=72.0
        ),
        EntityScore(
            entity_id="ERA-002",
            name="Inde — abandon familial des parents âgés et sans-abri gériatrique",
            sub1=82.0, sub2=78.0, sub3=84.0, sub4=76.0
        ),
        EntityScore(
            entity_id="ERA-003",
            name="États-Unis — discrimination à l'emploi et âgisme systémique",
            sub1=74.0, sub2=66.0, sub3=70.0, sub4=64.0
        ),
        EntityScore(
            entity_id="ERA-004",
            name="Chine — pression confucéenne et maltraitance intrafamiliale silencieuse",
            sub1=72.0, sub2=76.0, sub3=68.0, sub4=70.0
        ),
        EntityScore(
            entity_id="ERA-005",
            name="Brésil — violences en EHPAD et impunité des agresseurs",
            sub1=58.0, sub2=62.0, sub3=56.0, sub4=52.0
        ),
        EntityScore(
            entity_id="ERA-006",
            name="Nigeria — sorcellerie imputée aux personnes âgées et lynchages",
            sub1=54.0, sub2=62.0, sub3=52.0, sub4=50.0
        ),
        EntityScore(
            entity_id="ERA-007",
            name="France — sous-représentation politique et paupérisation des retraités",
            sub1=36.0, sub2=32.0, sub3=38.0, sub4=34.0
        ),
        EntityScore(
            entity_id="ERA-008",
            name="Suède — modèle de protection mais âgisme numérique croissant",
            sub1=14.0, sub2=12.0, sub3=16.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("ELDER RIGHTS & AGEISM ENGINE — Wave 130")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    output = {
        "engine": "elder_rights_ageism_engine",
        "wave": 130,
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
                "estimated_elder_rights_index": e.estimated_index,
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
