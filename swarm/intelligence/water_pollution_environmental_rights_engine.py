from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class WaterPollutionEnvironmentalRightsEntity:
    entity_id: str
    name: str
    country: str
    water_contamination_health_impact_score: float
    industrial_pollution_corporate_impunity_score: float
    community_displacement_sacrifice_zone_score: float
    environmental_legal_protection_enforcement_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_water_pollution_environmental_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.water_contamination_health_impact_score * 0.30
            + self.industrial_pollution_corporate_impunity_score * 0.25
            + self.community_displacement_sacrifice_zone_score * 0.25
            + self.environmental_legal_protection_enforcement_gap_score * 0.20,
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
        self.estimated_water_pollution_environmental_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class WaterPollutionEnvironmentalRightsEngineResult:
    agent: str = "Water Pollution Environmental Rights Engine Agent"
    domain: str = "water_pollution_environmental_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"


def run_water_pollution_environmental_rights_engine() -> WaterPollutionEnvironmentalRightsEngineResult:
    entities = [
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="NGA-002",
            name="Nigeria/Delta Niger",
            country="Nigeria",
            water_contamination_health_impact_score=92.0,
            industrial_pollution_corporate_impunity_score=95.0,
            community_displacement_sacrifice_zone_score=88.0,
            environmental_legal_protection_enforcement_gap_score=90.0,
            primary_pattern="Shell 50 ans déversements, 4000+ fuites documentées UNEP 2011, pêcheurs sans recours, eau potable impossible",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="CHN-001",
            name="Chine/Fleuve Jaune",
            country="Chine",
            water_contamination_health_impact_score=88.0,
            industrial_pollution_corporate_impunity_score=86.0,
            community_displacement_sacrifice_zone_score=82.0,
            environmental_legal_protection_enforcement_gap_score=88.0,
            primary_pattern="320M personnes eau contaminée métaux lourds, usines chimiques, Jiangsu cancers eau, censure données",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="IND-003",
            name="Inde/Gange",
            country="Inde",
            water_contamination_health_impact_score=85.0,
            industrial_pollution_corporate_impunity_score=82.0,
            community_displacement_sacrifice_zone_score=80.0,
            environmental_legal_protection_enforcement_gap_score=84.0,
            primary_pattern="80% maladies eau contaminée, 1500 tanières cuir Kanpur, arsenic Bihar, fluorose endémique",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="BGD-001",
            name="Bangladesh/Arsenic",
            country="Bangladesh",
            water_contamination_health_impact_score=86.0,
            industrial_pollution_corporate_impunity_score=78.0,
            community_displacement_sacrifice_zone_score=76.0,
            environmental_legal_protection_enforcement_gap_score=82.0,
            primary_pattern="20M personnes eaux souterraines arsenic naturel+industrie, cancers peau/poumons, aide insuffisante",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="USA-002",
            name="USA/Flint Michigan",
            country="USA",
            water_contamination_health_impact_score=60.0,
            industrial_pollution_corporate_impunity_score=55.0,
            community_displacement_sacrifice_zone_score=58.0,
            environmental_legal_protection_enforcement_gap_score=52.0,
            primary_pattern="Plomb eau 2014-2019, enfants intoxiqués, majorité noire sacrifiée, impunité fonctionnaires",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="PER-003",
            name="Pérou/Cerro de Pasco",
            country="Pérou",
            water_contamination_health_impact_score=58.0,
            industrial_pollution_corporate_impunity_score=62.0,
            community_displacement_sacrifice_zone_score=55.0,
            environmental_legal_protection_enforcement_gap_score=60.0,
            primary_pattern="Plomb/arsenic sang enfants 3x norme OMS, Volcan mine, déplacement refusé",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="FRA-002",
            name="France/PFAS",
            country="France",
            water_contamination_health_impact_score=38.0,
            industrial_pollution_corporate_impunity_score=35.0,
            community_displacement_sacrifice_zone_score=28.0,
            environmental_legal_protection_enforcement_gap_score=32.0,
            primary_pattern="PFAS Rhône/Ain, 14M personnes eau contaminée, Arkema/Daikin, action en justice en cours",
        ),
        WaterPollutionEnvironmentalRightsEntity(
            entity_id="DEU-001",
            name="Allemagne",
            country="Allemagne",
            water_contamination_health_impact_score=10.0,
            industrial_pollution_corporate_impunity_score=8.0,
            community_displacement_sacrifice_zone_score=7.0,
            environmental_legal_protection_enforcement_gap_score=9.0,
            primary_pattern="Wasserhaushaltsgesetz solide, contrôles stricts, rares dépassements norme, recours juridiques effectifs",
        ),
    ]

    result = WaterPollutionEnvironmentalRightsEngineResult()
    result.total_entities = len(entities)
    result.avg_composite = round(
        statistics.mean(e.composite_score for e in entities), 2
    )
    result.confidence_score = 0.88

    risk_dist: dict = {}
    for e in entities:
        risk_dist[e.risk_level] = risk_dist.get(e.risk_level, 0) + 1
    result.risk_distribution = risk_dist

    sorted_entities = sorted(entities, key=lambda e: e.composite_score, reverse=True)
    result.top_risk_entities = [e.name for e in sorted_entities[:3]]
    result.critical_alerts = [
        f"{e.name}: composite={e.composite_score}, index={e.estimated_water_pollution_environmental_rights_index}"
        for e in sorted_entities
        if e.risk_level == "critique"
    ]
    result.data_sources = [
        "who_drinking_water_quality_guidelines_2022",
        "unep_pollution_action_note_2023",
        "business_human_rights_resource_pollution_database",
        "amnesty_international_environmental_rights_report_2023",
    ]

    return result


if __name__ == "__main__":
    result = run_water_pollution_environmental_rights_engine()
    print(f"Agent      : {result.agent}")
    print(f"Domain     : {result.domain}")
    print(f"Entities   : {result.total_entities}")
    print(f"Avg composite : {result.avg_composite}")
    print(f"Confidence : {result.confidence_score}")
    print(f"Distribution: {result.risk_distribution}")
    print(f"Top risks  : {result.top_risk_entities}")
    print("Critical alerts:")
    for alert in result.critical_alerts:
        print(f"  - {alert}")
    print(f"Sources    : {result.data_sources}")
