from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WaterSanitationAccessRightsEntity:
    entity_id: str
    name: str
    country: str
    safe_water_access_denial_severity_score: float
    sanitation_infrastructure_absence_scale_score: float
    water_privatization_commodification_score: float
    climate_water_stress_conflict_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_water_sanitation_access_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.safe_water_access_denial_severity_score * 0.30
            + self.sanitation_infrastructure_absence_scale_score * 0.25
            + self.water_privatization_commodification_score * 0.25
            + self.climate_water_stress_conflict_deficit_gap_score * 0.20,
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
        self.estimated_water_sanitation_access_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class WaterSanitationAccessRightsEngineResult:
    agent: str = "Water Sanitation Access Rights Engine Agent"
    domain: str = "water_sanitation_access_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_water_sanitation_access_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WaterSanitationAccessRightsEntity] = field(default_factory=list)


def run_water_sanitation_access_rights_engine() -> WaterSanitationAccessRightsEngineResult:
    entities = [
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-001",
            name="Yemen — Guerre Civile Infrastructure Eau Détruite, Choléra 2.5M Cas, Puits Bombardés & Population Sans Eau Potable",
            country="Yemen",
            safe_water_access_denial_severity_score=95.0,
            sanitation_infrastructure_absence_scale_score=93.0,
            water_privatization_commodification_score=91.0,
            climate_water_stress_conflict_deficit_gap_score=94.0,
            primary_pattern="safe_water_access_denial_severity",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-002",
            name="RDC/Kivu — Zones Conflit Sans Eau Traitée, Cholera Endémique, Femmes 6h/Jour Eau & Viols Puits Contamination Intentionnelle",
            country="RDC",
            safe_water_access_denial_severity_score=91.0,
            sanitation_infrastructure_absence_scale_score=92.0,
            water_privatization_commodification_score=88.0,
            climate_water_stress_conflict_deficit_gap_score=90.0,
            primary_pattern="sanitation_infrastructure_absence_scale",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-003",
            name="Inde/Assainissement — 500M Sans Toilettes 2020, Défécation Espace Ouvert, Dalits Puits Interdits & Fluorose Eaux Contaminées",
            country="Inde",
            safe_water_access_denial_severity_score=88.0,
            sanitation_infrastructure_absence_scale_score=89.0,
            water_privatization_commodification_score=85.0,
            climate_water_stress_conflict_deficit_gap_score=87.0,
            primary_pattern="sanitation_infrastructure_absence_scale",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-004",
            name="Bolivie/Cochabamba — Privatisation Eau Bechtel 1999, Guerre de l'Eau, Coupures Pauvres & Militarisation Distribution",
            country="Bolivie",
            safe_water_access_denial_severity_score=84.0,
            sanitation_infrastructure_absence_scale_score=82.0,
            water_privatization_commodification_score=86.0,
            climate_water_stress_conflict_deficit_gap_score=83.0,
            primary_pattern="water_privatization_commodification",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-005",
            name="Pakistan/Inondations — Inondations 2022 33M Affectés, Eau Contaminée Post-Désastre, Infrastructure WASH Détruite & Diarrhée Mortelle",
            country="Pakistan",
            safe_water_access_denial_severity_score=56.0,
            sanitation_infrastructure_absence_scale_score=54.0,
            water_privatization_commodification_score=55.0,
            climate_water_stress_conflict_deficit_gap_score=53.0,
            primary_pattern="climate_water_stress_conflict_deficit_gap",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-006",
            name="Mexique/Pénurie — Mexico City Day Zero, Aquifères Sur-Exploités, Colonie Sans Eau Courante & Distribution Camion-Citerne Corruption",
            country="Mexique",
            safe_water_access_denial_severity_score=53.0,
            sanitation_infrastructure_absence_scale_score=51.0,
            water_privatization_commodification_score=54.0,
            climate_water_stress_conflict_deficit_gap_score=52.0,
            primary_pattern="safe_water_access_denial_severity",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-007",
            name="ONU/EAU — Résolution 64/292 Droit Eau 2010, WaterAid, WASH Monitoring & Reporting JMP",
            country="Global",
            safe_water_access_denial_severity_score=27.0,
            sanitation_infrastructure_absence_scale_score=25.0,
            water_privatization_commodification_score=28.0,
            climate_water_stress_conflict_deficit_gap_score=26.0,
            primary_pattern="sanitation_infrastructure_absence_scale",
        ),
        WaterSanitationAccessRightsEntity(
            entity_id="WAR-008",
            name="SDG6/OMS — ODD 6 Eau Potable 2030, OMS Standards Qualité, Rapport Progrès & Mécanismes Financement",
            country="Global",
            safe_water_access_denial_severity_score=4.0,
            sanitation_infrastructure_absence_scale_score=4.0,
            water_privatization_commodification_score=4.0,
            climate_water_stress_conflict_deficit_gap_score=4.0,
            primary_pattern="safe_water_access_denial_severity",
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

    return WaterSanitationAccessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_water_sanitation_access_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unicef_jmp_water_sanitation_report",
            "un_water_sdg6_progress_report",
            "human_rights_watch_water_conflict_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_water_sanitation_access_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_water_sanitation_access_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
