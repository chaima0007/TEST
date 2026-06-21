from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class DeforestationIndigenousRightsEntity:
    entity_id: str
    name: str
    country: str
    deforestation_rate_territorial_loss_score: float
    indigenous_land_rights_violation_score: float
    criminalisation_defenders_impunity_score: float
    legal_protection_enforcement_deficit_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_deforestation_indigenous_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.deforestation_rate_territorial_loss_score * 0.30
            + self.indigenous_land_rights_violation_score * 0.25
            + self.criminalisation_defenders_impunity_score * 0.25
            + self.legal_protection_enforcement_deficit_score * 0.20,
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
        self.estimated_deforestation_indigenous_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class DeforestationIndigenousRightsEngineResult:
    agent: str = "Deforestation Indigenous Rights Engine Agent"
    domain: str = "deforestation_indigenous_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_deforestation_indigenous_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DeforestationIndigenousRightsEntity] = field(default_factory=list)


def run_deforestation_indigenous_rights_engine() -> DeforestationIndigenousRightsEngineResult:
    entities = [
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-001",
            name="Brésil/Amazonie Bolsonaro Héritage — 11 568 km² Déforestés 2022, FUNAI Démantelé, 160+ Peuples Non-Contactés Menacés & Assassinat Leonardo Guajajara",
            country="Brésil",
            deforestation_rate_territorial_loss_score=94.0,
            indigenous_land_rights_violation_score=92.0,
            criminalisation_defenders_impunity_score=91.0,
            legal_protection_enforcement_deficit_score=89.0,
            primary_pattern="deforestation_rate_territorial_loss",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-002",
            name="RDC/Bassin Congo — 500 000 ha/an Déforestés, Peuples Pygmées Batwa Expulsés Parcs Nationaux, Exploitation Illégale & Zéro Consultation CLIP",
            country="RDC",
            deforestation_rate_territorial_loss_score=89.0,
            indigenous_land_rights_violation_score=88.0,
            criminalisation_defenders_impunity_score=87.0,
            legal_protection_enforcement_deficit_score=90.0,
            primary_pattern="legal_protection_enforcement_deficit",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-003",
            name="Indonésie/Papouasie Occidentale — Huile Palme 3,5M ha Concessions, Peuples Marind & Awyu Expulsés, Défenseurs Emprisonnés & Armée Déployée",
            country="Indonésie",
            deforestation_rate_territorial_loss_score=86.0,
            indigenous_land_rights_violation_score=87.0,
            criminalisation_defenders_impunity_score=85.0,
            legal_protection_enforcement_deficit_score=84.0,
            primary_pattern="indigenous_land_rights_violation",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-004",
            name="Pérou/Amazonie Minière — 1 500 Communautés Sans Titre Foncier, Extraction Or Illégale Madre de Dios, 30 Défenseurs Tués 2020-2024 & Narco-Déforestation",
            country="Pérou",
            deforestation_rate_territorial_loss_score=80.0,
            indigenous_land_rights_violation_score=82.0,
            criminalisation_defenders_impunity_score=83.0,
            legal_protection_enforcement_deficit_score=78.0,
            primary_pattern="criminalisation_defenders_impunity",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-005",
            name="Honduras/Lenca Mesoamérique — 11 Défenseurs Tués/100k Habitants Taux Mondial, Assassinat Berta Cáceres Impuni, Concessions Forestières Illégales & Criminalisation ONG",
            country="Honduras",
            deforestation_rate_territorial_loss_score=58.0,
            indigenous_land_rights_violation_score=62.0,
            criminalisation_defenders_impunity_score=65.0,
            legal_protection_enforcement_deficit_score=60.0,
            primary_pattern="criminalisation_defenders_impunity",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-006",
            name="Myanmar/Karen Kayah — Déforestation Post-Coup 2021 Accélérée, Peuples Karen Bombardés Réfugiés Frontière, Teck & Charbon Exploités Armée",
            country="Myanmar",
            deforestation_rate_territorial_loss_score=55.0,
            indigenous_land_rights_violation_score=57.0,
            criminalisation_defenders_impunity_score=58.0,
            legal_protection_enforcement_deficit_score=56.0,
            primary_pattern="deforestation_rate_territorial_loss",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-007",
            name="Canada/First Nations Boréale — Pipelines Trans Mountain Contestés Wet'suwet'en, Logging 200+ Ans Territoire Non-Cédé, FPIC Partiel & Réconciliation Lente",
            country="Canada",
            deforestation_rate_territorial_loss_score=28.0,
            indigenous_land_rights_violation_score=32.0,
            criminalisation_defenders_impunity_score=25.0,
            legal_protection_enforcement_deficit_score=30.0,
            primary_pattern="indigenous_land_rights_violation",
        ),
        DeforestationIndigenousRightsEntity(
            entity_id="DIR-008",
            name="UE/EUDR Régulation Déforestation — Règlement 2023/1115 Import Zéro-Déforestation, Due Diligence Obligatoire, Géolocalisation Parcelles & Sanctions 4% CA",
            country="Union Européenne",
            deforestation_rate_territorial_loss_score=7.0,
            indigenous_land_rights_violation_score=8.0,
            criminalisation_defenders_impunity_score=6.0,
            legal_protection_enforcement_deficit_score=9.0,
            primary_pattern="legal_protection_enforcement_deficit",
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

    return DeforestationIndigenousRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_deforestation_indigenous_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "global_forest_watch_deforestation_monitoring_2024",
            "global_witness_land_defenders_annual_report",
            "cultural_survival_indigenous_rights_database",
            "ipbes_biodiversity_land_use_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_deforestation_indigenous_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_deforestation_indigenous_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
