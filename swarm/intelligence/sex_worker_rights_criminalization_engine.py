#!/usr/bin/env python3
"""
Sex Worker Rights & Criminalization Engine — Caelum Partners Swarm Intelligence
Domaine : droits des travailleur·se·s du sexe, criminalisation, violence policière, stigmatisation juridique
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class SexWorkerRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_legal_persecution_score: float
    police_violence_impunity_score: float
    healthcare_service_denial_score: float
    trafficking_conflation_harm_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sex_worker_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_legal_persecution_score * 0.30
            + self.police_violence_impunity_score * 0.25
            + self.healthcare_service_denial_score * 0.25
            + self.trafficking_conflation_harm_score * 0.20,
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
        self.estimated_sex_worker_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SexWorkerRightsEngineResult:
    agent: str = "Sex Worker Rights & Criminalization Engine Agent"
    domain: str = "sex_worker_rights_criminalization"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_sex_worker_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexWorkerRightsEntity] = field(default_factory=list)


def run_sex_worker_rights_criminalization_engine() -> SexWorkerRightsEngineResult:
    entities = [
        SexWorkerRightsEntity(
            entity_id="SWR-001",
            name="Ouganda — Loi Anti-Homosexualité & Rafles, Travailleuses du Sexe Emprisonnées Sans Procès",
            country="Ouganda",
            criminalization_legal_persecution_score=95.0,
            police_violence_impunity_score=92.0,
            healthcare_service_denial_score=90.0,
            trafficking_conflation_harm_score=88.0,
            primary_pattern="criminalization_legal_persecution",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-002",
            name="Bangladesh — Quartiers Tolérés Illégaux, Rafles Policières, Violences & Aucun Recours Légal",
            country="Bangladesh",
            criminalization_legal_persecution_score=88.0,
            police_violence_impunity_score=90.0,
            healthcare_service_denial_score=85.0,
            trafficking_conflation_harm_score=82.0,
            primary_pattern="police_violence_impunity",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-003",
            name="Russie — Criminalisation Totale, Extorsion Policière Systématique, Zéro Protection VIH",
            country="Russie",
            criminalization_legal_persecution_score=85.0,
            police_violence_impunity_score=88.0,
            healthcare_service_denial_score=82.0,
            trafficking_conflation_harm_score=80.0,
            primary_pattern="police_violence_impunity",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-004",
            name="États-Unis/FOSTA-SESTA — Loi 2018, Plateformes Coupées, Travailleur·se·s Poussé·e·s Clandestinité",
            country="États-Unis",
            criminalization_legal_persecution_score=78.0,
            police_violence_impunity_score=75.0,
            healthcare_service_denial_score=72.0,
            trafficking_conflation_harm_score=85.0,
            primary_pattern="trafficking_conflation_harm",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-005",
            name="France — Modèle Nordique, Pénalisation Clients, Travailleuses Isolées & Hausse Violences",
            country="France",
            criminalization_legal_persecution_score=55.0,
            police_violence_impunity_score=48.0,
            healthcare_service_denial_score=42.0,
            trafficking_conflation_harm_score=58.0,
            primary_pattern="trafficking_conflation_harm",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-006",
            name="Suède — Modèle Originel, Travailleuses Marginalisées, Accès Réduit Services Santé",
            country="Suède",
            criminalization_legal_persecution_score=48.0,
            police_violence_impunity_score=40.0,
            healthcare_service_denial_score=45.0,
            trafficking_conflation_harm_score=52.0,
            primary_pattern="criminalization_legal_persecution",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-007",
            name="Allemagne — Prostituiertengesetz 2016, Enregistrement Obligatoire, Accès Santé Partiel",
            country="Allemagne",
            criminalization_legal_persecution_score=28.0,
            police_violence_impunity_score=25.0,
            healthcare_service_denial_score=22.0,
            trafficking_conflation_harm_score=30.0,
            primary_pattern="criminalization_legal_persecution",
        ),
        SexWorkerRightsEntity(
            entity_id="SWR-008",
            name="Nouvelle-Zélande — Decriminalisation 2003, Droit du Travail Applicable, Modèle Mondial",
            country="Nouvelle-Zélande",
            criminalization_legal_persecution_score=5.0,
            police_violence_impunity_score=8.0,
            healthcare_service_denial_score=6.0,
            trafficking_conflation_harm_score=10.0,
            primary_pattern="criminalization_legal_persecution",
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

    return SexWorkerRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sex_worker_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_network_sex_work_projects_sweat_annual_report_2025",
            "unaids_sex_workers_hiv_rights_global_assessment_2025",
            "human_rights_watch_swept_away_sex_workers_policing_report_2025",
            "amnesty_international_sex_workers_rights_decriminalization_policy_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_sex_worker_rights_criminalization_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sex_worker_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
