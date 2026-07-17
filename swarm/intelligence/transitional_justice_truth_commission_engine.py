from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # truth_revelation ×0.30
    sub2: float  # accountability_mechanisms ×0.25
    sub3: float  # victim_participation ×0.25
    sub4: float  # institutional_reform ×0.20
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
    EntityScore("TJ001", "Sierra Leone — Truth and Reconciliation Commission", 88.0, 85.0, 80.0, 75.0),
    EntityScore("TJ002", "South Africa — TRC Apartheid Legacy", 82.0, 78.0, 85.0, 70.0),
    EntityScore("TJ003", "Rwanda — Gacaca Community Courts", 79.0, 83.0, 76.0, 72.0),
    EntityScore("TJ004", "Colombia — JEP Special Jurisdiction for Peace", 75.0, 72.0, 78.0, 68.0),
    # 2 élevé (40–59)
    EntityScore("TJ005", "Guatemala — Historical Clarification Commission", 55.0, 50.0, 52.0, 48.0),
    EntityScore("TJ006", "Tunisia — Truth and Dignity Instance", 50.0, 53.0, 48.0, 45.0),
    # 1 modéré (20–39)
    EntityScore("TJ007", "Philippines — Non-Formal Truth Commission", 35.0, 30.0, 32.0, 28.0),
    # 1 faible (<20)
    EntityScore("TJ008", "Cambodia — ECCC Outreach Deficit", 15.0, 12.0, 18.0, 10.0),
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
            "sub1_truth_revelation": entity.sub1,
            "sub2_accountability_mechanisms": entity.sub2,
            "sub3_victim_participation": entity.sub3,
            "sub4_institutional_reform": entity.sub4,
            "composite_score": entity.composite_score,
            "risk_level": entity.risk_level,
            "estimated_transitional_justice_index": entity.estimated_index,
        })

    avg = round(total_composite / len(ENTITIES), 2)

    return {
        "engine": "transitional_justice_truth_commission_engine",
        "domain": "Transitional Justice & Truth Commissions",
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
