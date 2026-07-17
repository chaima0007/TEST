from dataclasses import dataclass, field
from typing import List, Dict
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — cadre légal (lois NCII, deepfake, revenge porn)
    sub2: float  # ×0.25 — impunité & taux de condamnation
    sub3: float  # ×0.25 — accès recours victimes & plateformes
    sub4: float  # ×0.20 — stigmatisation sociale & revictimisation
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
        EntityScore("PH", "Philippines",         sub1=82, sub2=80, sub3=75, sub4=78),
        EntityScore("IN", "Inde",                sub1=80, sub2=78, sub3=72, sub4=76),
        EntityScore("MX", "Mexique",             sub1=78, sub2=76, sub3=70, sub4=74),
        EntityScore("NG", "Nigéria",             sub1=76, sub2=74, sub3=68, sub4=72),
        EntityScore("US", "États-Unis",          sub1=52, sub2=50, sub3=45, sub4=48),
        EntityScore("AU", "Australie",           sub1=48, sub2=46, sub3=42, sub4=44),
        EntityScore("FR", "France",              sub1=28, sub2=26, sub3=30, sub4=32),
        EntityScore("UK", "Royaume-Uni",         sub1=12, sub2=10, sub3=14, sub4=16),
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
            "estimated_ncii_abuse_index": e.estimated_index,
            "sub_scores": {
                "legal_framework_ncii_deepfake": e.sub1,
                "impunity_conviction_rate": e.sub2,
                "victim_recourse_platform_access": e.sub3,
                "social_stigma_revictimization": e.sub4,
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
        "engine": "nonconsensual_intimate_image_abuse_engine",
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
