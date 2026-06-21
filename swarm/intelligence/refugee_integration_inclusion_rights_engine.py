from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RefugeeIntegrationInclusionRightsEntity:
    entity_id: str
    name: str
    country: str
    work_authorization_economic_exclusion_severity_score: float
    education_language_integration_barrier_scale_score: float
    housing_segregation_camp_confinement_score: float
    social_protection_civic_participation_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_refugee_integration_inclusion_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.work_authorization_economic_exclusion_severity_score * 0.30
            + self.education_language_integration_barrier_scale_score * 0.25
            + self.housing_segregation_camp_confinement_score * 0.25
            + self.social_protection_civic_participation_deficit_gap_score * 0.20,
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
        self.estimated_refugee_integration_inclusion_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RefugeeIntegrationInclusionRightsEngineResult:
    agent: str = "Refugee Integration Inclusion Rights Engine Agent"
    domain: str = "refugee_integration_inclusion_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_refugee_integration_inclusion_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RefugeeIntegrationInclusionRightsEntity] = field(default_factory=list)

def run_refugee_integration_inclusion_rights_engine() -> RefugeeIntegrationInclusionRightsEngineResult:
    entities = [
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-001",
            name="Liban/Syrie — 1.5M Réfugiés 25% Population, Interdits Travailler 70 Secteurs, Camps Informels & Inscriptions Scolaires Échouées",
            country="Liban",
            work_authorization_economic_exclusion_severity_score=95.0,
            education_language_integration_barrier_scale_score=93.0,
            housing_segregation_camp_confinement_score=92.0,
            social_protection_civic_participation_deficit_gap_score=94.0,
            primary_pattern="work_authorization_economic_exclusion_severity",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-002",
            name="Turquie/3.5M — 3.5M Syriens, Permis Travail 15%, Ghettos Urbains, Xénophobie Montante & Expulsions Forcées 2023",
            country="Turquie",
            work_authorization_economic_exclusion_severity_score=91.0,
            education_language_integration_barrier_scale_score=89.0,
            housing_segregation_camp_confinement_score=90.0,
            social_protection_civic_participation_deficit_gap_score=88.0,
            primary_pattern="housing_segregation_camp_confinement",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-003",
            name="Bangladesh/Rohingya — 1M Cox Bazar Camp, 12 Ans Confinement, Éducation Limitée Myanmar Curr. & Pas Droit Travail",
            country="Bangladesh",
            work_authorization_economic_exclusion_severity_score=87.0,
            education_language_integration_barrier_scale_score=86.0,
            housing_segregation_camp_confinement_score=85.0,
            social_protection_civic_participation_deficit_gap_score=88.0,
            primary_pattern="education_language_integration_barrier_scale",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-004",
            name="Australie/Offshore — Nauru/Manus Détention Indéfinie, Interdiction Installation Permanente, Santé Mentale Crise & Boats Turn-Back Policy",
            country="Australie",
            work_authorization_economic_exclusion_severity_score=83.0,
            education_language_integration_barrier_scale_score=82.0,
            housing_segregation_camp_confinement_score=84.0,
            social_protection_civic_participation_deficit_gap_score=81.0,
            primary_pattern="social_protection_civic_participation_deficit_gap",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-005",
            name="Europe/Dublin — Dublin III Réfugiés Renvoyés, Grèce Camps Surpeuplés, Intégration Inégale & Reconnaissance Diplômes Bloquée",
            country="Europe",
            work_authorization_economic_exclusion_severity_score=56.0,
            education_language_integration_barrier_scale_score=54.0,
            housing_segregation_camp_confinement_score=55.0,
            social_protection_civic_participation_deficit_gap_score=57.0,
            primary_pattern="work_authorization_economic_exclusion_severity",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-006",
            name="USA/TPS — Temporary Protected Status Expirations, Accès Services Limité, Éducation Enfants Non-Documentés & Intégration Discontinue",
            country="USA",
            work_authorization_economic_exclusion_severity_score=52.0,
            education_language_integration_barrier_scale_score=51.0,
            housing_segregation_camp_confinement_score=54.0,
            social_protection_civic_participation_deficit_gap_score=53.0,
            primary_pattern="social_protection_civic_participation_deficit_gap",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-007",
            name="UNHCR/IRC — Solutions Durables 3R, International Rescue Committee, IKEA Foundation Intégration & Mécanisme Réseau Support",
            country="Global",
            work_authorization_economic_exclusion_severity_score=27.0,
            education_language_integration_barrier_scale_score=25.0,
            housing_segregation_camp_confinement_score=28.0,
            social_protection_civic_participation_deficit_gap_score=26.0,
            primary_pattern="education_language_integration_barrier_scale",
        ),
        RefugeeIntegrationInclusionRightsEntity(
            entity_id="RIR-008",
            name="ONU/1951 Art.17-24 — Droits Économiques Réfugiés Conv. 1951, Art.22 Éducation, Art.21 Logement & SDG 10.7 Migration",
            country="Global",
            work_authorization_economic_exclusion_severity_score=4.0,
            education_language_integration_barrier_scale_score=4.0,
            housing_segregation_camp_confinement_score=4.0,
            social_protection_civic_participation_deficit_gap_score=4.0,
            primary_pattern="work_authorization_economic_exclusion_severity",
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

    return RefugeeIntegrationInclusionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_refugee_integration_inclusion_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_trends_refugee_integration_report",
            "international_rescue_committee_integration_report",
            "human_rights_watch_refugee_exclusion_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_refugee_integration_inclusion_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_refugee_integration_inclusion_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
