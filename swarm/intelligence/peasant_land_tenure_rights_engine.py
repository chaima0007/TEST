#!/usr/bin/env python3
"""
Peasant Land Tenure Rights Engine — Caelum Partners Swarm Intelligence
Domaine : sécurité foncière paysanne, droits de tenure, accaparement des terres, réforme agraire
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class PeasantLandTenureEntity:
    entity_id: str
    name: str
    country: str
    land_tenure_insecurity_score: float
    eviction_without_compensation_score: float
    agrarian_reform_obstruction_score: float
    corporate_land_grabbing_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_peasant_land_tenure_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.land_tenure_insecurity_score * 0.30
            + self.eviction_without_compensation_score * 0.25
            + self.agrarian_reform_obstruction_score * 0.25
            + self.corporate_land_grabbing_score * 0.20,
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
        self.estimated_peasant_land_tenure_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class PeasantLandTenureEngineResult:
    agent: str = "Peasant Land Tenure Rights Engine Agent"
    domain: str = "peasant_land_tenure_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_peasant_land_tenure_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PeasantLandTenureEntity] = field(default_factory=list)


def run_peasant_land_tenure_rights_engine() -> PeasantLandTenureEngineResult:
    entities = [
        PeasantLandTenureEntity(
            entity_id="PLT-001",
            name="Éthiopie — Terres Étatiques, Expulsions Massives Rift Valley & Investisseurs Étrangers",
            country="Éthiopie",
            land_tenure_insecurity_score=92.0,
            eviction_without_compensation_score=90.0,
            agrarian_reform_obstruction_score=88.0,
            corporate_land_grabbing_score=92.0,
            primary_pattern="land_tenure_insecurity",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-002",
            name="Cambodge — Concessions Économiques, 500 000 Paysans Expulsés, Loi Foncière Contournée",
            country="Cambodge",
            land_tenure_insecurity_score=90.0,
            eviction_without_compensation_score=92.0,
            agrarian_reform_obstruction_score=85.0,
            corporate_land_grabbing_score=88.0,
            primary_pattern="eviction_without_compensation",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-003",
            name="Soudan du Sud — Conflits Fonciers Ethniques, Terres Coutumières Non Reconnues, Milices Agraires",
            country="Soudan du Sud",
            land_tenure_insecurity_score=88.0,
            eviction_without_compensation_score=85.0,
            agrarian_reform_obstruction_score=90.0,
            corporate_land_grabbing_score=80.0,
            primary_pattern="agrarian_reform_obstruction",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-004",
            name="Philippines — Réforme Agraire Sabotée, Hacienda Luisita, Paysans Assassinés Mindanao",
            country="Philippines",
            land_tenure_insecurity_score=78.0,
            eviction_without_compensation_score=80.0,
            agrarian_reform_obstruction_score=85.0,
            corporate_land_grabbing_score=75.0,
            primary_pattern="agrarian_reform_obstruction",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-005",
            name="Bangladesh — Chars Fluviaux, Terres Inondées Sans Titre, Paysans Déplacés par Crues",
            country="Bangladesh",
            land_tenure_insecurity_score=55.0,
            eviction_without_compensation_score=58.0,
            agrarian_reform_obstruction_score=50.0,
            corporate_land_grabbing_score=48.0,
            primary_pattern="land_tenure_insecurity",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-006",
            name="Colombie — Accords de Paix, Restitution des Terres Inachevée, Menaces contre Paysans",
            country="Colombie",
            land_tenure_insecurity_score=52.0,
            eviction_without_compensation_score=55.0,
            agrarian_reform_obstruction_score=58.0,
            corporate_land_grabbing_score=50.0,
            primary_pattern="agrarian_reform_obstruction",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-007",
            name="Bolivie — Réforme Agraire Incomplète, Droits Communaux Reconnus mais Cadastre Lacunaire",
            country="Bolivie",
            land_tenure_insecurity_score=30.0,
            eviction_without_compensation_score=28.0,
            agrarian_reform_obstruction_score=25.0,
            corporate_land_grabbing_score=32.0,
            primary_pattern="land_tenure_insecurity",
        ),
        PeasantLandTenureEntity(
            entity_id="PLT-008",
            name="Pays-Bas — Cadastre Complet, Bail Rural Protégé, Droits Fermiers Garantis par Loi",
            country="Pays-Bas",
            land_tenure_insecurity_score=6.0,
            eviction_without_compensation_score=5.0,
            agrarian_reform_obstruction_score=8.0,
            corporate_land_grabbing_score=10.0,
            primary_pattern="corporate_land_grabbing",
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

    return PeasantLandTenureEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_peasant_land_tenure_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "grain_org_land_grabbing_database_2025",
            "international_land_coalition_land_matrix_global_report_2025",
            "fao_voluntary_guidelines_responsible_governance_tenure_implementation_review",
            "oxfam_righting_the_land_rights_gap_report_2025",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_peasant_land_tenure_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_peasant_land_tenure_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
