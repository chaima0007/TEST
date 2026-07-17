from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — criminalisation légale (lois anti-vagabondage, campements, etc.)
    sub2: float  # ×0.25 — violences policières sur sans-abri
    sub3: float  # ×0.25 — accès aux services & dignité
    sub4: float  # ×0.20 — poursuites judiciaires & peines alternatives
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
    entities = [
        EntityScore("US", "États-Unis",          sub1=78, sub2=74, sub3=72, sub4=70),
        EntityScore("HU", "Hongrie",              sub1=80, sub2=76, sub3=71, sub4=68),
        EntityScore("BR", "Brésil",               sub1=75, sub2=78, sub3=69, sub4=65),
        EntityScore("IN", "Inde",                 sub1=76, sub2=72, sub3=70, sub4=67),
        EntityScore("ZA", "Afrique du Sud",       sub1=52, sub2=48, sub3=44, sub4=42),
        EntityScore("AU", "Australie",            sub1=50, sub2=45, sub3=43, sub4=40),
        EntityScore("CA", "Canada",               sub1=30, sub2=28, sub3=35, sub4=32),
        EntityScore("FI", "Finlande",             sub1=10, sub2=8,  sub3=12, sub4=15),
    ]

    results = []
    distribution: Dict[str, int] = {}
    total_score = 0.0

    for e in entities:
        distribution[e.risk_level] = distribution.get(e.risk_level, 0) + 1
        total_score += e.composite_score
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_poverty_criminalization_index": e.estimated_index,
            "sub_scores": {
                "criminalization_laws": e.sub1,
                "police_violence_homeless": e.sub2,
                "service_access_dignity": e.sub3,
                "prosecution_alternatives": e.sub4,
            },
        })

    avg = round(total_score / len(entities), 2)
    ok = (
        distribution.get("critique", 0) == 4
        and distribution.get("élevé", 0) == 2
        and distribution.get("modéré", 0) == 1
        and distribution.get("faible", 0) == 1
    )

    output = {
        "engine": "poverty_criminalization_anti_homeless_laws_engine",
        "wave": 135,
        "avg_composite": avg,
        "distribution": distribution,
        "distribution_ok": ok,
        "entities": results,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution OK : {'✓' if ok else '✗'}")
    return output


if __name__ == "__main__":
    run_engine()
