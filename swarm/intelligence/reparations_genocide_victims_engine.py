from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # legal_recognition ×0.30
    sub2: float  # reparation_programs ×0.25
    sub3: float  # victim_access ×0.25
    sub4: float  # memory_preservation ×0.20
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
    EntityScore("RGV001", "Armenia — Ottoman Genocide Reparations Denial", 92.0, 88.0, 85.0, 90.0),
    EntityScore("RGV002", "Rwanda — Genocide Survivors Fund Gaps", 80.0, 75.0, 78.0, 72.0),
    EntityScore("RGV003", "Namibia — Herero & Nama Genocide Redress", 76.0, 70.0, 72.0, 68.0),
    EntityScore("RGV004", "Bosnia — Srebrenica Survivors Reparations", 72.0, 68.0, 74.0, 65.0),
    # 2 élevé (40–59)
    EntityScore("RGV005", "Cambodia — Khmer Rouge Survivor Compensation", 55.0, 52.0, 48.0, 50.0),
    EntityScore("RGV006", "Bangladesh — 1971 Liberation War Victims", 50.0, 48.0, 52.0, 45.0),
    # 1 modéré (20–39)
    EntityScore("RGV007", "Iraq — Yazidi Survivors Reparation Program", 35.0, 30.0, 28.0, 32.0),
    # 1 faible (<20)
    EntityScore("RGV008", "Myanmar — Rohingya Reparation Prospects", 14.0, 10.0, 12.0, 8.0),
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
            "sub1_legal_recognition": entity.sub1,
            "sub2_reparation_programs": entity.sub2,
            "sub3_victim_access": entity.sub3,
            "sub4_memory_preservation": entity.sub4,
            "composite_score": entity.composite_score,
            "risk_level": entity.risk_level,
            "estimated_reparations_genocide_index": entity.estimated_index,
        })

    avg = round(total_composite / len(ENTITIES), 2)

    return {
        "engine": "reparations_genocide_victims_engine",
        "domain": "Reparations for Genocide Victims",
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
