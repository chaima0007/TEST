from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class SexWorkRightsEntity:
    entity_id: str
    name: str
    country: str
    criminalization_rate_score: float
    violence_impunity_score: float
    legal_protection_absence_score: float
    stigma_discrimination_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_sex_work_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.criminalization_rate_score * 0.30
            + self.violence_impunity_score * 0.25
            + self.legal_protection_absence_score * 0.25
            + self.stigma_discrimination_score * 0.20,
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
        self.estimated_sex_work_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class SexWorkRightsEngineResult:
    agent: str = "Sex Work Rights Engine Agent"
    domain: str = "sex_work_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_sex_work_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SexWorkRightsEntity] = field(default_factory=list)

def run_sex_work_rights_engine() -> SexWorkRightsEngineResult:
    entities = [
        SexWorkRightsEntity(
            entity_id="SWR-001",
            name="Asie du Sud-Est/Cambodge — Raflades, Centres Détention & Criminalisation SESTA/FOSTA",
            country="Asie du Sud-Est",
            criminalization_rate_score=90.0,
            violence_impunity_score=88.0,
            legal_protection_absence_score=92.0,
            stigma_discrimination_score=85.0,
            primary_pattern="criminalization_rate",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-002",
            name="Afrique Sub-Saharienne — Kenya/Nigeria Sex Workers, Police Brutalité & VIH Non-Traité",
            country="Afrique Sub-Saharienne",
            criminalization_rate_score=85.0,
            violence_impunity_score=90.0,
            legal_protection_absence_score=88.0,
            stigma_discrimination_score=82.0,
            primary_pattern="violence_impunity",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-003",
            name="USA — SESTA/FOSTA, Criminalisation Numérique & Travailleuses du Sexe Déplacées",
            country="Amérique du Nord",
            criminalization_rate_score=72.0,
            violence_impunity_score=75.0,
            legal_protection_absence_score=80.0,
            stigma_discrimination_score=78.0,
            primary_pattern="legal_protection_absence",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-004",
            name="Russie/Europe Est — Persécution LGBT & Travailleuses Sexuelles, Extorsion Policière",
            country="Europe de l'Est",
            criminalization_rate_score=68.0,
            violence_impunity_score=72.0,
            legal_protection_absence_score=75.0,
            stigma_discrimination_score=82.0,
            primary_pattern="stigma_discrimination",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-005",
            name="Inde — Devadasi, Section 370 & Traite Sous Couvert Travail Sexuel",
            country="Asie du Sud",
            criminalization_rate_score=52.0,
            violence_impunity_score=58.0,
            legal_protection_absence_score=55.0,
            stigma_discrimination_score=60.0,
            primary_pattern="criminalization_rate",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-006",
            name="Chine — Rééducation Par le Travail, Raflades Régulières & Absence Droits Travail",
            country="Asie du Nord-Est",
            criminalization_rate_score=55.0,
            violence_impunity_score=50.0,
            legal_protection_absence_score=58.0,
            stigma_discrimination_score=52.0,
            primary_pattern="criminalization_rate",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-007",
            name="Nouvelle-Zélande/NZ — Modèle Décriminalisation, Lacunes & Limites Réplication Mondiale",
            country="Océanie",
            criminalization_rate_score=22.0,
            violence_impunity_score=28.0,
            legal_protection_absence_score=30.0,
            stigma_discrimination_score=32.0,
            primary_pattern="legal_protection_absence",
        ),
        SexWorkRightsEntity(
            entity_id="SWR-008",
            name="ONU/OMS/ONUSIDA — Recommandations Décriminalisation & Résistance États Membres",
            country="Global",
            criminalization_rate_score=4.0,
            violence_impunity_score=5.0,
            legal_protection_absence_score=3.0,
            stigma_discrimination_score=6.0,
            primary_pattern="violence_impunity",
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

    return SexWorkRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_sex_work_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unaids_sex_work_criminalization_health_impact_report",
            "global_network_sex_work_projects_gnswp_annual_advocacy_report",
            "human_rights_watch_swept_away_criminalization_sex_workers_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_sex_work_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_sex_work_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
