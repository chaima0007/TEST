from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#14b8a6"


@dataclass
class ClimateRefugeeRightsEntity:
    entity_id: str
    name: str
    country: str
    displacement_severity_score: float
    legal_protection_gap_score: float
    adaptation_funding_gap_score: float
    territorial_loss_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_refugee_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.displacement_severity_score * 0.30
            + self.legal_protection_gap_score * 0.25
            + self.adaptation_funding_gap_score * 0.25
            + self.territorial_loss_score * 0.20,
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
        self.estimated_climate_refugee_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ClimateRefugeeRightsEngineResult:
    agent: str = "ClimateRefugeeRights Engine Agent"
    domain: str = "climate_refugee_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_climate_refugee_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateRefugeeRightsEntity] = field(default_factory=list)


def run_climate_refugee_rights_engine() -> ClimateRefugeeRightsEngineResult:
    entities = [
        ClimateRefugeeRightsEntity(
            entity_id="CRR-001",
            name="Bangladesh — 20M déplacés d'ici 2050, cyclones & montée des eaux",
            country="Bangladesh",
            displacement_severity_score=95.0,
            legal_protection_gap_score=94.0,
            adaptation_funding_gap_score=93.0,
            territorial_loss_score=96.0,
            primary_pattern="mass_climate_displacement_no_legal_status",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-002",
            name="Tuvalu — Île 50cm altitude, accord migration Australie 2023",
            country="Tuvalu",
            displacement_severity_score=90.0,
            legal_protection_gap_score=91.0,
            adaptation_funding_gap_score=89.0,
            territorial_loss_score=92.0,
            primary_pattern="complete_territorial_loss_sovereignty",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-003",
            name="Mozambique — Cyclones Idai/Kenneth, 2,5M déplacés",
            country="Mozambique",
            displacement_severity_score=84.0,
            legal_protection_gap_score=83.0,
            adaptation_funding_gap_score=82.0,
            territorial_loss_score=85.0,
            primary_pattern="cyclone_induced_mass_displacement",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-004",
            name="Pakistan — Inondations 2022, 33% territoire submergé",
            country="Pakistan",
            displacement_severity_score=78.0,
            legal_protection_gap_score=77.0,
            adaptation_funding_gap_score=76.0,
            territorial_loss_score=79.0,
            primary_pattern="catastrophic_flooding_infrastructure_loss",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-005",
            name="Îles Marshall — Migration vers USA, demande statut réfugié",
            country="Îles Marshall",
            displacement_severity_score=54.0,
            legal_protection_gap_score=53.0,
            adaptation_funding_gap_score=52.0,
            territorial_loss_score=55.0,
            primary_pattern="atoll_submersion_migration_statelessness",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-006",
            name="Éthiopie/Sahel — Sécheresses consécutives, déplacés climato-conflits",
            country="Éthiopie",
            displacement_severity_score=46.0,
            legal_protection_gap_score=45.0,
            adaptation_funding_gap_score=44.0,
            territorial_loss_score=47.0,
            primary_pattern="drought_conflict_nexus_displacement",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-007",
            name="Pays-Bas — Delta Works adaptation, inégalités globales réponse",
            country="Pays-Bas",
            displacement_severity_score=30.0,
            legal_protection_gap_score=29.0,
            adaptation_funding_gap_score=28.0,
            territorial_loss_score=31.0,
            primary_pattern="adaptation_infrastructure_global_disparity",
        ),
        ClimateRefugeeRightsEntity(
            entity_id="CRR-008",
            name="UNHCR/IPCC — Agenda Nansen, reconnaissance réfugiés climatiques ONU",
            country="International",
            displacement_severity_score=12.0,
            legal_protection_gap_score=11.0,
            adaptation_funding_gap_score=10.0,
            territorial_loss_score=13.0,
            primary_pattern="international_framework_climate_refugees",
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

    return ClimateRefugeeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_refugee_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ipcc_ar6_climate_change_displacement_risks_2022",
            "idmc_global_report_internal_displacement_2024",
            "un_human_rights_climate_change_obligations_report",
            "climate_vulnerable_forum_loss_damage_documentation",
            "unhcr_climate_displacement_protection_gap_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_refugee_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_refugee_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
