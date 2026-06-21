from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ElderlyRightsAgeDiscriminationEntity:
    entity_id: str
    name: str
    country: str
    elder_abuse_neglect_institutional_severity_score: float
    pension_social_security_denial_scale_score: float
    age_discrimination_employment_exclusion_score: float
    elderly_healthcare_access_dignity_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_elderly_rights_age_discrimination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.elder_abuse_neglect_institutional_severity_score * 0.30
            + self.pension_social_security_denial_scale_score * 0.25
            + self.age_discrimination_employment_exclusion_score * 0.25
            + self.elderly_healthcare_access_dignity_deficit_gap_score * 0.20,
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
        self.estimated_elderly_rights_age_discrimination_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ElderlyRightsAgeDiscriminationEngineResult:
    agent: str = "Elderly Rights Age Discrimination Engine Agent"
    domain: str = "elderly_rights_age_discrimination"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_elderly_rights_age_discrimination_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ElderlyRightsAgeDiscriminationEntity] = field(default_factory=list)


def run_elderly_rights_age_discrimination_engine() -> ElderlyRightsAgeDiscriminationEngineResult:
    entities = [
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-001",
            name="Chine/Maisons Retraite Abandons Covid Scandale — Aînés Isolés Morts Confinement, Familles Séparées & Maltraitance Institutionnelle Documentée",
            country="Chine",
            elder_abuse_neglect_institutional_severity_score=93.0,
            pension_social_security_denial_scale_score=88.0,
            age_discrimination_employment_exclusion_score=87.0,
            elderly_healthcare_access_dignity_deficit_gap_score=91.0,
            primary_pattern="elder_abuse_neglect_institutional_severity",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-002",
            name="Inde/Abandons Aînés Temples Vieillesse — 3.7M Personnes Âgées Sans Abri, Abandon Familial Structurel & Discrimination Caste-Âge Cumulée",
            country="Inde",
            elder_abuse_neglect_institutional_severity_score=90.0,
            pension_social_security_denial_scale_score=89.0,
            age_discrimination_employment_exclusion_score=85.0,
            elderly_healthcare_access_dignity_deficit_gap_score=88.0,
            primary_pattern="pension_social_security_denial_scale",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-003",
            name="Brésil/EHPAD Abus Maltraitance Pandémie — 36 000 Morts Résidences 2020, Surmortalité Aînés Pauvres & Négligence Institutionnelle Systémique",
            country="Brésil",
            elder_abuse_neglect_institutional_severity_score=88.0,
            pension_social_security_denial_scale_score=84.0,
            age_discrimination_employment_exclusion_score=83.0,
            elderly_healthcare_access_dignity_deficit_gap_score=86.0,
            primary_pattern="elder_abuse_neglect_institutional_severity",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-004",
            name="Russie/Retraites Gelées Inflation Pauvreté Aînés — Âge Retraite Relevé 2018, Pensions Insuffisantes & Discrimination Emploi 50+ Documentée",
            country="Russie",
            elder_abuse_neglect_institutional_severity_score=85.0,
            pension_social_security_denial_scale_score=87.0,
            age_discrimination_employment_exclusion_score=86.0,
            elderly_healthcare_access_dignity_deficit_gap_score=83.0,
            primary_pattern="age_discrimination_employment_exclusion",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-005",
            name="USA/Maisons Retraite Abus 1.5M Signalements/An — Under-Staffing Chronique, Abus Financiers Aînés & Discrimination Couleur dans EHPAD",
            country="USA",
            elder_abuse_neglect_institutional_severity_score=58.0,
            pension_social_security_denial_scale_score=54.0,
            age_discrimination_employment_exclusion_score=57.0,
            elderly_healthcare_access_dignity_deficit_gap_score=55.0,
            primary_pattern="elder_abuse_neglect_institutional_severity",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-006",
            name="Afrique Sub-Saharienne/Sorcellerie Accusations Aîné Exclusion — Aînés Accusés Sorcellerie, Lynchages, Expulsions & Violence Communautaire Ritualisée",
            country="Afrique Sub-Saharienne",
            elder_abuse_neglect_institutional_severity_score=55.0,
            pension_social_security_denial_scale_score=52.0,
            age_discrimination_employment_exclusion_score=50.0,
            elderly_healthcare_access_dignity_deficit_gap_score=58.0,
            primary_pattern="elderly_healthcare_access_dignity_deficit_gap",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-007",
            name="HelpAge/AARP Alliance Internationale Vieillissement — Plaidoyer Convention ONU Droits Aînés, Rapport Global AgeWatch & Indicateurs Inclusion",
            country="Global",
            elder_abuse_neglect_institutional_severity_score=28.0,
            pension_social_security_denial_scale_score=26.0,
            age_discrimination_employment_exclusion_score=27.0,
            elderly_healthcare_access_dignity_deficit_gap_score=25.0,
            primary_pattern="elder_abuse_neglect_institutional_severity",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="ERA-008",
            name="ONU/Plan Madrid 2002 Vieillissement & MIPAA — Cadre International Non-Discrimination Âge, Résolutions AG Personnes Âgées & SDG Inclusion",
            country="Global",
            elder_abuse_neglect_institutional_severity_score=6.0,
            pension_social_security_denial_scale_score=5.0,
            age_discrimination_employment_exclusion_score=5.0,
            elderly_healthcare_access_dignity_deficit_gap_score=6.0,
            primary_pattern="pension_social_security_denial_scale",
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

    return ElderlyRightsAgeDiscriminationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_elderly_rights_age_discrimination_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "helpage_global_agewatch_index_annual_report",
            "who_elder_abuse_global_status_report",
            "ilo_age_discrimination_employment_survey",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_elderly_rights_age_discrimination_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_elderly_rights_age_discrimination_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
