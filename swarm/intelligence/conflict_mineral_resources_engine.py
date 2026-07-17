from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — financement groupes armés via minerais
    sub2: float  # ×0.25 — déplacement civils autour des mines
    sub3: float  # ×0.25 — travail enfants dans les mines
    sub4: float  # ×0.20 — destruction environnementale

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_conflict_mineral_index: float = field(init=False)

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
        self.estimated_conflict_mineral_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="CMR-001",
            name="RDC Est — cobalt, coltan et or sous contrôle de milices",
            sub1=98.0, sub2=95.0, sub3=92.0, sub4=90.0
        ),
        EntityScore(
            entity_id="CMR-002",
            name="Myanmar — jade et minerais finançant la junte militaire",
            sub1=92.0, sub2=87.0, sub3=82.0, sub4=84.0
        ),
        EntityScore(
            entity_id="CMR-003",
            name="Soudan du Sud — pétrole au cœur du conflit civil",
            sub1=86.0, sub2=84.0, sub3=76.0, sub4=80.0
        ),
        EntityScore(
            entity_id="CMR-004",
            name="Zimbabwe — diamants de Marange et répression étatique",
            sub1=78.0, sub2=74.0, sub3=72.0, sub4=70.0
        ),
        EntityScore(
            entity_id="CMR-005",
            name="Colombie — or et coca finançant groupes armés",
            sub1=60.0, sub2=56.0, sub3=52.0, sub4=50.0
        ),
        EntityScore(
            entity_id="CMR-006",
            name="RCA — diamants et or exploités par groupes armés",
            sub1=62.0, sub2=58.0, sub3=56.0, sub4=54.0
        ),
        EntityScore(
            entity_id="CMR-007",
            name="Pérou — orpaillage illégal en Amazonie (Madre de Dios)",
            sub1=36.0, sub2=32.0, sub3=34.0, sub4=30.0
        ),
        EntityScore(
            entity_id="CMR-008",
            name="Rwanda — certification 3TG et traçabilité minerais",
            sub1=13.0, sub2=11.0, sub3=12.0, sub4=10.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("CONFLICT MINERAL & RESOURCES ENGINE — Wave 166")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_conflict_mineral_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, f"Distribution invalide : {dist}"

    output = {
        "engine": "conflict_mineral_resources_engine",
        "wave": 166,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_armed_group_funding": e.sub1,
                "sub2_civilian_displacement": e.sub2,
                "sub3_child_labor_mining": e.sub3,
                "sub4_environmental_destruction": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_conflict_mineral_index": e.estimated_conflict_mineral_index,
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
