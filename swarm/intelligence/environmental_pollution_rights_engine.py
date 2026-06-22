from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#22c55e"


@dataclass
class EnvironmentalPollutionRightsEntity:
    entity_id: str
    name: str
    country: str
    air_pollution_mortality_score: float
    water_contamination_score: float
    toxic_waste_exposure_score: float
    environmental_justice_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_pollution_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.air_pollution_mortality_score * 0.30
            + self.water_contamination_score * 0.25
            + self.toxic_waste_exposure_score * 0.25
            + self.environmental_justice_gap_score * 0.20,
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
        self.estimated_environmental_pollution_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class EnvironmentalPollutionRightsEngineResult:
    agent: str = "Environmental Pollution Rights Engine Agent"
    domain: str = "environmental_pollution_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_pollution_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalPollutionRightsEntity] = field(default_factory=list)


def run_environmental_pollution_rights_engine() -> EnvironmentalPollutionRightsEngineResult:
    entities = [
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-001",
            name="Bangladesh — Pollution Textile Dhaka Rivières, 99% Eau Contaminée & 280 000 Morts/An Pollution Air",
            country="Bangladesh",
            air_pollution_mortality_score=89.0,
            water_contamination_score=91.0,
            toxic_waste_exposure_score=88.0,
            environmental_justice_gap_score=90.0,
            primary_pattern="water_contamination_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-002",
            name="Pakistan — Lahore Ville la Plus Polluée Monde 2024, Smog Paralysant & Crise Eau Souterraine",
            country="Pakistan",
            air_pollution_mortality_score=88.0,
            water_contamination_score=86.0,
            toxic_waste_exposure_score=85.0,
            environmental_justice_gap_score=87.0,
            primary_pattern="air_pollution_mortality_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-003",
            name="Inde — Delhi Smog Mortel, 1,67 Million Morts Pollution Air/An & Fleuves Sacrés Toxiques",
            country="Inde",
            air_pollution_mortality_score=86.0,
            water_contamination_score=84.0,
            toxic_waste_exposure_score=83.0,
            environmental_justice_gap_score=85.0,
            primary_pattern="air_pollution_mortality_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-004",
            name="Nigeria — Pollution Delta Niger 60 Ans Shell & Eni, Sols Détruits & Communautés Sans Recours Juridique",
            country="Nigeria",
            air_pollution_mortality_score=82.0,
            water_contamination_score=85.0,
            toxic_waste_exposure_score=87.0,
            environmental_justice_gap_score=84.0,
            primary_pattern="toxic_waste_exposure_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-005",
            name="Chine — Rivières Toxiques Métaux Lourds Industrie, Zones Cancers & Villages Empoisonnés Invisibilisés",
            country="Chine",
            air_pollution_mortality_score=54.0,
            water_contamination_score=56.0,
            toxic_waste_exposure_score=57.0,
            environmental_justice_gap_score=55.0,
            primary_pattern="toxic_waste_exposure_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-006",
            name="USA — Flint Water Crisis, Cancer Alley Louisiane & Justice Environnementale Raciale Défaillante",
            country="USA",
            air_pollution_mortality_score=43.0,
            water_contamination_score=45.0,
            toxic_waste_exposure_score=47.0,
            environmental_justice_gap_score=50.0,
            primary_pattern="environmental_justice_gap_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-007",
            name="Pologne — Smog Charbon Hivernal, Maladies Respiratoires Chroniques & Résistance Transition Énergétique",
            country="Pologne",
            air_pollution_mortality_score=30.0,
            water_contamination_score=26.0,
            toxic_waste_exposure_score=28.0,
            environmental_justice_gap_score=27.0,
            primary_pattern="air_pollution_mortality_score",
        ),
        EnvironmentalPollutionRightsEntity(
            entity_id="EPR-008",
            name="Finlande — Air le Plus Pur EU, Eau Potable Universelle & Droits Environnementaux Constitutionnels",
            country="Finlande",
            air_pollution_mortality_score=11.0,
            water_contamination_score=9.0,
            toxic_waste_exposure_score=10.0,
            environmental_justice_gap_score=8.0,
            primary_pattern="air_pollution_mortality_score",
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

    return EnvironmentalPollutionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_pollution_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_ambient_air_quality_database_2024",
            "unep_global_chemicals_outlook_2023",
            "hrw_environmental_pollution_rights_documentation",
            "who_drinking_water_sanitation_hygiene_2023",
            "un_special_rapporteur_toxics_annual_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_environmental_pollution_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
