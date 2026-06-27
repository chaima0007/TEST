from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ElderCareAgingRightsEntity:
    entity_id: str
    name: str
    country: str
    elder_abuse_neglect_institutionalization_severity_score: float
    pension_social_protection_exclusion_scale_score: float
    ageism_employment_healthcare_discrimination_score: float
    dementia_care_autonomy_rights_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_elder_care_aging_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.elder_abuse_neglect_institutionalization_severity_score * 0.30
            + self.pension_social_protection_exclusion_scale_score * 0.25
            + self.ageism_employment_healthcare_discrimination_score * 0.25
            + self.dementia_care_autonomy_rights_deficit_gap_score * 0.20,
            2,
        )
        if self.composite_score >= 60:
            self.risk_level = "critique"
        elif self.composite_score >= 40:
            self.risk_level = "élevé"
        elif self.composite_score >= 20:
            self.risk_level = "modéré"
        else:
            self.risk_level = "faible"
        self.estimated_elder_care_aging_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ElderCareAgingRightsEngineResult:
    agent: str = "Elder Care Aging Rights Engine Agent"
    domain: str = "elder_care_aging_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_elder_care_aging_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ElderCareAgingRightsEntity] = field(default_factory=list)


def run_elder_care_aging_rights_engine() -> ElderCareAgingRightsEngineResult:
    entities = [
        ElderCareAgingRightsEntity(
            entity_id="ECA-001",
            name="Inde/Asie Sud — 3/4 Ainés Sans Pension, Familles Abandon Rural, Brus Vieillissants Apatrides & Maltraitance Invisible",
            country="Inde/Asie Sud",
            elder_abuse_neglect_institutionalization_severity_score=95.0,
            pension_social_protection_exclusion_scale_score=93.0,
            ageism_employment_healthcare_discrimination_score=93.0,
            dementia_care_autonomy_rights_deficit_gap_score=91.0,
            primary_pattern="pension_social_protection_exclusion_scale",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-002",
            name="Afrique Sub-Saharienne — HIV/AIDS Orphelins Parents Ainés, Pensions Absentes 90%, Sorcellerie Âgées Accusées & Déplacement",
            country="Afrique Sub-Saharienne",
            elder_abuse_neglect_institutionalization_severity_score=92.0,
            pension_social_protection_exclusion_scale_score=90.0,
            ageism_employment_healthcare_discrimination_score=90.0,
            dementia_care_autonomy_rights_deficit_gap_score=88.0,
            primary_pattern="pension_social_protection_exclusion_scale",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-003",
            name="USA/Europe COVID — EHPAD COVID 40% Morts, Directives Ne-Pas-Réanimer Âge, Isolement Forcé & Vaccination Retard Ainés",
            country="USA/Europe",
            elder_abuse_neglect_institutionalization_severity_score=89.0,
            pension_social_protection_exclusion_scale_score=87.0,
            ageism_employment_healthcare_discrimination_score=87.0,
            dementia_care_autonomy_rights_deficit_gap_score=85.0,
            primary_pattern="elder_abuse_neglect_institutionalization_severity",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-004",
            name="Chine/Japon — Vieillissement Démographique Crise, Traités Confucéens vs Institutions, Kodawari Abandon Urbain & Maltraitance EHPAD",
            country="Chine/Japon",
            elder_abuse_neglect_institutionalization_severity_score=86.0,
            pension_social_protection_exclusion_scale_score=84.0,
            ageism_employment_healthcare_discrimination_score=84.0,
            dementia_care_autonomy_rights_deficit_gap_score=82.0,
            primary_pattern="dementia_care_autonomy_rights_deficit_gap",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-005",
            name="France/UK — EHPAD Orpea Scandale Maltraitance, Personal Budgets Coupés, Restraint Chimique & Capacité Juridique Tutelle",
            country="France/UK",
            elder_abuse_neglect_institutionalization_severity_score=57.0,
            pension_social_protection_exclusion_scale_score=55.0,
            ageism_employment_healthcare_discrimination_score=55.0,
            dementia_care_autonomy_rights_deficit_gap_score=53.0,
            primary_pattern="elder_abuse_neglect_institutionalization_severity",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-006",
            name="Amérique Latine — Retraites Dollarisées Perdues, Violence Intra-Familiale Âgés, Systèmes Santé Sans Gériatrie & Abandon",
            country="Amérique Latine",
            elder_abuse_neglect_institutionalization_severity_score=54.0,
            pension_social_protection_exclusion_scale_score=52.0,
            ageism_employment_healthcare_discrimination_score=52.0,
            dementia_care_autonomy_rights_deficit_gap_score=50.0,
            primary_pattern="pension_social_protection_exclusion_scale",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-007",
            name="HelpAge International/AARP — Advocacy Droits Personnes Âgées, Monitoring Maltraitance, Convention Proposée ONU & Standards",
            country="Global",
            elder_abuse_neglect_institutionalization_severity_score=27.0,
            pension_social_protection_exclusion_scale_score=26.0,
            ageism_employment_healthcare_discrimination_score=26.0,
            dementia_care_autonomy_rights_deficit_gap_score=25.0,
            primary_pattern="ageism_employment_healthcare_discrimination",
        ),
        ElderCareAgingRightsEntity(
            entity_id="ECA-008",
            name="ONU/MIPAA — Plan International Madrid Vieillissement, Décennie Vieillissement Sain 2021-2030 & SDG 3 Santé",
            country="Global",
            elder_abuse_neglect_institutionalization_severity_score=5.0,
            pension_social_protection_exclusion_scale_score=4.0,
            ageism_employment_healthcare_discrimination_score=4.0,
            dementia_care_autonomy_rights_deficit_gap_score=4.0,
            primary_pattern="dementia_care_autonomy_rights_deficit_gap",
        ),
    ]

    composites = [e.composite_score for e in entities]
    avg_composite = round(statistics.mean(composites), 2)

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1

    pattern_dist: dict = {}
    for e in entities:
        pattern_dist[e.primary_pattern] = pattern_dist.get(e.primary_pattern, 0) + 1

    sorted_entities = sorted(entities, key=lambda x: x.composite_score, reverse=True)
    top_risk = [e.name for e in sorted_entities[:3]]
    alerts = [
        f"{e.name.split('—')[0].strip()}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return ElderCareAgingRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_elder_care_aging_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_global_status_report_elder_abuse",
            "helpage_international_aging_rights_index",
            "ilo_pension_social_protection_elderly_coverage",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_elder_care_aging_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_elder_care_aging_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
