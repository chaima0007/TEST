from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — sub1_protest_ban_laws: Lois d'interdiction manifestations
    sub2: float  # ×0.25 — sub2_police_brutality_protests: Brutalité policière manifestations
    sub3: float  # ×0.25 — sub3_arrest_detention_protesters: Arrestations manifestants
    sub4: float  # ×0.20 — sub4_assembly_permit_restrictions: Restrictions permis de rassemblement

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_assembly_rights_index: float = field(init=False)

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
        self.estimated_assembly_rights_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="FAP-001",
            name="Chine (Tiananmen legacy + Hong Kong)",
            sub1=96.0, sub2=92.0, sub3=95.0, sub4=88.0
        ),
        EntityScore(
            entity_id="FAP-002",
            name="Belarus (2020 répression)",
            sub1=90.0, sub2=86.0, sub3=89.0, sub4=84.0
        ),
        EntityScore(
            entity_id="FAP-003",
            name="Iran (Mahsa Amini 2022-2024)",
            sub1=88.0, sub2=84.0, sub3=86.0, sub4=80.0
        ),
        EntityScore(
            entity_id="FAP-004",
            name="Russie (anti-guerre 2022+)",
            sub1=84.0, sub2=79.0, sub3=82.0, sub4=76.0
        ),
        EntityScore(
            entity_id="FAP-005",
            name="USA (BLM — force excessive)",
            sub1=52.0, sub2=58.0, sub3=54.0, sub4=50.0
        ),
        EntityScore(
            entity_id="FAP-006",
            name="France (gilets jaunes — LBD)",
            sub1=44.0, sub2=52.0, sub3=46.0, sub4=45.0
        ),
        EntityScore(
            entity_id="FAP-007",
            name="Allemagne (réglementation stricte)",
            sub1=24.0, sub2=22.0, sub3=28.0, sub4=30.0
        ),
        EntityScore(
            entity_id="FAP-008",
            name="Islande (ECHR gold standard)",
            sub1=8.0, sub2=7.0, sub3=9.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("FREEDOM OF ASSEMBLY & PROTEST RIGHTS ENGINE — Wave 165")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_assembly_rights_index:.2f}"
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
        "engine": "freedom_of_assembly_protest_rights_engine",
        "wave": 165,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_protest_ban_laws": e.sub1,
                "sub2_police_brutality_protests": e.sub2,
                "sub3_arrest_detention_protesters": e.sub3,
                "sub4_assembly_permit_restrictions": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_assembly_rights_index": e.estimated_assembly_rights_index,
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
