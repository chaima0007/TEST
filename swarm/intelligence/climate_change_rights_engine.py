from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#10b981"


@dataclass
class ClimateChangeRightsEntity:
    entity_id: str
    name: str
    country: str
    climate_vulnerability_score: float
    climate_adaptation_failure_score: float
    fossil_fuel_harm_score: float
    climate_justice_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_climate_change_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.climate_vulnerability_score * 0.30
            + self.climate_adaptation_failure_score * 0.25
            + self.fossil_fuel_harm_score * 0.25
            + self.climate_justice_gap_score * 0.20,
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
        self.estimated_climate_change_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ClimateChangeRightsEngineResult:
    agent: str = "Climate Change Rights Engine Agent"
    domain: str = "climate_change_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_climate_change_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ClimateChangeRightsEntity] = field(default_factory=list)


def run_climate_change_rights_engine() -> ClimateChangeRightsEngineResult:
    entities = [
        ClimateChangeRightsEntity(
            entity_id="CCR-001",
            name="Îles Marshall — Submersion Imminente du Territoire National, Droit à l'Existence Menacé par la Montée des Eaux",
            country="Îles Marshall",
            climate_vulnerability_score=95.0,
            climate_adaptation_failure_score=88.0,
            fossil_fuel_harm_score=82.0,
            climate_justice_gap_score=91.0,
            primary_pattern="climate_vulnerability_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-002",
            name="Bangladesh — Inondations Chroniques Exposant 40 Millions de Personnes, Déplacements Climatiques Massifs",
            country="Bangladesh",
            climate_vulnerability_score=91.0,
            climate_adaptation_failure_score=85.0,
            fossil_fuel_harm_score=80.0,
            climate_justice_gap_score=88.0,
            primary_pattern="climate_vulnerability_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-003",
            name="Mozambique — Cyclones Idai et Kenneth, Génocide Climatique Documenté, 3 Millions de Personnes Touchées",
            country="Mozambique",
            climate_vulnerability_score=88.0,
            climate_adaptation_failure_score=87.0,
            fossil_fuel_harm_score=83.0,
            climate_justice_gap_score=89.0,
            primary_pattern="climate_justice_gap_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-004",
            name="Pakistan — Inondations 2022, 33 Millions de Personnes Touchées, Un Tiers du Territoire Submergé",
            country="Pakistan",
            climate_vulnerability_score=89.0,
            climate_adaptation_failure_score=86.0,
            fossil_fuel_harm_score=81.0,
            climate_justice_gap_score=87.0,
            primary_pattern="climate_vulnerability_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-005",
            name="Inde — Vagues de Chaleur Mortelles Répétées, 600 Millions de Personnes en Stress Hydrique Sévère",
            country="Inde",
            climate_vulnerability_score=55.0,
            climate_adaptation_failure_score=50.0,
            fossil_fuel_harm_score=52.0,
            climate_justice_gap_score=53.0,
            primary_pattern="climate_vulnerability_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-006",
            name="Nigéria — Désertification du Nord, Sécheresse Sahélienne & Conflits Agropastoraux Liés au Changement Climatique",
            country="Nigéria",
            climate_vulnerability_score=48.0,
            climate_adaptation_failure_score=50.0,
            fossil_fuel_harm_score=55.0,
            climate_justice_gap_score=51.0,
            primary_pattern="fossil_fuel_harm_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-007",
            name="USA — Racisme Climatique Ouragan Katrina, Réponse Inadéquate Puerto Rico & Inégalités Environnementales Documentées",
            country="USA",
            climate_vulnerability_score=28.0,
            climate_adaptation_failure_score=30.0,
            fossil_fuel_harm_score=35.0,
            climate_justice_gap_score=32.0,
            primary_pattern="fossil_fuel_harm_score",
        ),
        ClimateChangeRightsEntity(
            entity_id="CCR-008",
            name="Costa Rica — 100% Énergie Renouvelable, Zéro Émission Nette 2050 & Leader Mondial de la Justice Climatique",
            country="Costa Rica",
            climate_vulnerability_score=10.0,
            climate_adaptation_failure_score=9.0,
            fossil_fuel_harm_score=8.0,
            climate_justice_gap_score=11.0,
            primary_pattern="climate_vulnerability_score",
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

    return ClimateChangeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_climate_change_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ipcc_sixth_assessment_report_2023",
            "un_special_rapporteur_human_rights_environment_2024",
            "hrw_climate_crisis_human_rights_2023",
            "ohchr_climate_change_human_rights_analytical_study",
            "climate_vulnerability_index_germanwatch_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_climate_change_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
