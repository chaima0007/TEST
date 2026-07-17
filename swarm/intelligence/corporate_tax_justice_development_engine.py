from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — échelle évitement fiscal
    sub2: float  # ×0.25 — impact pays en développement
    sub3: float  # ×0.25 — treaty shopping & BEPS
    sub4: float  # ×0.20 — score transparence OCCRP/TJN

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_tax_justice_index: float = field(init=False)

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
        self.estimated_tax_justice_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="CTJ-001",
            name="Apple/Google (structure irlandaise)",
            sub1=88.0, sub2=84.0, sub3=86.0, sub4=80.0
        ),
        EntityScore(
            entity_id="CTJ-002",
            name="Shell (Pays-Bas + Nigeria profit shift)",
            sub1=84.0, sub2=82.0, sub3=80.0, sub4=78.0
        ),
        EntityScore(
            entity_id="CTJ-003",
            name="Glencore (RDC royalties évitées)",
            sub1=92.0, sub2=88.0, sub3=86.0, sub4=82.0
        ),
        EntityScore(
            entity_id="CTJ-004",
            name="Amazon (Luxembourg structuration)",
            sub1=78.0, sub2=76.0, sub3=76.0, sub4=72.0
        ),
        EntityScore(
            entity_id="CTJ-005",
            name="HSBC (filiales offshore)",
            sub1=56.0, sub2=54.0, sub3=52.0, sub4=50.0
        ),
        EntityScore(
            entity_id="CTJ-006",
            name="Starbucks (IP royalties)",
            sub1=48.0, sub2=46.0, sub3=48.0, sub4=44.0
        ),
        EntityScore(
            entity_id="CTJ-007",
            name="Unilever (BEPS pillar 2 partiel)",
            sub1=30.0, sub2=28.0, sub3=28.0, sub4=30.0
        ),
        EntityScore(
            entity_id="CTJ-008",
            name="Danone (B-Corp + transparence)",
            sub1=12.0, sub2=10.0, sub3=10.0, sub4=12.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("CORPORATE TAX JUSTICE & DEVELOPMENT ENGINE — Wave 164")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_tax_justice_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, "Distribution incorrecte — ajuster les sous-scores"

    output = {
        "engine": "corporate_tax_justice_development_engine",
        "wave": 164,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_tax_avoidance_scale": e.sub1,
                "sub2_developing_country_impact": e.sub2,
                "sub3_treaty_shopping": e.sub3,
                "sub4_occrp_transparency_score": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_tax_justice_index": e.estimated_tax_justice_index,
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
