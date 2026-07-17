from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ClimateChangeHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    climate_displacement_refugee_rights_severity_score: float
    extreme_weather_livelihood_destruction_scale_score: float
    fossil_fuel_community_health_impact_score: float
    climate_justice_loss_damage_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_change_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.climate_displacement_refugee_rights_severity_score * 0.30
            + self.extreme_weather_livelihood_destruction_scale_score * 0.25
            + self.fossil_fuel_community_health_impact_score * 0.25
            + self.climate_justice_loss_damage_deficit_gap_score * 0.20,
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
        self.estimated_climate_change_human_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ClimateChangeHumanRightsEngineResult:
    agent: str = "Climate Change Human Rights Engine Agent"
    domain: str = "climate_change_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_climate_change_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateChangeHumanRightsEntity] = field(default_factory=list)


def run_climate_change_human_rights_engine() -> ClimateChangeHumanRightsEngineResult:
    entities = [
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-001",
            name="Tuvalu/Îles Pacifique — Submersion Territoriale Totale, 11 000 Citoyens Apatrides Futurs, Coraux Blanchis & Eau Douce Salinisée",
            country="Tuvalu/Pacifique",
            climate_displacement_refugee_rights_severity_score=97.0,
            extreme_weather_livelihood_destruction_scale_score=95.0,
            fossil_fuel_community_health_impact_score=93.0,
            climate_justice_loss_damage_deficit_gap_score=96.0,
            primary_pattern="climate_displacement_refugee_rights_severity",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-002",
            name="Bangladesh/Delta du Gange — 20M Réfugiés Climatiques 2050, Cyclones Amplifiés, Inondations Annuelles & Salinisation Terres Agricoles",
            country="Bangladesh",
            climate_displacement_refugee_rights_severity_score=94.0,
            extreme_weather_livelihood_destruction_scale_score=92.0,
            fossil_fuel_community_health_impact_score=90.0,
            climate_justice_loss_damage_deficit_gap_score=93.0,
            primary_pattern="climate_displacement_refugee_rights_severity",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-003",
            name="Sahel/Afrique — Désertification 6M km², Conflits Éleveurs-Agriculteurs Eau, Famines Récurrentes & 1M+ Déplacés Annuels",
            country="Sahel/Afrique",
            climate_displacement_refugee_rights_severity_score=91.0,
            extreme_weather_livelihood_destruction_scale_score=89.0,
            fossil_fuel_community_health_impact_score=88.0,
            climate_justice_loss_damage_deficit_gap_score=90.0,
            primary_pattern="extreme_weather_livelihood_destruction_scale",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-004",
            name="Amazonie/Brésil — Déforestation 20% Biome, Communautés Autochtones Chassées, Sécheresses Record & Droits Territoriaux Violés",
            country="Brésil/Amazonie",
            climate_displacement_refugee_rights_severity_score=82.0,
            extreme_weather_livelihood_destruction_scale_score=80.0,
            fossil_fuel_community_health_impact_score=83.0,
            climate_justice_loss_damage_deficit_gap_score=81.0,
            primary_pattern="fossil_fuel_community_health_impact",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-005",
            name="Australie/Bushfires 2019-2020 — 3 Milliards Animaux Tués, Communautés Rurales Détruites, Fumée=Santé Publique & Peuples Premiers Terres Brûlées",
            country="Australie",
            climate_displacement_refugee_rights_severity_score=57.0,
            extreme_weather_livelihood_destruction_scale_score=55.0,
            fossil_fuel_community_health_impact_score=54.0,
            climate_justice_loss_damage_deficit_gap_score=56.0,
            primary_pattern="extreme_weather_livelihood_destruction_scale",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-006",
            name="USA/Porto Rico Ouragan Maria — Infrastructure Détruite 6 Mois, 3 000 Morts Non-Reconnus, Diaspora Forcée & Abandon Fédéral Documenté",
            country="USA/Porto Rico",
            climate_displacement_refugee_rights_severity_score=54.0,
            extreme_weather_livelihood_destruction_scale_score=52.0,
            fossil_fuel_community_health_impact_score=51.0,
            climate_justice_loss_damage_deficit_gap_score=53.0,
            primary_pattern="climate_displacement_refugee_rights_severity",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-007",
            name="IPCC/UNHRC — Rapport Changement Climatique Droits Humains 2022, Résolution ONU Droit Environnement Sain & Rapporteur Spécial Créé",
            country="Global",
            climate_displacement_refugee_rights_severity_score=28.0,
            extreme_weather_livelihood_destruction_scale_score=27.0,
            fossil_fuel_community_health_impact_score=26.0,
            climate_justice_loss_damage_deficit_gap_score=25.0,
            primary_pattern="climate_justice_loss_damage_deficit_gap",
        ),
        ClimateChangeHumanRightsEntity(
            entity_id="CCH-008",
            name="ONU/Accord Paris — COP28 Fonds Loss & Damage 700M$, NDC Insuffisantes 2.7°C Trajectoire & Mécanisme Compensation Climatique Partiel",
            country="Global",
            climate_displacement_refugee_rights_severity_score=5.0,
            extreme_weather_livelihood_destruction_scale_score=4.0,
            fossil_fuel_community_health_impact_score=4.0,
            climate_justice_loss_damage_deficit_gap_score=5.0,
            primary_pattern="climate_justice_loss_damage_deficit_gap",
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

    return ClimateChangeHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_change_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ipcc_sixth_assessment_report_2022",
            "unhrc_climate_change_human_rights_resolution",
            "internal_displacement_monitoring_centre_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_change_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_climate_change_human_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
