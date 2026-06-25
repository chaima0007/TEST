from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EnvironmentalRightsEntity:
    entity_id: str
    name: str
    country: str
    toxic_pollution_environmental_health_severity_score: float
    indigenous_environmental_destruction_scale_score: float
    environmental_defender_criminalisation_score: float
    state_corporate_environmental_impunity_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.toxic_pollution_environmental_health_severity_score * 0.30
            + self.indigenous_environmental_destruction_scale_score * 0.25
            + self.environmental_defender_criminalisation_score * 0.25
            + self.state_corporate_environmental_impunity_gap_score * 0.20,
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
        self.estimated_environmental_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EnvironmentalRightsEngineResult:
    agent: str = "Environmental Rights Engine Agent"
    domain: str = "environmental_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalRightsEntity] = field(default_factory=list)

def run_environmental_rights_engine() -> EnvironmentalRightsEngineResult:
    entities = [
        EnvironmentalRightsEntity(
            entity_id="ENR-001",
            name="Nigeria/Delta Niger — Déversements Shell 40 Ans, 11M Habitants Pollution, Cancer/Mortalité & Zéro Décontamination",
            country="Nigeria",
            toxic_pollution_environmental_health_severity_score=96.0,
            indigenous_environmental_destruction_scale_score=93.0,
            environmental_defender_criminalisation_score=91.0,
            state_corporate_environmental_impunity_gap_score=94.0,
            primary_pattern="toxic_pollution_environmental_health_severity",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-002",
            name="Inde/Bhopal Legacy — 500 000 Exposés Union Carbide 1984, Eau Contaminée Encore 2024 & Impunité Dow Chemical",
            country="Inde",
            toxic_pollution_environmental_health_severity_score=93.0,
            indigenous_environmental_destruction_scale_score=89.0,
            environmental_defender_criminalisation_score=88.0,
            state_corporate_environmental_impunity_gap_score=91.0,
            primary_pattern="state_corporate_environmental_impunity_gap",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-003",
            name="Amazonie/Brésil — Mercure Garimpos Peuples Yanomami, Déforestation Légalisée Bolsonaro & Défenseurs Assassinés",
            country="Brésil",
            toxic_pollution_environmental_health_severity_score=89.0,
            indigenous_environmental_destruction_scale_score=92.0,
            environmental_defender_criminalisation_score=87.0,
            state_corporate_environmental_impunity_gap_score=85.0,
            primary_pattern="indigenous_environmental_destruction_scale",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-004",
            name="Chine/Régions Industrielles — Smog PM2.5 Shanghai/Beijing, Villages Cancer Henan & Protestations Environnementales Réprimées",
            country="Chine",
            toxic_pollution_environmental_health_severity_score=87.0,
            indigenous_environmental_destruction_scale_score=82.0,
            environmental_defender_criminalisation_score=85.0,
            state_corporate_environmental_impunity_gap_score=84.0,
            primary_pattern="toxic_pollution_environmental_health_severity",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-005",
            name="Philippines — 800 Défenseurs Environnement Tués Depuis 2010, Mines Ouvertes & Lois Anti-Activisme",
            country="Philippines",
            toxic_pollution_environmental_health_severity_score=54.0,
            indigenous_environmental_destruction_scale_score=56.0,
            environmental_defender_criminalisation_score=58.0,
            state_corporate_environmental_impunity_gap_score=50.0,
            primary_pattern="environmental_defender_criminalisation",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-006",
            name="Mexique/Amérique Centrale — Défenseurs Eau/Forêts Assassinés Cartels+État, Impunité 98% & Communautés Isolées",
            country="Mexique",
            toxic_pollution_environmental_health_severity_score=52.0,
            indigenous_environmental_destruction_scale_score=53.0,
            environmental_defender_criminalisation_score=55.0,
            state_corporate_environmental_impunity_gap_score=48.0,
            primary_pattern="environmental_defender_criminalisation",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-007",
            name="Global Witness/AIDA — Rapport Défenseurs Environnement, Litiges Climatiques & Droit Environnement Sain ONU",
            country="Global",
            toxic_pollution_environmental_health_severity_score=26.0,
            indigenous_environmental_destruction_scale_score=28.0,
            environmental_defender_criminalisation_score=25.0,
            state_corporate_environmental_impunity_gap_score=27.0,
            primary_pattern="indigenous_environmental_destruction_scale",
        ),
        EnvironmentalRightsEntity(
            entity_id="ENR-008",
            name="ONU/Résolution 76/300 — Droit Environnement Sain Reconnaissance 2022, Rapporteur & SDG 15 Vie Terrestre",
            country="Global",
            toxic_pollution_environmental_health_severity_score=4.0,
            indigenous_environmental_destruction_scale_score=4.0,
            environmental_defender_criminalisation_score=5.0,
            state_corporate_environmental_impunity_gap_score=4.0,
            primary_pattern="environmental_defender_criminalisation",
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

    return EnvironmentalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_defenders_environmental_rights_report",
            "unep_state_of_environment_report",
            "amnesty_international_corporate_environmental_impunity",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_environmental_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
