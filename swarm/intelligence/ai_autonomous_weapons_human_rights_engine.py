from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — sub1_lethal_autonomous_development: Développement armes autonomes létales
    sub2: float  # ×0.25 — sub2_human_rights_impact: Impact droits humains documenté
    sub3: float  # ×0.25 — sub3_international_law_compliance: Conformité droit international humanitaire
    sub4: float  # ×0.20 — sub4_transparency_accountability: Transparence et responsabilité

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_ai_weapons_index: float = field(init=False)

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
        self.estimated_ai_weapons_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="AAW-001",
            name="Israël (Lavender AI targeting system)",
            sub1=90.0, sub2=92.0, sub3=88.0, sub4=84.0
        ),
        EntityScore(
            entity_id="AAW-002",
            name="USA (Project Maven + drone kill chain)",
            sub1=84.0, sub2=80.0, sub3=82.0, sub4=78.0
        ),
        EntityScore(
            entity_id="AAW-003",
            name="Chine (LAWS développement accéléré)",
            sub1=88.0, sub2=84.0, sub3=86.0, sub4=80.0
        ),
        EntityScore(
            entity_id="AAW-004",
            name="Russie (KUB-BLA autonome Ukraine)",
            sub1=80.0, sub2=78.0, sub3=76.0, sub4=74.0
        ),
        EntityScore(
            entity_id="AAW-005",
            name="Turquie (Kargu-2 Libye)",
            sub1=62.0, sub2=58.0, sub3=56.0, sub4=58.0
        ),
        EntityScore(
            entity_id="AAW-006",
            name="Corée du Sud (Super aEgis II)",
            sub1=52.0, sub2=50.0, sub3=50.0, sub4=52.0
        ),
        EntityScore(
            entity_id="AAW-007",
            name="UK (drone Reaper humain-dans-boucle)",
            sub1=28.0, sub2=26.0, sub3=24.0, sub4=30.0
        ),
        EntityScore(
            entity_id="AAW-008",
            name="Autriche (traité ban LAWS)",
            sub1=8.0, sub2=9.0, sub3=7.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("AI AUTONOMOUS WEAPONS & HUMAN RIGHTS ENGINE — Wave 165")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_ai_weapons_index:.2f}"
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
        "engine": "ai_autonomous_weapons_human_rights_engine",
        "wave": 165,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_lethal_autonomous_development": e.sub1,
                "sub2_human_rights_impact": e.sub2,
                "sub3_international_law_compliance": e.sub3,
                "sub4_transparency_accountability": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_ai_weapons_index": e.estimated_ai_weapons_index,
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
