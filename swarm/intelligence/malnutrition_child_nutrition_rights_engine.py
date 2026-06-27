from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MalnutritionChildNutritionRightsEntity:
    entity_id: str
    name: str
    country: str
    acute_malnutrition_stunting_prevalence_score: float
    food_insecurity_famine_risk_score: float
    healthcare_nutrition_services_access_deficit_score: float
    political_will_funding_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_malnutrition_child_nutrition_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.acute_malnutrition_stunting_prevalence_score * 0.30
            + self.food_insecurity_famine_risk_score * 0.25
            + self.healthcare_nutrition_services_access_deficit_score * 0.25
            + self.political_will_funding_accountability_gap_score * 0.20,
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
        self.estimated_malnutrition_child_nutrition_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MalnutritionChildNutritionRightsEngineResult:
    agent: str = "Malnutrition Child Nutrition Rights Engine Agent"
    domain: str = "malnutrition_child_nutrition_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_malnutrition_child_nutrition_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MalnutritionChildNutritionRightsEntity] = field(default_factory=list)


def run_malnutrition_child_nutrition_rights_engine() -> MalnutritionChildNutritionRightsEngineResult:
    entities = [
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-001",
            name="Yémen/Famine Guerre — 2,2M Enfants Malnutrition Aiguë Sévère, 540 000 Kwashiorkor Stade Famine, Blocus Ports Hudaydah & 80% Population Aide Humanitaire",
            country="Yémen",
            acute_malnutrition_stunting_prevalence_score=96.0,
            food_insecurity_famine_risk_score=95.0,
            healthcare_nutrition_services_access_deficit_score=94.0,
            political_will_funding_accountability_gap_score=93.0,
            primary_pattern="acute_malnutrition_stunting_prevalence",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-002",
            name="Soudan/Darfour Katastrophe — 3,5M Enfants Malnutrition Aiguë, Famine IPC Phase 5 Nord Darfour 2024, MSF Cliniques Bombardées & 730 000 Déplacés Camps",
            country="Soudan",
            acute_malnutrition_stunting_prevalence_score=92.0,
            food_insecurity_famine_risk_score=94.0,
            healthcare_nutrition_services_access_deficit_score=91.0,
            political_will_funding_accountability_gap_score=92.0,
            primary_pattern="food_insecurity_famine_risk",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-003",
            name="Somalia/Sécheresse Cyclique — 1,8M Enfants GAM >15%, Sécheresses Consécutives 2022-2024 El Niño, Al-Shabaab Blocage Aide & 760 000 Réfugiés Internes",
            country="Somalia",
            acute_malnutrition_stunting_prevalence_score=88.0,
            food_insecurity_famine_risk_score=90.0,
            healthcare_nutrition_services_access_deficit_score=89.0,
            political_will_funding_accountability_gap_score=87.0,
            primary_pattern="food_insecurity_famine_risk",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-004",
            name="Niger/Sahel Structural — 67% Enfants <5 Retard Croissance, Malnutrition Chronique Endémique, Coup 2023 Suspension Aide & Budget Nutrition 1,2% PIB",
            country="Niger",
            acute_malnutrition_stunting_prevalence_score=83.0,
            food_insecurity_famine_risk_score=81.0,
            healthcare_nutrition_services_access_deficit_score=85.0,
            political_will_funding_accountability_gap_score=86.0,
            primary_pattern="political_will_funding_accountability_gap",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-005",
            name="Inde/Bihar Paradoxe — 48% Stunting Bihar État, 1er Producteur Alimentaire Mondial & 3ème Malnutrition, Inégalités Castes Dalits Sans Accès Rations",
            country="Inde",
            acute_malnutrition_stunting_prevalence_score=58.0,
            food_insecurity_famine_risk_score=52.0,
            healthcare_nutrition_services_access_deficit_score=55.0,
            political_will_funding_accountability_gap_score=54.0,
            primary_pattern="acute_malnutrition_stunting_prevalence",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-006",
            name="Guatemala/Corridor Sec — 46,5% Stunting Maya K'iche' Zones Rurales, Canicule Corridor Sec Récoltes Perdues, Terres Haciendas & Sans Accès Eau Potable",
            country="Guatemala",
            acute_malnutrition_stunting_prevalence_score=54.0,
            food_insecurity_famine_risk_score=50.0,
            healthcare_nutrition_services_access_deficit_score=52.0,
            political_will_funding_accountability_gap_score=56.0,
            primary_pattern="political_will_funding_accountability_gap",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-007",
            name="Brésil/Yanomami Crise 2023 — 570 Enfants Yanomami Malnutrition Sévère, Garimpeiros Mercure Rivières, Lula Urgence Sanitaire & Reconstruction Services",
            country="Brésil",
            acute_malnutrition_stunting_prevalence_score=29.0,
            food_insecurity_famine_risk_score=32.0,
            healthcare_nutrition_services_access_deficit_score=35.0,
            political_will_funding_accountability_gap_score=28.0,
            primary_pattern="healthcare_nutrition_services_access_deficit",
        ),
        MalnutritionChildNutritionRightsEntity(
            entity_id="MCN-008",
            name="Suède/Alimentation Scolaire Modèle — 100% Enfants Repas Scolaires Gratuits, EFSA Normes Nutritionnelles, Budget 350€/Enfant/An & Score Faim GHI 5.0",
            country="Suède",
            acute_malnutrition_stunting_prevalence_score=4.0,
            food_insecurity_famine_risk_score=3.0,
            healthcare_nutrition_services_access_deficit_score=4.0,
            political_will_funding_accountability_gap_score=5.0,
            primary_pattern="acute_malnutrition_stunting_prevalence",
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

    return MalnutritionChildNutritionRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_malnutrition_child_nutrition_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_global_nutrition_report_2024",
            "wfp_food_security_ipc_analysis",
            "who_global_child_malnutrition_joint_estimates",
            "ifpri_global_hunger_index_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_malnutrition_child_nutrition_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_malnutrition_child_nutrition_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
