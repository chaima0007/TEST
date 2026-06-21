#!/usr/bin/env python3
"""
Wave 148 — Disability Rights & Inclusion Intelligence Engine
Caelum Partners Swarm Intelligence Platform

Assesses violations of CRPD (Convention on the Rights of Persons with Disabilities)
across legal protection gaps, accessibility deficits, exclusion from education/work,
and institutionalization risks.
Distribution: 4 critique / 2 élevé / 1 modéré / 1 faible
"""

from dataclasses import dataclass, field
import json
import statistics


@dataclass
class EntityScore:
    entity_id: str
    name: str
    sub1: float  # Legal protection gap — CRPD ratification & enforcement (0–10)
    sub2: float  # Accessibility deficit — built environment & digital (0–10)
    sub3: float  # Inclusion exclusion — education & employment (0–10)
    sub4: float  # Institutionalization risk — segregation & abuse (0–10)
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


def run_engine() -> dict:
    entities = [
        # 4 critique
        EntityScore(
            entity_id="AF-001",
            name="Afghanistan — Taliban Disability Rights Rollback",
            sub1=9.2,  # Taliban regime dissolved disability ministry; no CRPD enforcement
            sub2=8.8,  # physical infrastructure destroyed; wheelchairs & prosthetics scarce
            sub3=9.0,  # women with disabilities doubly excluded; no education access
            sub4=8.5,  # institutionalization normalized; family confinement widespread
        ),
        EntityScore(
            entity_id="YE-002",
            name="Yémen — Conflit & Handicap de Guerre",
            sub1=9.0,  # no functioning government to implement CRPD obligations
            sub2=9.2,  # 80% of healthcare infrastructure destroyed; no rehabilitation
            sub3=8.8,  # 500,000+ war-wounded with disabilities; 95% without support
            sub4=8.2,  # conflict creates disability; no institutional response
        ),
        EntityScore(
            entity_id="ET-003",
            name="Éthiopie — Déficit Structurel & Conflit Tigré",
            sub1=8.5,  # CRPD ratified but implementation near-zero; no disability law
            sub2=8.0,  # conflict destroyed rehabilitation centers in north
            sub3=8.2,  # persons with disabilities excluded from humanitarian response
            sub4=7.8,  # witchcraft stigma drives family confinement in rural areas
        ),
        EntityScore(
            entity_id="SD-004",
            name="Soudan — Guerre Civile & Populations Vulnérables",
            sub1=8.8,  # Sudan war 2023–: disability services nonexistent under RSF
            sub2=8.5,  # 10M+ displaced; persons with disabilities left behind
            sub3=8.6,  # no accessible evacuation; hospitals destroyed
            sub4=8.0,  # RSF documented torture of persons with disabilities in Khartoum
        ),
        # 2 élevé
        EntityScore(
            entity_id="MM-005",
            name="Myanmar — Coup & Disability Policy Collapse",
            sub1=6.0,  # junta suspended CRPD implementation committees
            sub2=5.5,  # urban accessibility minimal; rural near-absent
            sub3=5.8,  # 11M persons with disabilities; <5% have employment support
            sub4=5.2,  # psychiatric institutions report abuse; no oversight
        ),
        EntityScore(
            entity_id="IN-R-006",
            name="Inde Rurale — Lacunes RPWD & Exclusion",
            sub1=5.8,  # Rights of Persons with Disabilities Act 2016 unenforced rurally
            sub2=5.2,  # village-level accessibility nonexistent; 70M rural disabled
            sub3=5.5,  # education enrolment for children with disabilities <30% rural
            sub4=4.8,  # family confinement normalized; community care absent
        ),
        # 1 modéré
        EntityScore(
            entity_id="BR-007",
            name="Brésil — Progrès Législatif, Exclusion Persistante",
            sub1=3.5,  # Lei Brasileira de Inclusão 2015 enacted; enforcement patchy
            sub2=3.2,  # urban centers partially accessible; favelas and rural excluded
            sub3=3.0,  # 45M persons with disabilities; employment gap 40%+ persists
            sub4=2.8,  # psychiatric reform underway but institutions still operating
        ),
        # 1 faible
        EntityScore(
            entity_id="NL-008",
            name="Pays-Bas — Modèle CDPH avec Lacunes Résiduelles",
            sub1=1.5,  # CRPD ratified 2016; active Optional Protocol monitoring
            sub2=1.2,  # high accessibility standards; ISO/UN compliant infrastructure
            sub3=1.0,  # employment inclusion programs funded; quota enforcement
            sub4=1.3,  # deinstitutionalization progressing; community living supported
        ),
    ]

    results = []
    for e in entities:
        results.append({
            "entity_id": e.entity_id,
            "name": e.name,
            "sub1_legal_protection_gap": e.sub1,
            "sub2_accessibility_deficit": e.sub2,
            "sub3_inclusion_education_work": e.sub3,
            "sub4_institutionalization_risk": e.sub4,
            "composite_score": e.composite_score,
            "risk_level": e.risk_level,
            "estimated_disability_rights_inclusion_index": e.estimated_index,
        })

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    distribution = {
        "critique": sum(1 for e in entities if e.risk_level == "critique"),
        "élevé": sum(1 for e in entities if e.risk_level == "élevé"),
        "modéré": sum(1 for e in entities if e.risk_level == "modéré"),
        "faible": sum(1 for e in entities if e.risk_level == "faible"),
    }

    summary = {
        "engine": "disability_rights_inclusion_engine",
        "wave": 148,
        "total_entities": len(entities),
        "avg_composite": avg_composite,
        "distribution": distribution,
        "estimated_avg_index": round(avg_composite / 100 * 10, 2),
        "entities": results,
    }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    run_engine()
