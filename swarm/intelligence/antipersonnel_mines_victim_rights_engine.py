from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Density of unexploded mines / contamination ×0.30
    sub2: float  # Civilian casualty rate & demographics ×0.25
    sub3: float  # Victim assistance & rehabilitation gaps ×0.25
    sub4: float  # Clearance capacity & international support ×0.20

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


def run_engine() -> Dict:
    entities: List[EntityScore] = [
        # 4 critique (≥60)
        EntityScore(
            entity_id="AFG",
            name="Afghanistan",
            sub1=92.0, sub2=88.0, sub3=85.0, sub4=80.0
        ),
        EntityScore(
            entity_id="MMR",
            name="Myanmar",
            sub1=82.0, sub2=78.0, sub3=76.0, sub4=70.0
        ),
        EntityScore(
            entity_id="SYR",
            name="Syria",
            sub1=80.0, sub2=76.0, sub3=74.0, sub4=68.0
        ),
        EntityScore(
            entity_id="YEM",
            name="Yemen",
            sub1=78.0, sub2=74.0, sub3=72.0, sub4=66.0
        ),
        # 2 élevé (40–59)
        EntityScore(
            entity_id="UKR",
            name="Ukraine",
            sub1=58.0, sub2=54.0, sub3=50.0, sub4=46.0
        ),
        EntityScore(
            entity_id="CAM",
            name="Cambodia",
            sub1=54.0, sub2=50.0, sub3=48.0, sub4=44.0
        ),
        # 1 modéré (20–39)
        EntityScore(
            entity_id="ANG",
            name="Angola",
            sub1=36.0, sub2=32.0, sub3=30.0, sub4=28.0
        ),
        # 1 faible (<20)
        EntityScore(
            entity_id="CRO",
            name="Croatia",
            sub1=14.0, sub2=12.0, sub3=10.0, sub4=11.0
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_antipersonnel_mines_victim_index": e.estimated_index,
            "sub_scores": {
                "mine_contamination_density": e.sub1,
                "civilian_casualty_rate": e.sub2,
                "victim_assistance_rehabilitation_gaps": e.sub3,
                "clearance_capacity_support": e.sub4,
            }
        })

    avg = round(sum(e.composite_score for e in entities) / len(entities), 2)
    dist: Dict[str, int] = {}
    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1

    output = {
        "engine": "antipersonnel_mines_victim_rights_engine",
        "wave": 131,
        "entities": results,
        "summary": {
            "avg_composite": avg,
            "distribution": dist,
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique', 0) == 4 and dist.get('élevé', 0) == 2 and dist.get('modéré', 0) == 1 and dist.get('faible', 0) == 1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    return output


if __name__ == "__main__":
    run_engine()
