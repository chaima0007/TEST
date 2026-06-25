from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WaterScarcityConflictRightsEntity:
    entity_id: str
    name: str
    country: str
    water_access_deprivation_weapon_score: float
    water_conflict_displacement_violence_score: float
    climate_drought_rights_impact_score: float
    water_governance_corruption_access_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_water_scarcity_conflict_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.water_access_deprivation_weapon_score * 0.30
            + self.water_conflict_displacement_violence_score * 0.25
            + self.climate_drought_rights_impact_score * 0.25
            + self.water_governance_corruption_access_gap_score * 0.20,
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
        self.estimated_water_scarcity_conflict_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class WaterScarcityConflictRightsEngineResult:
    agent: str = "Water Scarcity Conflict Rights Engine Agent"
    domain: str = "water_scarcity_conflict_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_water_scarcity_conflict_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WaterScarcityConflictRightsEntity] = field(default_factory=list)


def run_water_scarcity_conflict_rights_engine() -> WaterScarcityConflictRightsEngineResult:
    entities = [
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-001",
            name="Yémen — Réseau Eau Sanaa Détruit Frappes 2015-2023, Épidémie Choléra 2.5M Cas, Infrastructure Ciblée, 21M Sans Eau",
            country="Yémen",
            water_access_deprivation_weapon_score=97.0,
            water_conflict_displacement_violence_score=93.0,
            climate_drought_rights_impact_score=88.0,
            water_governance_corruption_access_gap_score=85.0,
            primary_pattern="water_access_deprivation_weapon",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-002",
            name="Gaza/Cisjordanie — 90L/Jour Gaza vs 300L Colons, Puits Détruits, Mer Méditerranée Salinisation, Blocus Matériaux",
            country="Palestine",
            water_access_deprivation_weapon_score=93.0,
            water_conflict_displacement_violence_score=89.0,
            climate_drought_rights_impact_score=85.0,
            water_governance_corruption_access_gap_score=82.0,
            primary_pattern="water_access_deprivation_weapon",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-003",
            name="Syrie — Barrages Euphrate Weaponisés IS/Turquie, Pumping Stations Détruites, 3M Sans Eau 2020 Hasaka Crise",
            country="Syrie",
            water_access_deprivation_weapon_score=89.0,
            water_conflict_displacement_violence_score=85.0,
            climate_drought_rights_impact_score=82.0,
            water_governance_corruption_access_gap_score=79.0,
            primary_pattern="water_conflict_displacement_violence",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-004",
            name="Afrique Subsaharienne/Lac Tchad — Réduction 90% Superficie, 30M Dépendants, Conflits Peuls-Agriculteurs, Boko Haram",
            country="Afrique Subsaharienne",
            water_access_deprivation_weapon_score=84.0,
            water_conflict_displacement_violence_score=80.0,
            climate_drought_rights_impact_score=78.0,
            water_governance_corruption_access_gap_score=75.0,
            primary_pattern="climate_drought_rights_impact",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-005",
            name="Inde/Pakistan — Indus Water Treaty Menacé 2023, Modi Suspension, Décharge Agriculture 80M Paysans, Tensions Nucléaires",
            country="Inde/Pakistan",
            water_access_deprivation_weapon_score=55.0,
            water_conflict_displacement_violence_score=51.0,
            climate_drought_rights_impact_score=50.0,
            water_governance_corruption_access_gap_score=47.0,
            primary_pattern="water_governance_corruption_access_gap",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-006",
            name="Éthiopie/GERD — Barrage Renaissance, Égypte-Soudan Menacés, Nil Bleu Réduit 25%, Négociations ONU Bloquées",
            country="Éthiopie",
            water_access_deprivation_weapon_score=51.0,
            water_conflict_displacement_violence_score=47.0,
            climate_drought_rights_impact_score=46.0,
            water_governance_corruption_access_gap_score=43.0,
            primary_pattern="water_conflict_displacement_violence",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-007",
            name="ONU/SDG6 — Objectif Eau Potable 2030, 2Md Sans Eau Sûre, Rapport OMS 2023, Financement 114Md$/An Insuffisant",
            country="Global",
            water_access_deprivation_weapon_score=27.0,
            water_conflict_displacement_violence_score=25.0,
            climate_drought_rights_impact_score=24.0,
            water_governance_corruption_access_gap_score=22.0,
            primary_pattern="water_governance_corruption_access_gap",
        ),
        WaterScarcityConflictRightsEntity(
            entity_id="WSC-008",
            name="Singapour/NEWater — Recyclage Eau 100%, Dessalement Avancé, Indépendance Hydrique, Modèle Stress Hydrique",
            country="Singapour",
            water_access_deprivation_weapon_score=5.0,
            water_conflict_displacement_violence_score=4.0,
            climate_drought_rights_impact_score=4.0,
            water_governance_corruption_access_gap_score=3.0,
            primary_pattern="climate_drought_rights_impact",
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

    return WaterScarcityConflictRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_water_scarcity_conflict_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unicef_jmp_water_sanitation_report",
            "un_water_world_water_development_report",
            "hrw_water_conflict_rights_violations_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_water_scarcity_conflict_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_water_scarcity_conflict_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
