from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateJusticeEnvironmentalDefendersEntity:
    entity_id: str
    name: str
    country: str
    environmental_defender_killing_criminalization_severity_score: float
    climate_loss_damage_vulnerable_population_scale_score: float
    fossil_fuel_corporate_impunity_score: float
    climate_litigation_access_justice_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_justice_environmental_defenders_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.environmental_defender_killing_criminalization_severity_score * 0.30
            + self.climate_loss_damage_vulnerable_population_scale_score * 0.25
            + self.fossil_fuel_corporate_impunity_score * 0.25
            + self.climate_litigation_access_justice_deficit_gap_score * 0.20,
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
        self.estimated_climate_justice_environmental_defenders_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ClimateJusticeEnvironmentalDefendersEngineResult:
    agent: str = "Climate Justice Environmental Defenders Engine Agent"
    domain: str = "climate_justice_environmental_defenders"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_justice_environmental_defenders_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateJusticeEnvironmentalDefendersEntity] = field(default_factory=list)


def run_climate_justice_environmental_defenders_engine() -> ClimateJusticeEnvironmentalDefendersEngineResult:
    entities = [
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-001",
            name="Philippines/Honduras — Berta Cáceres Assassinée, Île Nations Submersion, Défenseurs Environnement #1 Tués Monde & Impunité Totale",
            country="Philippines/Honduras",
            environmental_defender_killing_criminalization_severity_score=93.0,
            climate_loss_damage_vulnerable_population_scale_score=91.0,
            fossil_fuel_corporate_impunity_score=90.0,
            climate_litigation_access_justice_deficit_gap_score=92.0,
            primary_pattern="environmental_defender_killing_criminalization_severity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-002",
            name="Amazonie Brésil — 300+ Défenseurs Tués Bolsonaro Era, Terres Indigènes Déforestées, Garimpeiros Violents & Lula Réforme Lente",
            country="Brésil",
            environmental_defender_killing_criminalization_severity_score=90.0,
            climate_loss_damage_vulnerable_population_scale_score=88.0,
            fossil_fuel_corporate_impunity_score=89.0,
            climate_litigation_access_justice_deficit_gap_score=91.0,
            primary_pattern="environmental_defender_killing_criminalization_severity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-003",
            name="Pakistan/Bangladesh — Inondations Catastrophiques 33M Déplacés, Pertes Économiques Irréparables, Emprunt FMI Climate & Pollueurs Non Responsables",
            country="Pakistan/Bangladesh",
            environmental_defender_killing_criminalization_severity_score=87.0,
            climate_loss_damage_vulnerable_population_scale_score=85.0,
            fossil_fuel_corporate_impunity_score=86.0,
            climate_litigation_access_justice_deficit_gap_score=88.0,
            primary_pattern="climate_loss_damage_vulnerable_population_scale",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-004",
            name="Afrique Subsaharienne — Sécheresse Corne Afrique 36M, Lac Tchad Disparu 90%, Cyclones Mozambique & Multinationales Extractives Immunisées",
            country="Afrique Subsaharienne",
            environmental_defender_killing_criminalization_severity_score=84.0,
            climate_loss_damage_vulnerable_population_scale_score=82.0,
            fossil_fuel_corporate_impunity_score=83.0,
            climate_litigation_access_justice_deficit_gap_score=85.0,
            primary_pattern="fossil_fuel_corporate_impunity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-005",
            name="Indonésie/PNG — Déforestation Palmier Huile, Communautés Indigènes Expulsées, Forêts Tourbe Brûlées & Licences Sans FPIC",
            country="Indonésie/PNG",
            environmental_defender_killing_criminalization_severity_score=55.0,
            climate_loss_damage_vulnerable_population_scale_score=53.0,
            fossil_fuel_corporate_impunity_score=54.0,
            climate_litigation_access_justice_deficit_gap_score=56.0,
            primary_pattern="environmental_defender_killing_criminalization_severity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-006",
            name="USA/Australie — Greenwashing Légal, Climate SLAPP Contre Activistes, Fossil Fuel Subsidies 7T$/An & Lobbying Anti-Climate",
            country="USA/Australie",
            environmental_defender_killing_criminalization_severity_score=52.0,
            climate_loss_damage_vulnerable_population_scale_score=50.0,
            fossil_fuel_corporate_impunity_score=51.0,
            climate_litigation_access_justice_deficit_gap_score=53.0,
            primary_pattern="fossil_fuel_corporate_impunity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-007",
            name="Global Witness/Frontline Defenders — Rapports Défenseurs Environnement, Cartographie Meurtres & Mécanismes Protection",
            country="Global",
            environmental_defender_killing_criminalization_severity_score=27.0,
            climate_loss_damage_vulnerable_population_scale_score=25.0,
            fossil_fuel_corporate_impunity_score=26.0,
            climate_litigation_access_justice_deficit_gap_score=26.0,
            primary_pattern="environmental_defender_killing_criminalization_severity",
        ),
        ClimateJusticeEnvironmentalDefendersEntity(
            entity_id="CJE-008",
            name="ONU/Accord Paris + Aarhus — Droits Humains Climate Change, Rapporteur Spécial & SDG 13 Action Climatique",
            country="Global",
            environmental_defender_killing_criminalization_severity_score=5.0,
            climate_loss_damage_vulnerable_population_scale_score=3.0,
            fossil_fuel_corporate_impunity_score=4.0,
            climate_litigation_access_justice_deficit_gap_score=4.0,
            primary_pattern="climate_litigation_access_justice_deficit_gap",
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

    return ClimateJusticeEnvironmentalDefendersEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_justice_environmental_defenders_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_environmental_defenders_annual_report",
            "ipcc_climate_loss_damage_vulnerable_populations",
            "frontline_defenders_at_risk_global_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_justice_environmental_defenders_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_justice_environmental_defenders_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
