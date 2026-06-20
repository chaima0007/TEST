from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonOvercrowdingEntity:
    entity_id: str
    name: str
    country: str
    occupancy_rate_excess_score: float
    health_sanitation_failure_score: float
    violence_inmate_death_score: float
    reform_political_will_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_overcrowding_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.occupancy_rate_excess_score * 0.30
            + self.health_sanitation_failure_score * 0.25
            + self.violence_inmate_death_score * 0.25
            + self.reform_political_will_gap_score * 0.20,
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
        self.estimated_prison_overcrowding_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonOvercrowdingEngineResult:
    agent: str = "Prison Overcrowding Engine Agent"
    domain: str = "prison_overcrowding"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_prison_overcrowding_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonOvercrowdingEntity] = field(default_factory=list)

def run_prison_overcrowding_engine() -> PrisonOvercrowdingEngineResult:
    entities = [
        PrisonOvercrowdingEntity(
            entity_id="PO-001",
            name="El Salvador — CECOT 800% Capacité, Gangs/MS13 Détenus en Masse & Droits Suspendus",
            country="Amérique Centrale",
            occupancy_rate_excess_score=95.0,
            health_sanitation_failure_score=90.0,
            violence_inmate_death_score=88.0,
            reform_political_will_gap_score=85.0,
            primary_pattern="occupancy_rate_excess",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-002",
            name="Philippines — BJMP 500% Capacité, Morts Liées à la Chaleur & Torture Banalisée",
            country="Asie du Sud-Est",
            occupancy_rate_excess_score=88.0,
            health_sanitation_failure_score=85.0,
            violence_inmate_death_score=88.0,
            reform_political_will_gap_score=82.0,
            primary_pattern="violence_inmate_death",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-003",
            name="Venezuela — Prisons DGCIM/Tocuyito, Bandas Armées Contrôlent Cellules & Épidémies",
            country="Amérique Latine",
            occupancy_rate_excess_score=85.0,
            health_sanitation_failure_score=88.0,
            violence_inmate_death_score=85.0,
            reform_political_will_gap_score=80.0,
            primary_pattern="health_sanitation_failure",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-004",
            name="Haïti — Pénitencier National Port-au-Prince, 4000% Capacité & Gangs Infiltrés",
            country="Caraïbes",
            occupancy_rate_excess_score=80.0,
            health_sanitation_failure_score=85.0,
            violence_inmate_death_score=82.0,
            reform_political_will_gap_score=78.0,
            primary_pattern="health_sanitation_failure",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-005",
            name="Thaïlande — 300% Capacité, Prisonniers Drogues Surreprésentés & Réforme Lente",
            country="Asie du Sud-Est",
            occupancy_rate_excess_score=52.0,
            health_sanitation_failure_score=55.0,
            violence_inmate_death_score=58.0,
            reform_political_will_gap_score=50.0,
            primary_pattern="reform_political_will_gap",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-006",
            name="Mexique — Prisons Fédérales Surpeuplées, Cartels & Corruption Pénitentiaire Systémique",
            country="Amérique du Nord",
            occupancy_rate_excess_score=48.0,
            health_sanitation_failure_score=52.0,
            violence_inmate_death_score=55.0,
            reform_political_will_gap_score=50.0,
            primary_pattern="reform_political_will_gap",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-007",
            name="UE/Pays-Bas — Fermeture Prisons, Alternatives Détention & Population Carcérale en Baisse",
            country="Europe",
            occupancy_rate_excess_score=22.0,
            health_sanitation_failure_score=28.0,
            violence_inmate_death_score=30.0,
            reform_political_will_gap_score=25.0,
            primary_pattern="occupancy_rate_excess",
        ),
        PrisonOvercrowdingEntity(
            entity_id="PO-008",
            name="ONU/ONUDC — Règles Mandela, Standards Minima Traitement Détenus & Monitoring Global",
            country="Global",
            occupancy_rate_excess_score=4.0,
            health_sanitation_failure_score=5.0,
            violence_inmate_death_score=3.0,
            reform_political_will_gap_score=6.0,
            primary_pattern="violence_inmate_death",
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

    return PrisonOvercrowdingEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_overcrowding_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "world_prison_brief_icps_global_prison_population_database",
            "penal_reform_international_global_prison_trends_annual_report",
            "un_special_rapporteur_torture_places_of_deprivation_liberty_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_overcrowding_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_overcrowding_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
