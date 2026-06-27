from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — prévalence des attaques à l'acide et impunité
    sub2: float  # ×0.25 — défaillance législative et application pénale
    sub3: float  # ×0.25 — stigmatisation sociale et exclusion des survivantes
    sub4: float  # ×0.20 — accès aux soins médicaux / reconstruction / soutien psychologique

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
            entity_id="AAG-001",
            name="Bangladesh — taux d'attaques à l'acide parmi les plus élevés au monde",
            sub1=85.0, sub2=78.0, sub3=80.0, sub4=72.0
        ),
        EntityScore(
            entity_id="AAG-002",
            name="Pakistan — impunité systémique et rejet familial des victimes",
            sub1=80.0, sub2=82.0, sub3=78.0, sub4=68.0
        ),
        EntityScore(
            entity_id="AAG-003",
            name="Inde — incidents ruraux non signalés et accès à l'acide facilité",
            sub1=75.0, sub2=70.0, sub3=72.0, sub4=65.0
        ),
        EntityScore(
            entity_id="AAG-004",
            name="Cambodge — violences conjugales à l'acide et corruption judiciaire",
            sub1=70.0, sub2=74.0, sub3=68.0, sub4=62.0
        ),
        EntityScore(
            entity_id="AAG-005",
            name="Éthiopie — agressions liées aux conflits de terres et dot",
            sub1=50.0, sub2=48.0, sub3=55.0, sub4=44.0
        ),
        EntityScore(
            entity_id="AAG-006",
            name="Ouganda — stigmatisation persistante et manque de chirurgie réparatrice",
            sub1=46.0, sub2=44.0, sub3=52.0, sub4=42.0
        ),
        EntityScore(
            entity_id="AAG-007",
            name="Iran — cas liés au contrôle des femmes dans les espaces publics",
            sub1=32.0, sub2=30.0, sub3=28.0, sub4=25.0
        ),
        EntityScore(
            entity_id="AAG-008",
            name="Royaume-Uni — attaques en hausse mais dispositif légal renforcé",
            sub1=15.0, sub2=10.0, sub3=12.0, sub4=14.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("ACID ATTACK & GENDER VIOLENCE ENGINE — Wave 130")
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
        "engine": "acid_attack_gender_violence_engine",
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
                "estimated_acid_attack_index": e.estimated_index,
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
