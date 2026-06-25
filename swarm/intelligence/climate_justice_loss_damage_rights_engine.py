from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateJusticeLossDamageRightsEntity:
    entity_id: str
    name: str
    country: str
    loss_damage_compensation_denial_score: float
    climate_vulnerable_population_rights_gap_score: float
    fossil_fuel_subsidy_rights_violation_score: float
    climate_finance_access_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_justice_loss_damage_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.loss_damage_compensation_denial_score * 0.30
            + self.climate_vulnerable_population_rights_gap_score * 0.25
            + self.fossil_fuel_subsidy_rights_violation_score * 0.25
            + self.climate_finance_access_accountability_gap_score * 0.20,
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
        self.estimated_climate_justice_loss_damage_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ClimateJusticeLossDamageRightsEngineResult:
    agent: str = "Climate Justice Loss Damage Rights Engine Agent"
    domain: str = "climate_justice_loss_damage_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_justice_loss_damage_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateJusticeLossDamageRightsEntity] = field(default_factory=list)


def run_climate_justice_loss_damage_rights_engine() -> ClimateJusticeLossDamageRightsEngineResult:
    entities = [
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-001",
            name="Bangladesh/Deltas — 18M Habitants Zones Inondables, Cyclones +40% Intensité, Haor Submergés, Migration Forcée 2050",
            country="Bangladesh",
            loss_damage_compensation_denial_score=93.0,
            climate_vulnerable_population_rights_gap_score=90.0,
            fossil_fuel_subsidy_rights_violation_score=85.0,
            climate_finance_access_accountability_gap_score=82.0,
            primary_pattern="loss_damage_compensation_denial",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-002",
            name="Maldives/Tuvalu — Submersion 2100 Certaine, Souveraineté Menacée, Évacuation Population, Leaders À L&apos;ONU Plongent",
            country="Maldives/Tuvalu",
            loss_damage_compensation_denial_score=90.0,
            climate_vulnerable_population_rights_gap_score=87.0,
            fossil_fuel_subsidy_rights_violation_score=83.0,
            climate_finance_access_accountability_gap_score=80.0,
            primary_pattern="climate_vulnerable_population_rights_gap",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-003",
            name="Pakistan/Inondations 2022 — 1/3 Territoire Immergé, 33M Sinistrés, 1700 Morts, 0.9% Émissions Mondiales Pakistan",
            country="Pakistan",
            loss_damage_compensation_denial_score=86.0,
            climate_vulnerable_population_rights_gap_score=83.0,
            fossil_fuel_subsidy_rights_violation_score=79.0,
            climate_finance_access_accountability_gap_score=76.0,
            primary_pattern="loss_damage_compensation_denial",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-004",
            name="Sahel/Désertification — Terres Arables -40% 50 Ans, Famine Structurelle, Pastoralisme Détruit, Migration Climat",
            country="Sahel",
            loss_damage_compensation_denial_score=82.0,
            climate_vulnerable_population_rights_gap_score=79.0,
            fossil_fuel_subsidy_rights_violation_score=76.0,
            climate_finance_access_accountability_gap_score=73.0,
            primary_pattern="climate_vulnerable_population_rights_gap",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-005",
            name="USA/Chevron/Shell — Lobbying COP28, Délégations Record Fossiles 2400 Lobbyistes, Finance Déni Science",
            country="USA",
            loss_damage_compensation_denial_score=55.0,
            climate_vulnerable_population_rights_gap_score=52.0,
            fossil_fuel_subsidy_rights_violation_score=50.0,
            climate_finance_access_accountability_gap_score=47.0,
            primary_pattern="fossil_fuel_subsidy_rights_violation",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-006",
            name="UE/Carbon Border — Mécanisme Ajustement Carbone 2026, Pays ACP Impacts Commerciaux, Transition Juste Insuffisante",
            country="Union Européenne",
            loss_damage_compensation_denial_score=51.0,
            climate_vulnerable_population_rights_gap_score=48.0,
            fossil_fuel_subsidy_rights_violation_score=46.0,
            climate_finance_access_accountability_gap_score=43.0,
            primary_pattern="climate_finance_access_accountability_gap",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-007",
            name="ONU/Experts Droits — Rapport Droits Humains Changement Climatique 2023, Résolution 76/300 Droit Environnement",
            country="Global",
            loss_damage_compensation_denial_score=28.0,
            climate_vulnerable_population_rights_gap_score=26.0,
            fossil_fuel_subsidy_rights_violation_score=24.0,
            climate_finance_access_accountability_gap_score=22.0,
            primary_pattern="loss_damage_compensation_denial",
        ),
        ClimateJusticeLossDamageRightsEntity(
            entity_id="CJLD-008",
            name="Costa Rica/Pays Verts — 100% EnR 2022, Moratorium Pétrole, Biodiversité Protégée 25% Territoire, Modèle Tropical",
            country="Costa Rica",
            loss_damage_compensation_denial_score=5.0,
            climate_vulnerable_population_rights_gap_score=4.0,
            fossil_fuel_subsidy_rights_violation_score=4.0,
            climate_finance_access_accountability_gap_score=3.0,
            primary_pattern="climate_finance_access_accountability_gap",
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

    return ClimateJusticeLossDamageRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_justice_loss_damage_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unfccc_loss_damage_mechanism_cop27_cop28_reports",
            "ipcc_sixth_assessment_report_impacts_adaptation",
            "hrw_climate_justice_human_rights_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_justice_loss_damage_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_justice_loss_damage_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
