from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Prevalence of witch-hunt accusations ×0.30
    sub2: float  # State/community impunity for perpetrators ×0.25
    sub3: float  # Victim vulnerability & displacement ×0.25
    sub4: float  # Legal protection gaps ×0.20

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
            entity_id="PNG",
            name="Papua New Guinea",
            sub1=85.0, sub2=78.0, sub3=80.0, sub4=72.0
        ),
        EntityScore(
            entity_id="IND_JHK",
            name="India – Jharkhand / tribal belt",
            sub1=80.0, sub2=74.0, sub3=76.0, sub4=68.0
        ),
        EntityScore(
            entity_id="TZA",
            name="Tanzania",
            sub1=78.0, sub2=72.0, sub3=74.0, sub4=66.0
        ),
        EntityScore(
            entity_id="GIN",
            name="Guinea",
            sub1=79.0, sub2=73.0, sub3=75.0, sub4=67.0
        ),
        # 2 élevé (40–59)
        EntityScore(
            entity_id="NGA",
            name="Nigeria – Middle Belt",
            sub1=58.0, sub2=52.0, sub3=54.0, sub4=48.0
        ),
        EntityScore(
            entity_id="COD",
            name="Democratic Republic of Congo",
            sub1=55.0, sub2=50.0, sub3=52.0, sub4=45.0
        ),
        # 1 modéré (20–39)
        EntityScore(
            entity_id="NPL",
            name="Nepal – remote hill districts",
            sub1=38.0, sub2=34.0, sub3=35.0, sub4=30.0
        ),
        # 1 faible (<20)
        EntityScore(
            entity_id="GBR",
            name="United Kingdom – historical legacy cases",
            sub1=12.0, sub2=10.0, sub3=8.0, sub4=9.0
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_witch_hunt_persecution_index": e.estimated_index,
            "sub_scores": {
                "accusation_prevalence": e.sub1,
                "perpetrator_impunity": e.sub2,
                "victim_vulnerability_displacement": e.sub3,
                "legal_protection_gaps": e.sub4,
            }
        })

    avg = round(sum(e.composite_score for e in entities) / len(entities), 2)
    dist: Dict[str, int] = {}
    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1

    output = {
        "engine": "witch_hunt_accusation_persecution_engine",
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
