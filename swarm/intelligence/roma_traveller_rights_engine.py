from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # structural_discrimination ×0.30
    sub2: float  # forced_eviction_statelessness ×0.25
    sub3: float  # education_access ×0.25
    sub4: float  # political_representation ×0.20
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


ENTITIES: List[EntityScore] = [
    # 4 critique (≥60)
    EntityScore("RT001", "Bulgaria — Roma Segregated Schooling & Evictions", 88.0, 82.0, 85.0, 70.0),
    EntityScore("RT002", "Romania — Roma Forced Evictions & Statelessness", 84.0, 80.0, 78.0, 68.0),
    EntityScore("RT003", "Slovakia — Coercive Sterilisation & Segregation", 80.0, 75.0, 82.0, 65.0),
    EntityScore("RT004", "France — Irish Traveller Camp Demolitions", 74.0, 72.0, 68.0, 62.0),
    # 2 élevé (40–59)
    EntityScore("RT005", "Spain — Gitano Community Discrimination", 55.0, 50.0, 52.0, 48.0),
    EntityScore("RT006", "Hungary — Anti-Roma Hate Crime Impunity", 52.0, 54.0, 48.0, 44.0),
    # 1 modéré (20–39)
    EntityScore("RT007", "Germany — Sinti & Roma Memorial Exclusion", 30.0, 35.0, 28.0, 32.0),
    # 1 faible (<20)
    EntityScore("RT008", "Sweden — Nordic Roma Integration Programs", 16.0, 14.0, 18.0, 12.0),
]


def run_analysis() -> Dict:
    results = []
    dist: Dict[str, int] = {}
    total_composite = 0.0

    for entity in ENTITIES:
        dist[entity.risk_level] = dist.get(entity.risk_level, 0) + 1
        total_composite += entity.composite_score
        results.append({
            "entity_id": entity.entity_id,
            "name": entity.name,
            "sub1_structural_discrimination": entity.sub1,
            "sub2_forced_eviction_statelessness": entity.sub2,
            "sub3_education_access": entity.sub3,
            "sub4_political_representation": entity.sub4,
            "composite_score": entity.composite_score,
            "risk_level": entity.risk_level,
            "estimated_roma_traveller_rights_index": entity.estimated_index,
        })

    avg = round(total_composite / len(ENTITIES), 2)

    return {
        "engine": "roma_traveller_rights_engine",
        "domain": "Roma & Traveller Rights",
        "total_entities": len(ENTITIES),
        "avg_composite": avg,
        "distribution": dist,
        "entities": results,
    }


if __name__ == "__main__":
    output = run_analysis()
    print(json.dumps(output, indent=2, ensure_ascii=False))
    avg = output["avg_composite"]
    dist = output["distribution"]
    print(f"\navg_composite : {avg:.2f}")
    ok = (
        dist.get("critique", 0) == 4
        and dist.get("élevé", 0) == 2
        and dist.get("modéré", 0) == 1
        and dist.get("faible", 0) == 1
    )
    print(f"Distribution OK : {'✓' if ok else '✗'}")
