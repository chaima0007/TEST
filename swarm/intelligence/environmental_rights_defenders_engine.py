from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EnvironmentalRightsDefendersEntity:
    entity_id: str
    name: str
    country: str
    defenders_killed_attacked_score: float
    state_criminal_criminalisation_score: float
    corporate_land_grabbing_impunity_score: float
    climate_justice_indigenous_rights_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_environmental_rights_defenders_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.defenders_killed_attacked_score * 0.30
            + self.state_criminal_criminalisation_score * 0.25
            + self.corporate_land_grabbing_impunity_score * 0.25
            + self.climate_justice_indigenous_rights_score * 0.20,
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
        self.estimated_environmental_rights_defenders_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class EnvironmentalRightsDefendersEngineResult:
    agent: str = "Environmental Rights Defenders Engine Agent"
    domain: str = "environmental_rights_defenders"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_environmental_rights_defenders_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnvironmentalRightsDefendersEntity] = field(default_factory=list)


def run_environmental_rights_defenders_engine() -> EnvironmentalRightsDefendersEngineResult:
    entities = [
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-001",
            name="Honduras — Effet Berta Cáceres, Défenseurs Eau Systématiquement Assassinés, COPINH Persécuté & Impunité Totale Tueurs",
            country="Honduras",
            defenders_killed_attacked_score=95.0,
            state_criminal_criminalisation_score=93.0,
            corporate_land_grabbing_impunity_score=91.0,
            climate_justice_indigenous_rights_score=92.0,
            primary_pattern="defenders_killed_attacked",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-002",
            name="Philippines — Mindanao Défenseurs Miniers Tués, 800+ Activistes Environnement Assassinés & Loi Anti-Terrorisme Instrumentalisée",
            country="Philippines",
            defenders_killed_attacked_score=92.0,
            state_criminal_criminalisation_score=90.0,
            corporate_land_grabbing_impunity_score=88.0,
            climate_justice_indigenous_rights_score=89.0,
            primary_pattern="state_criminal_criminalisation",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-003",
            name="Brésil/Amazonie — Défenseurs Autochtones Tués Héritage Bolsonaro, Dom Phillips Assassiné & Terres Indigènes Déforestées Impunément",
            country="Brésil",
            defenders_killed_attacked_score=90.0,
            state_criminal_criminalisation_score=87.0,
            corporate_land_grabbing_impunity_score=92.0,
            climate_justice_indigenous_rights_score=88.0,
            primary_pattern="corporate_land_grabbing_impunity",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-004",
            name="Cambodge — Défenseurs Forêts Emprisonnés, Mother Nature Cambodia Arrêtée & Concessions Foncières Géantes Complicité État",
            country="Cambodge",
            defenders_killed_attacked_score=85.0,
            state_criminal_criminalisation_score=88.0,
            corporate_land_grabbing_impunity_score=87.0,
            climate_justice_indigenous_rights_score=83.0,
            primary_pattern="state_criminal_criminalisation",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-005",
            name="Mexique — Activistes Eau/Forêts Tués Cartels et État, Impunité 98% Meurtres & Communautés Zapotèques Assiégées",
            country="Mexique",
            defenders_killed_attacked_score=57.0,
            state_criminal_criminalisation_score=55.0,
            corporate_land_grabbing_impunity_score=53.0,
            climate_justice_indigenous_rights_score=56.0,
            primary_pattern="defenders_killed_attacked",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-006",
            name="Colombie — Post-Accord Leaders Environnementaux Tués, 33% Défenseurs Globaux Assassinés 2022 & PDET Non-Implémenté",
            country="Colombie",
            defenders_killed_attacked_score=55.0,
            state_criminal_criminalisation_score=50.0,
            corporate_land_grabbing_impunity_score=52.0,
            climate_justice_indigenous_rights_score=54.0,
            primary_pattern="defenders_killed_attacked",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-007",
            name="Kenya — Ogiek Victoire Partielle Cour Africaine, Défenseurs Fonciers Mau Forest & Litiges Environnementaux en Progrès",
            country="Kenya",
            defenders_killed_attacked_score=28.0,
            state_criminal_criminalisation_score=26.0,
            corporate_land_grabbing_impunity_score=25.0,
            climate_justice_indigenous_rights_score=27.0,
            primary_pattern="climate_justice_indigenous_rights",
        ),
        EnvironmentalRightsDefendersEntity(
            entity_id="ERD-008",
            name="Costa Rica — Modèle Conservation, Droits Verts Constitutionnels, Tribunaux Environnementaux & Défenseurs Protégés par Loi",
            country="Costa Rica",
            defenders_killed_attacked_score=6.0,
            state_criminal_criminalisation_score=5.0,
            corporate_land_grabbing_impunity_score=7.0,
            climate_justice_indigenous_rights_score=5.0,
            primary_pattern="climate_justice_indigenous_rights",
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

    return EnvironmentalRightsDefendersEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_environmental_rights_defenders_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_witness_defenders_killed_2023",
            "front_line_defenders_2023",
            "business_human_rights_resource_centre_env_2023",
            "unhchr_environmental_defenders_2022",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_environmental_rights_defenders_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_environmental_rights_defenders_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
