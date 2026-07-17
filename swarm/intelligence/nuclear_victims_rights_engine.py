from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — exposition aux radiations et impacts sanitaires documentés
    sub2: float  # ×0.25 — déni institutionnel et absence de reconnaissance juridique
    sub3: float  # ×0.25 — absence de réparation / indemnisation / décontamination
    sub4: float  # ×0.20 — déplacements forcés et perte de territoires ancestraux

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
            entity_id="NVR-001",
            name="Îles Marshall — essais nucléaires US et contamination permanente",
            sub1=90.0, sub2=85.0, sub3=88.0, sub4=92.0
        ),
        EntityScore(
            entity_id="NVR-002",
            name="Kazakhstan — victimes des essais soviétiques de Semipalatinsk",
            sub1=82.0, sub2=78.0, sub3=75.0, sub4=80.0
        ),
        EntityScore(
            entity_id="NVR-003",
            name="Japon — hibakusha de Hiroshima/Nagasaki et discriminations persistantes",
            sub1=70.0, sub2=65.0, sub3=60.0, sub4=62.0
        ),
        EntityScore(
            entity_id="NVR-004",
            name="Algérie — essais français au Sahara et déni de réparation",
            sub1=72.0, sub2=80.0, sub3=74.0, sub4=58.0
        ),
        EntityScore(
            entity_id="NVR-005",
            name="Ukraine — liquidateurs de Tchernobyl sous-indemnisés",
            sub1=52.0, sub2=50.0, sub3=55.0, sub4=46.0
        ),
        EntityScore(
            entity_id="NVR-006",
            name="Polynésie française — essais du Pacifique et maladies reconnues tardivement",
            sub1=46.0, sub2=54.0, sub3=48.0, sub4=44.0
        ),
        EntityScore(
            entity_id="NVR-007",
            name="États-Unis — Downwinders et Native American uranium miners",
            sub1=30.0, sub2=28.0, sub3=32.0, sub4=26.0
        ),
        EntityScore(
            entity_id="NVR-008",
            name="Australie — essais britanniques à Maralinga — réparations partielles",
            sub1=14.0, sub2=12.0, sub3=16.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("NUCLEAR VICTIMS RIGHTS ENGINE — Wave 130")
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
        "engine": "nuclear_victims_rights_engine",
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
                "estimated_nuclear_victims_index": e.estimated_index,
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
