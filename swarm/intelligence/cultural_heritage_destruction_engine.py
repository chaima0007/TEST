from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — destruction délibérée de sites patrimoniaux
    sub2: float  # ×0.25 — pillage et trafic d'antiquités
    sub3: float  # ×0.25 — destructions collatérales lors de conflits
    sub4: float  # ×0.20 — absence de cadre légal de protection

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_heritage_protection_index: float = field(init=False)

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
        self.estimated_heritage_protection_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="CHD-001",
            name="Syrie — Palmyre et Alep : sites UNESCO bombardés",
            sub1=98.0, sub2=92.0, sub3=96.0, sub4=88.0
        ),
        EntityScore(
            entity_id="CHD-002",
            name="Irak — Daesh à Mossoul : bibliothèque et musées détruits",
            sub1=96.0, sub2=90.0, sub3=88.0, sub4=86.0
        ),
        EntityScore(
            entity_id="CHD-003",
            name="Mali — Tombouctou : mosquées et mausolées détruits",
            sub1=87.0, sub2=80.0, sub3=82.0, sub4=80.0
        ),
        EntityScore(
            entity_id="CHD-004",
            name="Yemen — sites UNESCO bombardés dans le conflit",
            sub1=82.0, sub2=75.0, sub3=80.0, sub4=72.0
        ),
        EntityScore(
            entity_id="CHD-005",
            name="Libye — Cyrène et sites antiques pillés dans l'instabilité",
            sub1=60.0, sub2=62.0, sub3=52.0, sub4=52.0
        ),
        EntityScore(
            entity_id="CHD-006",
            name="Afghanistan — Bouddhas de Bamiyan : héritage de destruction",
            sub1=55.0, sub2=52.0, sub3=50.0, sub4=48.0
        ),
        EntityScore(
            entity_id="CHD-007",
            name="Cambodge — pillage Khmer rouge et trafic post-conflit",
            sub1=32.0, sub2=34.0, sub3=28.0, sub4=26.0
        ),
        EntityScore(
            entity_id="CHD-008",
            name="Grèce — restitution des marbres d'Elgin, enjeu légal",
            sub1=12.0, sub2=16.0, sub3=10.0, sub4=14.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("CULTURAL HERITAGE DESTRUCTION ENGINE — Wave 166")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_heritage_protection_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, f"Distribution invalide : {dist}"

    output = {
        "engine": "cultural_heritage_destruction_engine",
        "wave": 166,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_deliberate_destruction": e.sub1,
                "sub2_looting_trafficking": e.sub2,
                "sub3_conflict_collateral": e.sub3,
                "sub4_legal_framework_absence": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_heritage_protection_index": e.estimated_heritage_protection_index,
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
