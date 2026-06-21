from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FoodSovereigntyFamineRightsEntity:
    entity_id: str
    name: str
    country: str
    famine_food_insecurity_severity_score: float
    food_weaponization_siege_blockade_score: float
    smallholder_land_seed_rights_violation_score: float
    food_aid_obstruction_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_food_sovereignty_famine_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.famine_food_insecurity_severity_score * 0.30
            + self.food_weaponization_siege_blockade_score * 0.25
            + self.smallholder_land_seed_rights_violation_score * 0.25
            + self.food_aid_obstruction_accountability_gap_score * 0.20,
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
        self.estimated_food_sovereignty_famine_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class FoodSovereigntyFamineRightsEngineResult:
    agent: str = "Food Sovereignty Famine Rights Engine Agent"
    domain: str = "food_sovereignty_famine_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_food_sovereignty_famine_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FoodSovereigntyFamineRightsEntity] = field(default_factory=list)


def run_food_sovereignty_famine_rights_engine() -> FoodSovereigntyFamineRightsEngineResult:
    entities = [
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-001",
            name="Yémen/Siège Houthis — Blocus Portuaire Hodeidah, Famine IPC Phase 5, Destruction Agriculture & Obstruction Aide Humanitaire",
            country="Yémen",
            famine_food_insecurity_severity_score=92.0,
            food_weaponization_siege_blockade_score=90.0,
            smallholder_land_seed_rights_violation_score=75.0,
            food_aid_obstruction_accountability_gap_score=88.0,
            primary_pattern="food_weaponization_siege_blockade",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-002",
            name="Soudan/RSF Famine — Pillage Greniers Villages, Destruction Marchés, Déplacement Agriculteurs Darfour & Blocage Convois ONG",
            country="Soudan",
            famine_food_insecurity_severity_score=90.0,
            food_weaponization_siege_blockade_score=88.0,
            smallholder_land_seed_rights_violation_score=72.0,
            food_aid_obstruction_accountability_gap_score=85.0,
            primary_pattern="famine_food_insecurity_severity",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-003",
            name="Éthiopie/Tigré Blocus — Siège Total Région, Destruction Récoltes Armée, Famine Délibérée & Expulsion Agences ONU",
            country="Éthiopie",
            famine_food_insecurity_severity_score=85.0,
            food_weaponization_siege_blockade_score=82.0,
            smallholder_land_seed_rights_violation_score=78.0,
            food_aid_obstruction_accountability_gap_score=80.0,
            primary_pattern="food_weaponization_siege_blockade",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-004",
            name="Afghanistan/Talibans Aide Bloquée — Exclusion Femmes ONG, Gel Avoirs Bancaires Bloquant Importations, Sécheresse & Famine Systémique",
            country="Afghanistan",
            famine_food_insecurity_severity_score=80.0,
            food_weaponization_siege_blockade_score=78.0,
            smallholder_land_seed_rights_violation_score=82.0,
            food_aid_obstruction_accountability_gap_score=75.0,
            primary_pattern="smallholder_land_seed_rights_violation",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-005",
            name="Haïti/Gangs Bloquent Distribution — Contrôle Routes Alimentaires par Gangs, Insécurité Alimentaire Urbaine & Effondrement Système Agricole",
            country="Haïti",
            famine_food_insecurity_severity_score=60.0,
            food_weaponization_siege_blockade_score=58.0,
            smallholder_land_seed_rights_violation_score=55.0,
            food_aid_obstruction_accountability_gap_score=52.0,
            primary_pattern="famine_food_insecurity_severity",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-006",
            name="RCA/Pillage Agricole — Groupes Armés Volant Récoltes, Déplacement Paysans, Accaparement Terres & Impunité Totale",
            country="République Centrafricaine",
            famine_food_insecurity_severity_score=55.0,
            food_weaponization_siege_blockade_score=52.0,
            smallholder_land_seed_rights_violation_score=58.0,
            food_aid_obstruction_accountability_gap_score=48.0,
            primary_pattern="smallholder_land_seed_rights_violation",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-007",
            name="Venezuela/Restrictions Importations — Contrôle des Changes Bloquant Importations Alimentaires, Hyperinflation & Exode Agriculteurs",
            country="Venezuela",
            famine_food_insecurity_severity_score=30.0,
            food_weaponization_siege_blockade_score=25.0,
            smallholder_land_seed_rights_violation_score=35.0,
            food_aid_obstruction_accountability_gap_score=28.0,
            primary_pattern="smallholder_land_seed_rights_violation",
        ),
        FoodSovereigntyFamineRightsEntity(
            entity_id="FSFR-008",
            name="Brésil/Bolsa Família Modèle — Programme Transferts Conditionnels Alimentaires, Réduction Faim & Référence Mondiale Sécurité Alimentaire",
            country="Brésil",
            famine_food_insecurity_severity_score=5.0,
            food_weaponization_siege_blockade_score=4.0,
            smallholder_land_seed_rights_violation_score=8.0,
            food_aid_obstruction_accountability_gap_score=6.0,
            primary_pattern="famine_food_insecurity_severity",
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

    return FoodSovereigntyFamineRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_food_sovereignty_famine_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_hunger_map_2023",
            "ipc_acute_food_insecurity_analysis_2023",
            "grain_land_grabbing_database_2023",
            "oxfam_food_rights_violations_report_2023",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_food_sovereignty_famine_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_food_sovereignty_famine_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
