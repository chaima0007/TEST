#!/usr/bin/env python3
"""
Wave 144 — Caste Discrimination & Dalit Rights Engine
Scores 8 country/community contexts on systematic caste-based discrimination,
untouchability enforcement, Dalit legal protections, and access to justice.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""
from dataclasses import dataclass, field
import json


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # untouchability_practice_severity (0-10)
    sub2: float  # legal_protection_enforcement (0-10, higher = worse enforcement)
    sub3: float  # economic_exclusion_bonded_labor (0-10)
    sub4: float  # access_to_justice_impunity (0-10)
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
            entity_id="IND_dalits",
            name="Inde — Dalits (Scheduled Castes)",
            sub1=8.8,   # untouchability widespread in rural areas despite legal ban
            sub2=8.2,   # SC/ST Act weakly enforced; low conviction rates
            sub3=8.5,   # manual scavenging, bonded labor, wage discrimination
            sub4=8.0,   # extreme impunity for caste violence, police complicity
        ),
        EntityScore(
            entity_id="NPL_dalits",
            name="Népal — Dalits",
            sub1=8.5,   # inter-caste marriage violence, untouchability in villages
            sub2=7.9,   # Caste-Based Discrimination Act rarely applied
            sub3=8.0,   # dalits excluded from land ownership, skilled trades
            sub4=7.8,   # perpetrators seldom prosecuted
        ),
        EntityScore(
            entity_id="PAK_scheduled",
            name="Pakistan — Scheduled Castes & Sweepers",
            sub1=8.3,   # hereditary occupational segregation entrenched
            sub2=8.6,   # no specific caste protection law; Hindu minority doubly marginalized
            sub3=8.7,   # sanitation work enforced by caste; extreme poverty
            sub4=8.1,   # near-total impunity; police extortion common
        ),
        EntityScore(
            entity_id="BGD_namashudra",
            name="Bangladesh — Namashudra & Dalit communities",
            sub1=7.9,   # social segregation, separate wells, temples
            sub2=8.0,   # caste discrimination not criminalized
            sub3=7.8,   # excluded from formal employment and land titling
            sub4=8.2,   # violence against lower-caste women rarely investigated
        ),
        # 2 élevé
        EntityScore(
            entity_id="LKA_rodiya",
            name="Sri Lanka — Rodiya & low-caste communities",
            sub1=5.2,   # diminishing but persistent social exclusion
            sub2=5.5,   # limited legal framework; implementation gaps
            sub3=5.0,   # wage discrimination in plantation sector
            sub4=4.8,   # some prosecutions but systemic impunity remains
        ),
        EntityScore(
            entity_id="JPN_burakumin",
            name="Japon — Burakumin",
            sub1=5.5,   # overt discrimination declining; digital hate speech rising
            sub2=5.8,   # no dedicated anti-discrimination law (Dowa policy lapsed)
            sub3=5.6,   # employment and marriage discrimination documented
            sub4=5.2,   # civil suits possible but costly; low take-up
        ),
        # 1 modéré
        EntityScore(
            entity_id="GBR_diaspora",
            name="Royaume-Uni — Diaspora sud-asiatique (discrimination de caste)",
            sub1=3.8,   # caste-based bias in UK Hindu/Sikh communities documented
            sub2=3.5,   # Equality Act 2010 s.9 caste provisions not commenced
            sub3=3.2,   # occupational stereotyping in domestic/care sector
            sub4=3.0,   # EHRC underfunded; few cases pursued
        ),
        # 1 faible
        EntityScore(
            entity_id="CAN_diaspora",
            name="Canada — Diaspora sud-asiatique (sensibilisation caste)",
            sub1=1.8,   # rare overt incidents; awareness campaigns active
            sub2=1.5,   # human rights codes cover caste under ancestry
            sub3=1.4,   # limited economic exclusion
            sub4=1.2,   # complaints mechanism accessible
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
                "untouchability_practice_severity": e.sub1,
                "legal_protection_enforcement_failure": e.sub2,
                "economic_exclusion_bonded_labor": e.sub3,
                "access_to_justice_impunity": e.sub4,
            },
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_caste_discrimination_index": e.estimated_index,
        })

    avg_composite = round(total_composite / len(entities), 2)

    output = {
        "engine": "caste_discrimination_dalit_rights_engine",
        "wave": 144,
        "domain": "Caste Discrimination & Dalit Rights",
        "avg_composite": avg_composite,
        "distribution": distribution,
        "entities": results,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
