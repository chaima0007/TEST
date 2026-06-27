from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateDisplacementEntity:
    entity_id: str
    name: str
    country: str
    displacement_scale_severity_score: float
    legal_protection_gap_score: float
    adaptation_finance_absence_score: float
    return_resettlement_impossibility_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_displacement_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.displacement_scale_severity_score * 0.30
            + self.legal_protection_gap_score * 0.25
            + self.adaptation_finance_absence_score * 0.25
            + self.return_resettlement_impossibility_score * 0.20,
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
        self.estimated_climate_displacement_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ClimateDisplacementEngineResult:
    agent: str = "Climate Displacement Engine Agent"
    domain: str = "climate_displacement"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_displacement_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateDisplacementEntity] = field(default_factory=list)

def run_climate_displacement_engine() -> ClimateDisplacementEngineResult:
    entities = [
        ClimateDisplacementEntity(
            entity_id="CD-001",
            name="Tuvalu/Kiribati — Submersion Totale Prévue 2050, 100% Population Déplacée & Souveraineté Perdue",
            country="Océanie",
            displacement_scale_severity_score=95.0,
            legal_protection_gap_score=95.0,
            adaptation_finance_absence_score=92.0,
            return_resettlement_impossibility_score=98.0,
            primary_pattern="return_resettlement_impossibility",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-002",
            name="Bangladesh — 20M Déplacés Cyclones/Inondations, Deltas Submergés & Migration Urbaine Forcée",
            country="Asie du Sud",
            displacement_scale_severity_score=92.0,
            legal_protection_gap_score=88.0,
            adaptation_finance_absence_score=90.0,
            return_resettlement_impossibility_score=85.0,
            primary_pattern="displacement_scale_severity",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-003",
            name="Sahel/Afrique — Désertification 10M Déplacés, Conflit Eau/Terre & Aucun Statut Légal",
            country="Afrique Sub-Saharienne",
            displacement_scale_severity_score=88.0,
            legal_protection_gap_score=90.0,
            adaptation_finance_absence_score=88.0,
            return_resettlement_impossibility_score=82.0,
            primary_pattern="legal_protection_gap",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-004",
            name="Philippines — Typhons Annuels, 4M Déplacés/An & Reconstruction Zones Rouge Impossible",
            country="Asie du Sud-Est",
            displacement_scale_severity_score=85.0,
            legal_protection_gap_score=80.0,
            adaptation_finance_absence_score=82.0,
            return_resettlement_impossibility_score=85.0,
            primary_pattern="return_resettlement_impossibility",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-005",
            name="USA/Alaska — Villages Autochtones Érodés, Relocalisation Fédérale Lente & Cultures Perdues",
            country="Amérique du Nord",
            displacement_scale_severity_score=52.0,
            legal_protection_gap_score=48.0,
            adaptation_finance_absence_score=55.0,
            return_resettlement_impossibility_score=58.0,
            primary_pattern="adaptation_finance_absence",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-006",
            name="Europe/Méditerranée — Migrations Climatiques Mélangées, Distinction Réfugiés Inexistante & Refoulements",
            country="Europe",
            displacement_scale_severity_score=48.0,
            legal_protection_gap_score=55.0,
            adaptation_finance_absence_score=45.0,
            return_resettlement_impossibility_score=50.0,
            primary_pattern="legal_protection_gap",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-007",
            name="IDMC/UNHCR — Monitoring Déplacements, Plaidoyer Statut Légal & Nansen Initiative",
            country="Global",
            displacement_scale_severity_score=22.0,
            legal_protection_gap_score=25.0,
            adaptation_finance_absence_score=28.0,
            return_resettlement_impossibility_score=30.0,
            primary_pattern="displacement_scale_severity",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-008",
            name="ONU/Résolution — Reconnaissance Réfugiés Climatiques, Agenda Nansen & Lacunes Convention 1951",
            country="Global",
            displacement_scale_severity_score=4.0,
            legal_protection_gap_score=5.0,
            adaptation_finance_absence_score=3.0,
            return_resettlement_impossibility_score=6.0,
            primary_pattern="legal_protection_gap",
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

    return ClimateDisplacementEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_displacement_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "idmc_global_report_internal_displacement_annual",
            "unhcr_climate_change_displacement_legal_protection_gap_report",
            "world_bank_groundswell_climate_migration_projections_2050",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_climate_displacement_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_displacement_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
