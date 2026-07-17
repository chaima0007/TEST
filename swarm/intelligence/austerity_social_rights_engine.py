from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AusteritySocialRightsEntity:
    entity_id: str
    name: str
    country: str
    essential_services_dismantlement_score: float
    healthcare_education_access_collapse_score: float
    social_protection_withdrawal_score: float
    democratic_conditionality_breach_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_austerity_social_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.essential_services_dismantlement_score * 0.30
            + self.healthcare_education_access_collapse_score * 0.25
            + self.social_protection_withdrawal_score * 0.25
            + self.democratic_conditionality_breach_score * 0.20,
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
        self.estimated_austerity_social_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AusteritySocialRightsEngineResult:
    agent: str = "Austerity Social Rights Engine Agent"
    domain: str = "austerity_social_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_austerity_social_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AusteritySocialRightsEntity] = field(default_factory=list)

def run_austerity_social_rights_engine() -> AusteritySocialRightsEngineResult:
    entities = [
        AusteritySocialRightsEntity(
            entity_id="AU-001",
            name="Grèce — Mémorandum Troïka 2010-18, -30% Santé Publique, Pauvreté 36% & CESCR Violations",
            country="Europe du Sud",
            essential_services_dismantlement_score=95.0,
            healthcare_education_access_collapse_score=95.0,
            social_protection_withdrawal_score=92.0,
            democratic_conditionality_breach_score=90.0,
            primary_pattern="essential_services_dismantlement",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-002",
            name="UK — 12 Ans Austérité Cameron/Sunak, Banques Alimentaires ×10 & CRPD Violations Systémiques",
            country="Europe",
            essential_services_dismantlement_score=90.0,
            healthcare_education_access_collapse_score=88.0,
            social_protection_withdrawal_score=92.0,
            democratic_conditionality_breach_score=88.0,
            primary_pattern="social_protection_withdrawal",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-003",
            name="Argentine — FMI 57 Milliards 2018, Pauvreté 60%+ Milei 2024 & Démantèlement Social Accéléré",
            country="Amérique Latine",
            essential_services_dismantlement_score=88.0,
            healthcare_education_access_collapse_score=90.0,
            social_protection_withdrawal_score=88.0,
            democratic_conditionality_breach_score=88.0,
            primary_pattern="healthcare_education_access_collapse",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-004",
            name="Zambie — Restructuration Dette FMI 2022, Services Publics Effondrés & Conditionnalités Inhumaines",
            country="Afrique Australe",
            essential_services_dismantlement_score=85.0,
            healthcare_education_access_collapse_score=85.0,
            social_protection_withdrawal_score=85.0,
            democratic_conditionality_breach_score=85.0,
            primary_pattern="democratic_conditionality_breach",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-005",
            name="Brésil — PEC 55 Plafond Dépenses 20 Ans, -40% Investissement Social & Droits Gelés",
            country="Amérique Latine",
            essential_services_dismantlement_score=55.0,
            healthcare_education_access_collapse_score=52.0,
            social_protection_withdrawal_score=55.0,
            democratic_conditionality_breach_score=52.0,
            primary_pattern="social_protection_withdrawal",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-006",
            name="Portugal — Troïka 2011-14, Chômage 17%, Émigration 300K & Régression Droits Sociaux",
            country="Europe du Sud",
            essential_services_dismantlement_score=50.0,
            healthcare_education_access_collapse_score=50.0,
            social_protection_withdrawal_score=48.0,
            democratic_conditionality_breach_score=50.0,
            primary_pattern="essential_services_dismantlement",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-007",
            name="CETIM/ESCR-Net — Rapport Impact Austérité Droits Sociaux, Monitoring Conditionnalités FMI",
            country="Global",
            essential_services_dismantlement_score=22.0,
            healthcare_education_access_collapse_score=28.0,
            social_protection_withdrawal_score=25.0,
            democratic_conditionality_breach_score=30.0,
            primary_pattern="democratic_conditionality_breach",
        ),
        AusteritySocialRightsEntity(
            entity_id="AU-008",
            name="ONU/CESCR — Observation Générale 19 Sécurité Sociale, Obligation Non-Régression Droits PIDESC",
            country="Global",
            essential_services_dismantlement_score=4.0,
            healthcare_education_access_collapse_score=5.0,
            social_protection_withdrawal_score=3.0,
            democratic_conditionality_breach_score=6.0,
            primary_pattern="democratic_conditionality_breach",
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

    return AusteritySocialRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_austerity_social_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "imf_conditionality_social_impact_assessment_database",
            "un_cescr_austerity_measures_retrogression_reports",
            "oxfam_austerity_poverty_inequality_global_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_austerity_social_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_austerity_social_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
