#!/usr/bin/env python3
"""
Wave 144 — Rural Women Land & Inheritance Rights Engine
Scores 8 country contexts on denial of land access, discriminatory inheritance
laws/customs, tenure insecurity, and enforcement failures for rural women.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""
from dataclasses import dataclass, field
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # customary_law_land_denial (0-10)
    sub2: float  # statutory_inheritance_discrimination (0-10)
    sub3: float  # tenure_security_eviction_risk (0-10)
    sub4: float  # legal_remedy_access_failure (0-10)
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    estimated_index: float = field(init=False)

    def __post_init__(self):
        self.composite_score = round(
            (self.sub1 * 0.30 + self.sub2 * 0.25 + self.sub3 * 0.25 + self.sub4 * 0.20) * 10, 2
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


def main():
    entities = [
        # 4 critique
        EntityScore(
            entity_id="NER_rural_women",
            name="Niger — Femmes rurales (droit foncier & héritage)",
            sub1=9.0,   # customary exclusion absolute in most regions
            sub2=8.8,   # statutory law overridden by custom; polygamy compounds dispossession
            sub3=9.1,   # widows systematically evicted by in-laws
            sub4=8.5,   # courts inaccessible (distance, cost, literacy, corruption)
        ),
        EntityScore(
            entity_id="TZA_rural_women",
            name="Tanzanie — Femmes rurales (terre & succession)",
            sub1=8.5,   # customary tenure denies women inheritance in many regions
            sub2=8.0,   # Village Land Act gender provisions poorly enforced
            sub3=8.3,   # widow eviction common after spousal death
            sub4=7.9,   # legal aid absent in rural areas; language barriers
        ),
        EntityScore(
            entity_id="KHM_rural_women",
            name="Cambodge — Femmes rurales (terres & titres)",
            sub1=8.2,   # land concessions disproportionately displace women smallholders
            sub2=7.8,   # communal land titling excludes women heads-of-household
            sub3=8.6,   # forced evictions without compensation gendered impact
            sub4=8.0,   # courts aligned with corporate interests; activists targeted
        ),
        EntityScore(
            entity_id="PAK_rural_women",
            name="Pakistan — Femmes rurales (héritage foncier)",
            sub1=8.6,   # tribal jirga overrides statutory inheritance; women sign away shares
            sub2=8.4,   # Muslim inheritance law 50% share; custom further reduces to zero
            sub3=8.1,   # widows dependent on male kin; eviction on remarriage
            sub4=8.3,   # police refuse to register complaints; mediation coerced
        ),
        # 2 élevé
        EntityScore(
            entity_id="KEN_rural_women",
            name="Kenya — Femmes rurales (foncier & succession)",
            sub1=6.5,   # customary denial persists despite progressive constitution
            sub2=5.8,   # Succession Act gender-neutral but customary law still applied
            sub3=6.2,   # squatter settlements expose women to eviction
            sub4=5.5,   # some legal aid; FIDA Kenya active but under-resourced
        ),
        EntityScore(
            entity_id="GTM_indigenous_women",
            name="Guatemala — Femmes rurales indigènes (tierra)",
            sub1=6.3,   # Maya customary law excludes women from communal land
            sub2=6.0,   # Civil Code reformed but implementation weak
            sub3=6.5,   # palm oil/mining concessions displace indigenous women first
            sub4=6.1,   # indigenous women defenders face criminalization
        ),
        # 1 modéré
        EntityScore(
            entity_id="MEX_rural_women",
            name="Mexique — Femmes rurales (ejido & héritage)",
            sub1=3.9,   # ejido assembly membership historically male; reforms improving
            sub2=3.5,   # Agrarian Law amended; implementation uneven
            sub3=4.0,   # some eviction risk near extractive zones
            sub4=3.2,   # Tribunales Agrarios accessible; NGO support present
        ),
        # 1 faible
        EntityScore(
            entity_id="RWA_rural_women",
            name="Rwanda — Femmes rurales (loi foncière & succession)",
            sub1=1.9,   # Succession Law 2016 grants equal rights; largely applied
            sub2=1.5,   # progressive statutory framework with enforcement
            sub3=2.0,   # land registration program includes women; tenure improved
            sub4=1.8,   # Abunzi committees provide accessible local dispute resolution
        ),
    ]

    results = []
    total_composite = 0.0
    distribution = {"critique": 0, "élevé": 0, "modéré": 0, "faible": 0}

    for e in entities:
        total_composite += e.composite_score
        distribution[e.risk_level] += 1
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub_scores": {
                "customary_law_land_denial": e.sub1,
                "statutory_inheritance_discrimination": e.sub2,
                "tenure_security_eviction_risk": e.sub3,
                "legal_remedy_access_failure": e.sub4,
            },
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_rural_women_land_index": e.estimated_index,
        })

    avg_composite = round(total_composite / len(entities), 2)

    output = {
        "engine": "rural_women_land_inheritance_rights_engine",
        "wave": 144,
        "domain": "Rural Women Land & Inheritance Rights",
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
