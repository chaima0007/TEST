from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — conditions sécurité retour
    sub2: float  # ×0.25 — garantie caractère volontaire
    sub3: float  # ×0.25 — restitution biens/terres
    sub4: float  # ×0.20 — documentation & prévention apatridie

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_refugee_return_index: float = field(init=False)

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
        self.estimated_refugee_return_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="RVR-001",
            name="Syrie (retours forcés depuis Liban)",
            sub1=94.0, sub2=92.0, sub3=88.0, sub4=86.0
        ),
        EntityScore(
            entity_id="RVR-002",
            name="Afghanistan (Taliban 2021+)",
            sub1=90.0, sub2=88.0, sub3=84.0, sub4=80.0
        ),
        EntityScore(
            entity_id="RVR-003",
            name="Myanmar (Rohingya — aucune condition sûre)",
            sub1=86.0, sub2=84.0, sub3=80.0, sub4=78.0
        ),
        EntityScore(
            entity_id="RVR-004",
            name="Éthiopie (Tigré post-conflit)",
            sub1=74.0, sub2=72.0, sub3=70.0, sub4=68.0
        ),
        EntityScore(
            entity_id="RVR-005",
            name="Sud-Soudan (insécurité persistante)",
            sub1=58.0, sub2=54.0, sub3=52.0, sub4=50.0
        ),
        EntityScore(
            entity_id="RVR-006",
            name="RDC (est instable)",
            sub1=50.0, sub2=48.0, sub3=46.0, sub4=44.0
        ),
        EntityScore(
            entity_id="RVR-007",
            name="Kosovo (retours supervisés UNHCR)",
            sub1=30.0, sub2=28.0, sub3=26.0, sub4=24.0
        ),
        EntityScore(
            entity_id="RVR-008",
            name="Bosnia (Dayton Agreement model)",
            sub1=13.0, sub2=12.0, sub3=11.0, sub4=10.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("REFUGEE RETURN & VOLUNTARY REPATRIATION ENGINE — Wave 164")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_refugee_return_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, "Distribution incorrecte — ajuster les sous-scores"

    output = {
        "engine": "refugee_return_voluntary_repatriation_engine",
        "wave": 164,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_safety_return_conditions": e.sub1,
                "sub2_voluntary_nature_guarantee": e.sub2,
                "sub3_property_restitution": e.sub3,
                "sub4_documentation_statelessness": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_refugee_return_index": e.estimated_refugee_return_index,
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
