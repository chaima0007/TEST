from dataclasses import dataclass, field
from typing import List, Dict
import json

@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # ×0.30 — écart salarial femmes/hommes (pay gap percentage)
    sub2: float  # ×0.25 — exclusion marché travail femmes
    sub3: float  # ×0.25 — droits propriété et héritage
    sub4: float  # ×0.20 — écart inclusion financière

    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_gender_equity_index: float = field(init=False)

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
        self.estimated_gender_equity_index = round(self.composite_score / 100 * 10, 2)


def run_engine() -> List[EntityScore]:
    entities = [
        EntityScore(
            entity_id="GPG-001",
            name="Yemen — femmes < 6% de la population active",
            sub1=95.0, sub2=96.0, sub3=88.0, sub4=84.0
        ),
        EntityScore(
            entity_id="GPG-002",
            name="Pakistan — 25% écart salarial et forte exclusion du marché du travail",
            sub1=88.0, sub2=90.0, sub3=82.0, sub4=76.0
        ),
        EntityScore(
            entity_id="GPG-003",
            name="Inde — gender gap rural profond et droits fonciers limités",
            sub1=80.0, sub2=82.0, sub3=76.0, sub4=70.0
        ),
        EntityScore(
            entity_id="GPG-004",
            name="Égypte — lois d'héritage inégales et exclusion financière",
            sub1=74.0, sub2=75.0, sub3=72.0, sub4=65.0
        ),
        EntityScore(
            entity_id="GPG-005",
            name="Mexique — maquiladoras : écart salarial structurel",
            sub1=58.0, sub2=56.0, sub3=52.0, sub4=50.0
        ),
        EntityScore(
            entity_id="GPG-006",
            name="USA — 78 cents pour 1 dollar : persistance de l'écart salarial",
            sub1=48.0, sub2=48.0, sub3=46.0, sub4=44.0
        ),
        EntityScore(
            entity_id="GPG-007",
            name="France — 16% d'écart résiduel malgré les lois d'égalité",
            sub1=30.0, sub2=28.0, sub3=26.0, sub4=26.0
        ),
        EntityScore(
            entity_id="GPG-008",
            name="Islande — 5% d'écart salarial, loi d'égalité salariale en vigueur",
            sub1=10.0, sub2=10.0, sub3=10.0, sub4=10.0
        ),
    ]
    return entities


def main():
    entities = run_engine()

    print("=" * 60)
    print("GENDER PAY GAP & ECONOMIC RIGHTS ENGINE — Wave 166")
    print("=" * 60)

    dist: Dict[str, int] = {}
    total = 0.0

    for e in entities:
        dist[e.risk_level] = dist.get(e.risk_level, 0) + 1
        total += e.composite_score
        print(
            f"[{e.risk_level.upper():8s}] {e.name[:50]:<50s} "
            f"composite={e.composite_score:.2f}  index={e.estimated_gender_equity_index:.2f}"
        )

    avg = total / len(entities)

    print()
    print(f"avg_composite : {avg:.2f}")
    print(f"Distribution  : critique={dist.get('critique',0)} | élevé={dist.get('élevé',0)} | modéré={dist.get('modéré',0)} | faible={dist.get('faible',0)}")
    ok = (dist.get('critique',0)==4 and dist.get('élevé',0)==2 and dist.get('modéré',0)==1 and dist.get('faible',0)==1)
    print(f"Distribution OK : {'✓' if ok else '✗'}")

    assert ok, f"Distribution invalide : {dist}"

    output = {
        "engine": "gender_pay_gap_economic_rights_engine",
        "wave": 166,
        "entities": [
            {
                "entity_id": e.entity_id,
                "name": e.name,
                "sub1_pay_gap_percentage": e.sub1,
                "sub2_labor_market_exclusion": e.sub2,
                "sub3_property_inheritance_rights": e.sub3,
                "sub4_financial_inclusion_gap": e.sub4,
                "composite_score": e.composite_score,
                "risk_level": e.risk_level,
                "estimated_gender_equity_index": e.estimated_gender_equity_index,
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
