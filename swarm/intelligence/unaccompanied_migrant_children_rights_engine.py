#!/usr/bin/env python3
"""
Unaccompanied Migrant Children Rights Engine — Caelum Partners Swarm Intelligence
Domaine : droits des enfants migrants non accompagnés, détention, protection, accès à la justice
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class UnaccompaniedMigrantChildrenEntity:
    entity_id: str
    name: str
    country: str
    detention_without_guardian_score: float
    legal_representation_denial_score: float
    deportation_without_protection_score: float
    child_trafficking_exposure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_unaccompanied_migrant_children_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.detention_without_guardian_score * 0.30
            + self.legal_representation_denial_score * 0.25
            + self.deportation_without_protection_score * 0.25
            + self.child_trafficking_exposure_score * 0.20,
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
        self.estimated_unaccompanied_migrant_children_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class UnaccompaniedMigrantChildrenEngineResult:
    agent: str = "Unaccompanied Migrant Children Rights Engine Agent"
    domain: str = "unaccompanied_migrant_children_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_unaccompanied_migrant_children_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[UnaccompaniedMigrantChildrenEntity] = field(default_factory=list)


def run_unaccompanied_migrant_children_rights_engine() -> UnaccompaniedMigrantChildrenEngineResult:
    entities = [
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-001",
            name="États-Unis — Séparation Familiale, Cages CBP, 85 000 Enfants Perdus dans le Système",
            country="États-Unis",
            detention_without_guardian_score=92.0,
            legal_representation_denial_score=88.0,
            deportation_without_protection_score=85.0,
            child_trafficking_exposure_score=90.0,
            primary_pattern="detention_without_guardian",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-002",
            name="Libye — Centres de Détention Esclavagistes, Mineurs Torturés & Vendus aux Trafiquants",
            country="Libye",
            detention_without_guardian_score=95.0,
            legal_representation_denial_score=93.0,
            deportation_without_protection_score=88.0,
            child_trafficking_exposure_score=95.0,
            primary_pattern="child_trafficking_exposure",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-003",
            name="Grèce/UE — Pushbacks Illégaux, Mineurs en Zone de Transit Sans Tuteur Légal",
            country="Grèce / Union Européenne",
            detention_without_guardian_score=82.0,
            legal_representation_denial_score=85.0,
            deportation_without_protection_score=88.0,
            child_trafficking_exposure_score=72.0,
            primary_pattern="deportation_without_protection",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-004",
            name="Mexique — Route Migratoire Dangereuse, Mineurs Honduriens/Guatémaltèques sans Protection",
            country="Mexique",
            detention_without_guardian_score=80.0,
            legal_representation_denial_score=78.0,
            deportation_without_protection_score=82.0,
            child_trafficking_exposure_score=85.0,
            primary_pattern="child_trafficking_exposure",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-005",
            name="Royaume-Uni — Hôtels Sans Surveillance, 400 Mineurs Disparus, Rwanda Plan Age Disputes",
            country="Royaume-Uni",
            detention_without_guardian_score=48.0,
            legal_representation_denial_score=52.0,
            deportation_without_protection_score=55.0,
            child_trafficking_exposure_score=45.0,
            primary_pattern="legal_representation_denial",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-006",
            name="Turquie — 3,6M Réfugiés Syriens, Enfants Non Accompagnés Sans Statut ni Scolarisation",
            country="Turquie",
            detention_without_guardian_score=52.0,
            legal_representation_denial_score=58.0,
            deportation_without_protection_score=60.0,
            child_trafficking_exposure_score=55.0,
            primary_pattern="legal_representation_denial",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-007",
            name="Italie — Réforme Cutro, Mineurs Eritréens/Afghans en Détention Administrative Illégale",
            country="Italie",
            detention_without_guardian_score=32.0,
            legal_representation_denial_score=38.0,
            deportation_without_protection_score=35.0,
            child_trafficking_exposure_score=28.0,
            primary_pattern="detention_without_guardian",
        ),
        UnaccompaniedMigrantChildrenEntity(
            entity_id="UMC-008",
            name="Canada — STCA Révisé, Tuteurs Désignés, Aide Juridique Gratuite Mineurs Migrants",
            country="Canada",
            detention_without_guardian_score=8.0,
            legal_representation_denial_score=6.0,
            deportation_without_protection_score=10.0,
            child_trafficking_exposure_score=12.0,
            primary_pattern="detention_without_guardian",
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

    return UnaccompaniedMigrantChildrenEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_unaccompanied_migrant_children_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_child_alert_unaccompanied_migrant_children_2025",
            "unhcr_global_trends_forced_displacement_2025",
            "save_the_children_no_safe_place_migration_report_2025",
            "human_rights_watch_children_immigration_detention_report_2025",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_unaccompanied_migrant_children_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_unaccompanied_migrant_children_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
