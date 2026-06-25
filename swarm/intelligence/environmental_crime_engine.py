from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EnvironmentalCrimeEntity:
    entity_id: str
    name: str
    country: str
    ecocide_scale_impunity_score: float
    wildlife_trafficking_networks_score: float
    illegal_extraction_corruption_score: float
    environmental_defender_killings_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_crime_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.ecocide_scale_impunity_score * 0.30
            + self.wildlife_trafficking_networks_score * 0.25
            + self.illegal_extraction_corruption_score * 0.25
            + self.environmental_defender_killings_score * 0.20,
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
        self.estimated_environmental_crime_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EnvironmentalCrimeEngineResult:
    agent: str = "Environmental Crime Engine Agent"
    domain: str = "environmental_crime"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_crime_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalCrimeEntity] = field(default_factory=list)

def run_environmental_crime_engine() -> EnvironmentalCrimeEngineResult:
    entities = [
        EnvironmentalCrimeEntity(
            entity_id="EC-001",
            name="Brésil/Amazonie — Déforestation Illégale 10K km²/an, Garimpeiros & Défenseurs Assassinés",
            country="Amérique Latine",
            ecocide_scale_impunity_score=95.0,
            wildlife_trafficking_networks_score=85.0,
            illegal_extraction_corruption_score=92.0,
            environmental_defender_killings_score=95.0,
            primary_pattern="environmental_defender_killings",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-002",
            name="Afrique/Braconnage — Trafic Ivoire/Rhinocéros, Réseaux Asie & Corruption Gardes Parcs",
            country="Afrique Sub-Saharienne",
            ecocide_scale_impunity_score=85.0,
            wildlife_trafficking_networks_score=95.0,
            illegal_extraction_corruption_score=88.0,
            environmental_defender_killings_score=85.0,
            primary_pattern="wildlife_trafficking_networks",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-003",
            name="Asie SE/Déforestation — Huile Palme Bornéo, Concessions Illégales & Incendies Délibérés",
            country="Asie du Sud-Est",
            ecocide_scale_impunity_score=88.0,
            wildlife_trafficking_networks_score=82.0,
            illegal_extraction_corruption_score=90.0,
            environmental_defender_killings_score=85.0,
            primary_pattern="illegal_extraction_corruption",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-004",
            name="Russie/Arctique — Extraction Pétrole Zone Protégée, Marée Norilsk 2020 & Impunité Norilsk Nickel",
            country="Europe de l'Est",
            ecocide_scale_impunity_score=82.0,
            wildlife_trafficking_networks_score=72.0,
            illegal_extraction_corruption_score=85.0,
            environmental_defender_killings_score=82.0,
            primary_pattern="ecocide_scale_impunity",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-005",
            name="Mexique/Honduras — Défenseurs Terres Assassinés, Cartels Mines Illégales & État Complice",
            country="Amérique Centrale",
            ecocide_scale_impunity_score=55.0,
            wildlife_trafficking_networks_score=52.0,
            illegal_extraction_corruption_score=58.0,
            environmental_defender_killings_score=58.0,
            primary_pattern="environmental_defender_killings",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-006",
            name="UE/Déchets Toxiques — Export Illégal DEEE Afrique, Responsabilité Producteur Insuffisante",
            country="Europe",
            ecocide_scale_impunity_score=48.0,
            wildlife_trafficking_networks_score=50.0,
            illegal_extraction_corruption_score=52.0,
            environmental_defender_killings_score=42.0,
            primary_pattern="illegal_extraction_corruption",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-007",
            name="Global Witness/EIA — Investigation Crimes Environnementaux, Défenseurs & Plaidoyer Écocide",
            country="Global",
            ecocide_scale_impunity_score=22.0,
            wildlife_trafficking_networks_score=25.0,
            illegal_extraction_corruption_score=28.0,
            environmental_defender_killings_score=30.0,
            primary_pattern="ecocide_scale_impunity",
        ),
        EnvironmentalCrimeEntity(
            entity_id="EC-008",
            name="ONU/UNEP — Programme Environnement, Crime Environnemental & Initiative Ecocide CPI Débat",
            country="Global",
            ecocide_scale_impunity_score=4.0,
            wildlife_trafficking_networks_score=5.0,
            illegal_extraction_corruption_score=3.0,
            environmental_defender_killings_score=6.0,
            primary_pattern="wildlife_trafficking_networks",
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

    return EnvironmentalCrimeEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_crime_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_environmental_defenders_killed_annual_report",
            "unodc_world_wildlife_crime_report_trafficking_analysis",
            "interpol_environmental_crime_global_threat_assessment",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_environmental_crime_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_crime_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
