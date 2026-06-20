from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateDisplacementEntity:
    entity_id: str
    name: str
    country: str
    displacement_scale_score: float
    state_protection_failure_score: float
    international_legal_gap_score: float
    adaptation_resource_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_displacement_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.displacement_scale_score * 0.30
            + self.state_protection_failure_score * 0.25
            + self.international_legal_gap_score * 0.25
            + self.adaptation_resource_denial_score * 0.20,
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
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_climate_displacement_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateDisplacementEntity] = field(default_factory=list)

def run_climate_displacement_engine() -> ClimateDisplacementEngineResult:
    entities = [
        ClimateDisplacementEntity(
            entity_id="CD-001",
            name="Bangladesh/Delta — 30M Menacés Hausse Mer, Cyclones & Déplacement Structurel",
            country="Asie du Sud",
            displacement_scale_score=92.0,
            state_protection_failure_score=88.0,
            international_legal_gap_score=90.0,
            adaptation_resource_denial_score=85.0,
            primary_pattern="displacement_scale",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-002",
            name="Îles Pacifique/Tuvalu — Submersion Totale, 11 000 Habitants & Disparition d'une Nation",
            country="Océanie",
            displacement_scale_score=88.0,
            state_protection_failure_score=85.0,
            international_legal_gap_score=92.0,
            adaptation_resource_denial_score=90.0,
            primary_pattern="international_legal_gap",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-003",
            name="Sahel/Afrique — 50M Déplacés Sécheresse, Conflits Eau & Désertification Massive",
            country="Afrique Sub-Saharienne",
            displacement_scale_score=85.0,
            state_protection_failure_score=80.0,
            international_legal_gap_score=88.0,
            adaptation_resource_denial_score=82.0,
            primary_pattern="state_protection_failure",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-004",
            name="Syrie/Moyen-Orient — Sécheresse 2006-2010, Déplacement Préalable & Conflit Armé",
            country="Moyen-Orient",
            displacement_scale_score=72.0,
            state_protection_failure_score=75.0,
            international_legal_gap_score=80.0,
            adaptation_resource_denial_score=78.0,
            primary_pattern="adaptation_resource_denial",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-005",
            name="Inde/Orissa — 8M Déplacés Catastrophes, Communautés Côtières & Barrage Sardar",
            country="Asie du Sud",
            displacement_scale_score=52.0,
            state_protection_failure_score=55.0,
            international_legal_gap_score=58.0,
            adaptation_resource_denial_score=50.0,
            primary_pattern="displacement_scale",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-006",
            name="USA/Puerto Rico — Ouragan Maria, Déplacement Non Reconnu & Inégalité Reconstruction",
            country="Amérique du Nord",
            displacement_scale_score=48.0,
            state_protection_failure_score=52.0,
            international_legal_gap_score=55.0,
            adaptation_resource_denial_score=58.0,
            primary_pattern="state_protection_failure",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-007",
            name="Europe/Méditerranée — Réfugiés Climatiques Refoulés, Convention 1951 Inadaptée",
            country="Europe",
            displacement_scale_score=25.0,
            state_protection_failure_score=30.0,
            international_legal_gap_score=32.0,
            adaptation_resource_denial_score=28.0,
            primary_pattern="international_legal_gap",
        ),
        ClimateDisplacementEntity(
            entity_id="CD-008",
            name="ONU/UNHCR/IPCC — Cadre Nansen, Principes Directeurs & Vide Juridique International",
            country="Global",
            displacement_scale_score=4.0,
            state_protection_failure_score=5.0,
            international_legal_gap_score=3.0,
            adaptation_resource_denial_score=6.0,
            primary_pattern="displacement_scale",
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
            "unhcr_global_trends_forced_displacement_annual_report",
            "ipcc_sixth_assessment_report_impacts_adaptation_vulnerability_chapter_climate_migration",
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
