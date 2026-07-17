from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PeriodPovertyRightsEntity:
    entity_id: str
    name: str
    country: str
    menstrual_product_access_denial_severity_score: float
    school_absenteeism_dropout_menstrual_scale_score: float
    social_stigma_menstrual_taboo_pattern_score: float
    sanitation_hygiene_infrastructure_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_period_poverty_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.menstrual_product_access_denial_severity_score * 0.30
            + self.school_absenteeism_dropout_menstrual_scale_score * 0.25
            + self.social_stigma_menstrual_taboo_pattern_score * 0.25
            + self.sanitation_hygiene_infrastructure_gap_score * 0.20,
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
        self.estimated_period_poverty_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PeriodPovertyRightsEngineResult:
    agent: str = "Period Poverty Rights Engine Agent"
    domain: str = "period_poverty_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_period_poverty_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PeriodPovertyRightsEntity] = field(default_factory=list)

def run_period_poverty_rights_engine() -> PeriodPovertyRightsEngineResult:
    entities = [
        PeriodPovertyRightsEntity(
            entity_id="PPR-001",
            name="Népal/Inde Rurale — Chhaupadi (Exil Cabane), 70% Filles Sans Produits & Infections Fatales",
            country="Asie du Sud",
            menstrual_product_access_denial_severity_score=95.0,
            school_absenteeism_dropout_menstrual_scale_score=92.0,
            social_stigma_menstrual_taboo_pattern_score=95.0,
            sanitation_hygiene_infrastructure_gap_score=92.0,
            primary_pattern="social_stigma_menstrual_taboo_pattern",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-002",
            name="Afrique Sub-Sah. — 1/10 Filles Échange Sex Contre Produits, 50% Sans Toilettes École",
            country="Afrique",
            menstrual_product_access_denial_severity_score=92.0,
            school_absenteeism_dropout_menstrual_scale_score=95.0,
            social_stigma_menstrual_taboo_pattern_score=88.0,
            sanitation_hygiene_infrastructure_gap_score=92.0,
            primary_pattern="school_absenteeism_dropout_menstrual_scale",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-003",
            name="Bangladesh/Pakistan — 73% Filles Absentéisme, Chiffons Non Stériles & Zéro Programme Scolaire",
            country="Asie du Sud",
            menstrual_product_access_denial_severity_score=88.0,
            school_absenteeism_dropout_menstrual_scale_score=90.0,
            social_stigma_menstrual_taboo_pattern_score=88.0,
            sanitation_hygiene_infrastructure_gap_score=88.0,
            primary_pattern="menstrual_product_access_denial_severity",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-004",
            name="Afrique de l'Est/Kenya — Serviettes Luxe Inaccessibles, Tabou Rural & Filles Quittent École M3",
            country="Afrique de l'Est",
            menstrual_product_access_denial_severity_score=88.0,
            school_absenteeism_dropout_menstrual_scale_score=88.0,
            social_stigma_menstrual_taboo_pattern_score=85.0,
            sanitation_hygiene_infrastructure_gap_score=88.0,
            primary_pattern="sanitation_hygiene_infrastructure_gap",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-005",
            name="UK/USA — 1/10 Filles Sans Produits Menstruels Adéquats, Tax Tampon 2015 & Sans-Abri",
            country="Europe/Amérique du Nord",
            menstrual_product_access_denial_severity_score=52.0,
            school_absenteeism_dropout_menstrual_scale_score=52.0,
            social_stigma_menstrual_taboo_pattern_score=50.0,
            sanitation_hygiene_infrastructure_gap_score=55.0,
            primary_pattern="sanitation_hygiene_infrastructure_gap",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-006",
            name="France — 4M Femmes En Précarité Menstruelle, Étudiantes 49% Concernées & Honte Scolaire",
            country="Europe",
            menstrual_product_access_denial_severity_score=52.0,
            school_absenteeism_dropout_menstrual_scale_score=50.0,
            social_stigma_menstrual_taboo_pattern_score=52.0,
            sanitation_hygiene_infrastructure_gap_score=52.0,
            primary_pattern="menstrual_product_access_denial_severity",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-007",
            name="Plan International/Days for Girls — Kits Menstruels, Éducation MHM & Plaidoyer Taxe",
            country="Global",
            menstrual_product_access_denial_severity_score=22.0,
            school_absenteeism_dropout_menstrual_scale_score=28.0,
            social_stigma_menstrual_taboo_pattern_score=25.0,
            sanitation_hygiene_infrastructure_gap_score=30.0,
            primary_pattern="school_absenteeism_dropout_menstrual_scale",
        ),
        PeriodPovertyRightsEntity(
            entity_id="PPR-008",
            name="ONU/UNFPA — MHM Menstrual Hygiene Management, SDG 6 Eau/Assainissement & CEDAW",
            country="Global",
            menstrual_product_access_denial_severity_score=4.0,
            school_absenteeism_dropout_menstrual_scale_score=5.0,
            social_stigma_menstrual_taboo_pattern_score=3.0,
            sanitation_hygiene_infrastructure_gap_score=6.0,
            primary_pattern="social_stigma_menstrual_taboo_pattern",
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

    return PeriodPovertyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_period_poverty_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "plan_international_girls_report_menstrual_health_period_poverty_2023",
            "unfpa_menstrual_hygiene_management_sdg6_global_review",
            "wash_united_menstrual_health_school_absenteeism_global_study",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_period_poverty_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_period_poverty_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
