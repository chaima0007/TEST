from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — sub1_torture_prevalence: Prévalence torture/mauvais traitements
    sub2: float  # ×0.25 — sub2_overcrowding_rate: Surpopulation carcérale
    sub3: float  # ×0.25 — sub3_legal_oversight_absence: Absence contrôle juridictionnel
    sub4: float  # ×0.20 — sub4_solitary_confinement: Usage isolement prolongé

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_prison_rights_index: float = field(init=False)

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
        self.estimated_prison_rights_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="PCT-001",
            name="Syrie (prisons Assad — Saydnaya)",
            sub1=98.0, sub2=94.0, sub3=97.0, sub4=92.0
        ),
        EntityScore(
            entity_id="PCT-002",
            name="Corée du Nord (gwalliso camps)",
            sub1=99.0, sub2=96.0, sub3=98.0, sub4=94.0
        ),
        EntityScore(
            entity_id="PCT-003",
            name="Érythrée (Sawa + prisons secrètes)",
            sub1=92.0, sub2=88.0, sub3=93.0, sub4=86.0
        ),
        EntityScore(
            entity_id="PCT-004",
            name="Libye (centres detention migrants)",
            sub1=85.0, sub2=82.0, sub3=84.0, sub4=79.0
        ),
        EntityScore(
            entity_id="PCT-005",
            name="Philippines (drug war prisons)",
            sub1=58.0, sub2=60.0, sub3=54.0, sub4=50.0
        ),
        EntityScore(
            entity_id="PCT-006",
            name="USA (solitary confinement)",
            sub1=46.0, sub2=44.0, sub3=50.0, sub4=55.0
        ),
        EntityScore(
            entity_id="PCT-007",
            name="France (surpopulation chronique)",
            sub1=26.0, sub2=38.0, sub3=24.0, sub4=28.0
        ),
        EntityScore(
            entity_id="PCT-008",
            name="Norvège (réhabilitation modèle)",
            sub1=6.0, sub2=8.0, sub3=5.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("PRISON CONDITIONS & TORTURE ENGINE — Wave 165")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_prison_rights_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert dist.get('critique', 0) == 4, f"Expected 4 critique, got {dist.get('critique', 0)}"
    assert dist.get('élevé', 0) == 2, f"Expected 2 élevé, got {dist.get('élevé', 0)}"
    assert dist.get('modéré', 0) == 1, f"Expected 1 modéré, got {dist.get('modéré', 0)}"
    assert dist.get('faible', 0) == 1, f"Expected 1 faible, got {dist.get('faible', 0)}"

    output = {
        "engine": "prison_conditions_torture_engine",
        "wave": 165,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_torture_prevalence": e.sub1,
                "sub2_overcrowding_rate": e.sub2,
                "sub3_legal_oversight_absence": e.sub3,
                "sub4_solitary_confinement": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_prison_rights_index": e.estimated_prison_rights_index,
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
