from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PovertySocialExclusionRightsEntity:
    entity_id: str
    name: str
    country: str
    extreme_poverty_essential_services_denial_severity_score: float
    social_protection_floor_absence_scale_score: float
    homelessness_vagrancy_criminalization_score: float
    poverty_trap_structural_inequality_redress_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_poverty_social_exclusion_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.extreme_poverty_essential_services_denial_severity_score * 0.30
            + self.social_protection_floor_absence_scale_score * 0.25
            + self.homelessness_vagrancy_criminalization_score * 0.25
            + self.poverty_trap_structural_inequality_redress_deficit_gap_score * 0.20,
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
        self.estimated_poverty_social_exclusion_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PovertySocialExclusionRightsEngineResult:
    agent: str = "Poverty Social Exclusion Rights Engine Agent"
    domain: str = "poverty_social_exclusion_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_poverty_social_exclusion_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PovertySocialExclusionRightsEntity] = field(default_factory=list)


def run_poverty_social_exclusion_rights_engine() -> PovertySocialExclusionRightsEngineResult:
    entities = [
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-001",
            name="Madagascar/DRC — 77% Population Extrême Pauvreté <2$/Jour, Malnutrition Aiguë Enfants 50%, Santé Absente & Oxfam Alerte",
            country="Madagascar/DRC",
            extreme_poverty_essential_services_denial_severity_score=95.0,
            social_protection_floor_absence_scale_score=93.0,
            homelessness_vagrancy_criminalization_score=92.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=91.0,
            primary_pattern="extreme_poverty_essential_services_denial_severity",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-002",
            name="Sahel/Yémen — Famines Cycliques, 100M Déplacés Pauvres, Dettes FMI Austérité & Programmes Conditionnels Exclusifs",
            country="Sahel/Yémen",
            extreme_poverty_essential_services_denial_severity_score=92.0,
            social_protection_floor_absence_scale_score=90.0,
            homelessness_vagrancy_criminalization_score=89.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=88.0,
            primary_pattern="social_protection_floor_absence_scale",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-003",
            name="Inde/Bangladesh — Bidonvilles 100M Urbains, Dalits Sans Accès Services, Travail Bonded & Filets Protection Troués",
            country="Inde/Bangladesh",
            extreme_poverty_essential_services_denial_severity_score=89.0,
            social_protection_floor_absence_scale_score=87.0,
            homelessness_vagrancy_criminalization_score=86.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=85.0,
            primary_pattern="poverty_trap_structural_inequality_redress_deficit_gap",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-004",
            name="Amérique Centrale — Pauvreté Migration Forcée, Gangs Contrôle Quartiers Pauvres, Remesas Unique Revenu & Inégalités Record",
            country="Amérique Centrale",
            extreme_poverty_essential_services_denial_severity_score=86.0,
            social_protection_floor_absence_scale_score=84.0,
            homelessness_vagrancy_criminalization_score=83.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=82.0,
            primary_pattern="poverty_trap_structural_inequality_redress_deficit_gap",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-005",
            name="USA/UK — Working Poor 40M USA, Foodbanks Record UK Austérité, Evictions COVID & Sans-Abri Criminalisés",
            country="USA/UK",
            extreme_poverty_essential_services_denial_severity_score=57.0,
            social_protection_floor_absence_scale_score=55.0,
            homelessness_vagrancy_criminalization_score=54.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=53.0,
            primary_pattern="homelessness_vagrancy_criminalization",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-006",
            name="Europe/OCDE — NEET Youth 12%, Pièges Pauvreté Bénéficiaires, Logement Social Listes Attente & Fracture Numérique",
            country="Europe/OCDE",
            extreme_poverty_essential_services_denial_severity_score=54.0,
            social_protection_floor_absence_scale_score=52.0,
            homelessness_vagrancy_criminalization_score=51.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=50.0,
            primary_pattern="social_protection_floor_absence_scale",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-007",
            name="Oxfam/BRAC — Rapports Inégalités Mondiales, Programmes Sortie Pauvreté, Advocacy Filets Sociaux & SDG Monitoring",
            country="Global",
            extreme_poverty_essential_services_denial_severity_score=27.0,
            social_protection_floor_absence_scale_score=26.0,
            homelessness_vagrancy_criminalization_score=25.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=25.0,
            primary_pattern="extreme_poverty_essential_services_denial_severity",
        ),
        PovertySocialExclusionRightsEntity(
            entity_id="PSE-008",
            name="ONU/Art.11 DESC — Droit Niveau Vie Suffisant, Rapporteur Extrême Pauvreté & SDG 1 Pas de Pauvreté",
            country="Global",
            extreme_poverty_essential_services_denial_severity_score=5.0,
            social_protection_floor_absence_scale_score=4.0,
            homelessness_vagrancy_criminalization_score=4.0,
            poverty_trap_structural_inequality_redress_deficit_gap_score=4.0,
            primary_pattern="extreme_poverty_essential_services_denial_severity",
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

    return PovertySocialExclusionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_poverty_social_exclusion_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "world_bank_poverty_global_database",
            "oxfam_inequality_kills_annual_report",
            "ilo_social_protection_floor_global_assessment",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_poverty_social_exclusion_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_poverty_social_exclusion_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
