from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Executions per capita & death row population ×0.30
    sub2: float  # Procedural fairness & access to legal defence ×0.25
    sub3: float  # Political will & abolitionist movement strength ×0.25
    sub4: float  # International treaty compliance & reporting ×0.20

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
            entity_id="CHN",
            name="China",
            sub1=95.0, sub2=88.0, sub3=90.0, sub4=85.0
        ),
        EntityScore(
            entity_id="IRN",
            name="Iran",
            sub1=88.0, sub2=82.0, sub3=84.0, sub4=78.0
        ),
        EntityScore(
            entity_id="SAU",
            name="Saudi Arabia",
            sub1=82.0, sub2=78.0, sub3=80.0, sub4=72.0
        ),
        EntityScore(
            entity_id="PRK",
            name="North Korea",
            sub1=80.0, sub2=76.0, sub3=78.0, sub4=70.0
        ),
        # 2 élevé (40–59)
        EntityScore(
            entity_id="USA",
            name="United States",
            sub1=52.0, sub2=48.0, sub3=45.0, sub4=42.0
        ),
        EntityScore(
            entity_id="EGY",
            name="Egypt",
            sub1=55.0, sub2=50.0, sub3=48.0, sub4=44.0
        ),
        # 1 modéré (20–39)
        EntityScore(
            entity_id="JPN",
            name="Japan",
            sub1=32.0, sub2=28.0, sub3=25.0, sub4=22.0
        ),
        # 1 faible (<20)
        EntityScore(
            entity_id="FRA",
            name="France",
            sub1=5.0, sub2=6.0, sub3=4.0, sub4=5.0
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_death_penalty_abolition_index": e.estimated_index,
            "sub_scores": {
                "executions_per_capita_death_row": e.sub1,
                "procedural_fairness_legal_defence": e.sub2,
                "political_will_abolitionist_strength": e.sub3,
                "treaty_compliance_reporting": e.sub4,
            }
        })

    avg = round(sum(e.composite_score for e in entities) / len(entities), 2)
    dist: Dict[str, int] = {}
    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1

    output = {
        "engine": "death_penalty_abolition_rights_engine",
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
