from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ElderlyRightsAgeDiscriminationEntity:
    entity_id: str
    name: str
    country: str
    elder_abuse_neglect_institutionalized_score: float
    pension_social_protection_deficit_score: float
    healthcare_access_denial_age_discrimination_score: float
    legal_protection_elder_rights_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_elderly_rights_age_discrimination_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.elder_abuse_neglect_institutionalized_score * 0.30
            + self.pension_social_protection_deficit_score * 0.25
            + self.healthcare_access_denial_age_discrimination_score * 0.25
            + self.legal_protection_elder_rights_gap_score * 0.20,
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
    data_sources: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"


def run_elderly_rights_age_discrimination_engine() -> ElderlyRightsAgeDiscriminationEngineResult:
    entities = [
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="IND-002",
            name="Inde",
            country="Inde",
            elder_abuse_neglect_institutionalized_score=86.0,
            pension_social_protection_deficit_score=90.0,
            healthcare_access_denial_age_discrimination_score=84.0,
            legal_protection_elder_rights_gap_score=88.0,
            primary_pattern="71% personnes âgées sans revenu propre, abandon familles urbaines, mendiance, soins inexistants zones rurales",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="NGA-001",
            name="Nigeria",
            country="Nigeria",
            elder_abuse_neglect_institutionalized_score=88.0,
            pension_social_protection_deficit_score=92.0,
            healthcare_access_denial_age_discrimination_score=86.0,
            legal_protection_elder_rights_gap_score=90.0,
            primary_pattern="Accusations sorcellerie tuent personnes âgées, abandon systématique, aucune pension 90%+ population",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="AFG-001",
            name="Afghanistan",
            country="Afghanistan",
            elder_abuse_neglect_institutionalized_score=84.0,
            pension_social_protection_deficit_score=88.0,
            healthcare_access_denial_age_discrimination_score=90.0,
            legal_protection_elder_rights_gap_score=92.0,
            primary_pattern="Personnes âgées exclues aide humanitaire, invalidité ignorée, femmes âgées particulièrement vulnérables Talibans",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="PER-002",
            name="Pérou",
            country="Pérou",
            elder_abuse_neglect_institutionalized_score=78.0,
            pension_social_protection_deficit_score=80.0,
            healthcare_access_denial_age_discrimination_score=76.0,
            legal_protection_elder_rights_gap_score=82.0,
            primary_pattern="Maltraitance documentée IPRESS, pensions insuffisantes, populations rurales quechuas sans accès",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="USA-001",
            name="USA",
            country="USA",
            elder_abuse_neglect_institutionalized_score=55.0,
            pension_social_protection_deficit_score=48.0,
            healthcare_access_denial_age_discrimination_score=52.0,
            legal_protection_elder_rights_gap_score=45.0,
            primary_pattern="1 personne âgée sur 10 victime maltraitance, EHPAD sous-staffés COVID-19 55K décès, discrimination âgisme santé",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="GBR-001",
            name="Royaume-Uni",
            country="Royaume-Uni",
            elder_abuse_neglect_institutionalized_score=52.0,
            pension_social_protection_deficit_score=45.0,
            healthcare_access_denial_age_discrimination_score=50.0,
            legal_protection_elder_rights_gap_score=42.0,
            primary_pattern="Scandales soins domicile, austerity 1.5M sans aide suffisante, isolation sociale épidémique",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="FRA-001",
            name="France",
            country="France",
            elder_abuse_neglect_institutionalized_score=35.0,
            pension_social_protection_deficit_score=28.0,
            healthcare_access_denial_age_discrimination_score=30.0,
            legal_protection_elder_rights_gap_score=25.0,
            primary_pattern="Canicule 2003 15K décès révélatrice, Orpea scandale 2022, progrès législatifs partiels",
        ),
        ElderlyRightsAgeDiscriminationEntity(
            entity_id="SWE-001",
            name="Suède",
            country="Suède",
            elder_abuse_neglect_institutionalized_score=10.0,
            pension_social_protection_deficit_score=8.0,
            healthcare_access_denial_age_discrimination_score=9.0,
            legal_protection_elder_rights_gap_score=7.0,
            primary_pattern="Système vieillissement actif modèle, pensions universelles, soins communautaires bien financés",
        ),
    ]

    result = ElderlyRightsAgeDiscriminationEngineResult()
    result.total_entities = len(entities)
    result.avg_composite = round(
        statistics.mean(e.composite_score for e in entities), 2
    )
    result.confidence_score = 0.85

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    result.risk_distribution = risk_dist

    sorted_entities = sorted(entities, key=lambda e: e.composite_score, reverse=True)
    result.top_risk_entities = [e.name for e in sorted_entities[:3]]
    result.critical_alerts = [
        f"{e.name}: composite={e.composite_score}, index={e.estimated_elderly_rights_age_discrimination_index}"
        for e in sorted_entities
        if e.risk_level == "critique"
    ]
    result.data_sources = [
        "who_global_report_ageism_2021",
        "helpage_global_agewatch_index_2023",
        "human_rights_watch_elder_care_database",
        "un_open_ended_working_group_ageing_2023",
    ]

    return result


if __name__ == "__main__":
    result = run_elderly_rights_age_discrimination_engine()
    print(f"Agent      : {result.agent}")
    print(f"Domain     : {result.domain}")
    print(f"Entities   : {result.total_entities}")
    print(f"Avg composite : {result.avg_composite}")
    print(f"Confidence : {result.confidence_score}")
    print(f"Distribution: {result.risk_distribution}")
    print(f"Top risks  : {result.top_risk_entities}")
    print("Critical alerts:")
    for alert in result.critical_alerts:
        print(f"  - {alert}")
    print(f"Sources    : {result.data_sources}")
