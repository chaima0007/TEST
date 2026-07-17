from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ENGINE_VERSION = "1.0.0"

@dataclass
class WaterRightsAccessSanitationEntity:
    entity_id: str
    name: str
    country: str
    water_access_denial_civilian_severity_score: float
    sanitation_infrastructure_collapse_score: float
    water_privatization_rights_erosion_score: float
    water_conflict_weaponization_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_water_rights_access_sanitation_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.water_access_denial_civilian_severity_score * 0.30
            + self.sanitation_infrastructure_collapse_score * 0.25
            + self.water_privatization_rights_erosion_score * 0.25
            + self.water_conflict_weaponization_score * 0.20,
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
        self.estimated_water_rights_access_sanitation_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class WaterRightsAccessSanitationEngineResult:
    agent: str = "Water Rights Access Sanitation Engine Agent"
    domain: str = "water_rights_access_sanitation"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = ENGINE_VERSION
    avg_estimated_water_rights_access_sanitation_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WaterRightsAccessSanitationEntity] = field(default_factory=list)


def run_water_rights_access_sanitation_engine() -> WaterRightsAccessSanitationEngineResult:
    entities = [
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-001",
            name="Yemen — Infrastructures Eau Détruites Guerre, Millions Sans Accès Eau Potable, Choléra Épidémique & Puits Bombardés Coalition",
            country="Yemen",
            water_access_denial_civilian_severity_score=96.0,
            sanitation_infrastructure_collapse_score=92.0,
            water_privatization_rights_erosion_score=85.0,
            water_conflict_weaponization_score=95.0,
            primary_pattern="crise_acces_eau_potable",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-002",
            name="RDC — Accès Eau Potable 35% Population Zones Conflit Kivu, Cholera Endémique, Femmes 6h Transport Eau & Contamination Intentionnelle",
            country="RDC",
            water_access_denial_civilian_severity_score=90.0,
            sanitation_infrastructure_collapse_score=88.0,
            water_privatization_rights_erosion_score=80.0,
            water_conflict_weaponization_score=82.0,
            primary_pattern="effondrement_infrastructures_sanitaires",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-003",
            name="Gaza — Désalinisation Détruite Siège, Eau Contaminée Population Civile, Infrastructures WASH Bombardées & Accès Bloqué Humanitaire",
            country="Palestine/Gaza",
            water_access_denial_civilian_severity_score=95.0,
            sanitation_infrastructure_collapse_score=90.0,
            water_privatization_rights_erosion_score=78.0,
            water_conflict_weaponization_score=96.0,
            primary_pattern="eau_arme_conflit",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-004",
            name="Somalie — Sécheresse Crise Humanitaire Eau 2022, 7M Personnes Déplacées, Pénurie Eau Pastorale & Enfants Malnutrition Déshydratation",
            country="Somalie",
            water_access_denial_civilian_severity_score=88.0,
            sanitation_infrastructure_collapse_score=84.0,
            water_privatization_rights_erosion_score=72.0,
            water_conflict_weaponization_score=76.0,
            primary_pattern="crise_acces_eau_potable",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-005",
            name="Bolivie/Cochabamba — Guerre de l'Eau Privatisation Bechtel 1999, Contrats Illégaux, Coupures Accès Pauvres & Résistance Populaire Réprimée",
            country="Bolivie",
            water_access_denial_civilian_severity_score=55.0,
            sanitation_infrastructure_collapse_score=48.0,
            water_privatization_rights_erosion_score=78.0,
            water_conflict_weaponization_score=40.0,
            primary_pattern="privatisation_eau_violation_droits",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-006",
            name="Inde/Punjab — Stress Hydrique Agriculture Intensive, Surexploitation Aquifères, Pesticides Eau Souterraine & Crise Accès Rural Dalit",
            country="Inde",
            water_access_denial_civilian_severity_score=50.0,
            sanitation_infrastructure_collapse_score=45.0,
            water_privatization_rights_erosion_score=62.0,
            water_conflict_weaponization_score=38.0,
            primary_pattern="privatisation_eau_violation_droits",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-007",
            name="Chili — Privatisation Eau Constitutionnelle Codes 1981, Droits Propriété Eau Concentrés Agro-Industrie & Communautés Sans Accès Garanti",
            country="Chili",
            water_access_denial_civilian_severity_score=28.0,
            sanitation_infrastructure_collapse_score=25.0,
            water_privatization_rights_erosion_score=42.0,
            water_conflict_weaponization_score=22.0,
            primary_pattern="privatisation_eau_violation_droits",
        ),
        WaterRightsAccessSanitationEntity(
            entity_id="WRAS-008",
            name="Pays-Bas — Eau Bien Commun Modèle Gestion Publique, Interdiction Privatisation Constitutionnelle, Standards RIVM & Accès Universel Garanti",
            country="Pays-Bas",
            water_access_denial_civilian_severity_score=5.0,
            sanitation_infrastructure_collapse_score=4.0,
            water_privatization_rights_erosion_score=6.0,
            water_conflict_weaponization_score=3.0,
            primary_pattern="crise_acces_eau_potable",
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

    return WaterRightsAccessSanitationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_water_rights_access_sanitation_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_unicef_joint_water_monitoring_2023",
            "human_rights_watch_water_crisis_reports",
            "food_water_watch_privatization_database",
            "oxfam_water_conflict_monitor_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_water_rights_access_sanitation_engine()
    print(f"Agent: {result.agent}")
    print(f"Engine version: {result.engine_version}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Confidence score: {result.confidence_score}")
    print(f"Avg index: {result.avg_estimated_water_rights_access_sanitation_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    print(f"Data sources: {result.data_sources}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — index={e.estimated_water_rights_access_sanitation_index}")
