from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — étendue historique des internats & politique d'assimilation forcée
    sub2: float  # ×0.25 — impunité & absence de justice transitionnelle
    sub3: float  # ×0.25 — séquelles intergénérationnelles & santé mentale
    sub4: float  # ×0.20 — reconnaissance officielle & réparations
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
        EntityScore("US", "États-Unis",          sub1=82, sub2=78, sub3=76, sub4=72),
        EntityScore("AU", "Australie",           sub1=80, sub2=76, sub3=74, sub4=68),
        EntityScore("CA", "Canada",              sub1=78, sub2=74, sub3=72, sub4=65),
        EntityScore("NZ", "Nouvelle-Zélande",    sub1=74, sub2=70, sub3=68, sub4=60),
        EntityScore("MX", "Mexique",             sub1=55, sub2=50, sub3=48, sub4=45),
        EntityScore("PE", "Pérou",               sub1=52, sub2=48, sub3=45, sub4=42),
        EntityScore("NO", "Norvège",             sub1=30, sub2=24, sub3=28, sub4=15),
        EntityScore("NL", "Pays-Bas",            sub1=10, sub2=8,  sub3=12, sub4=18),
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
            "estimated_assimilation_harm_index": e.estimated_index,
            "sub_scores": {
                "historical_scope_forced_assimilation": e.sub1,
                "impunity_transitional_justice_gap": e.sub2,
                "intergenerational_trauma_mental_health": e.sub3,
                "official_recognition_reparations": e.sub4,
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
        "engine": "residential_school_indigenous_assimilation_engine",
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
