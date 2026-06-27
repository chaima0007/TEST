from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#15803d"


@dataclass
class RightToFoodRightsEntity:
    entity_id: str
    name: str
    country: str
    acute_food_insecurity_score: float
    food_as_weapon_score: float
    agricultural_displacement_score: float
    structural_hunger_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_food_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.acute_food_insecurity_score * 0.30
            + self.food_as_weapon_score * 0.25
            + self.agricultural_displacement_score * 0.25
            + self.structural_hunger_score * 0.20,
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
        self.estimated_right_to_food_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToFoodRightsEngineResult:
    agent: str = "Right To Food Rights Engine Agent"
    domain: str = "right_to_food_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_food_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToFoodRightsEntity] = field(default_factory=list)


def run_right_to_food_rights_engine() -> RightToFoodRightsEngineResult:
    entities = [
        RightToFoodRightsEntity(
            entity_id="RTF-001",
            name="Yémen — 21M en insécurité alimentaire, blocus Hodeida, famine ONU niveau 5",
            country="Yémen",
            acute_food_insecurity_score=97.0,
            food_as_weapon_score=96.0,
            agricultural_displacement_score=94.0,
            structural_hunger_score=95.0,
            primary_pattern="food_as_weapon",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-002",
            name="Soudan/Darfour — Génocide alimentaire RSF, 25M en famine aiguë, IPC Phase 5",
            country="Soudan",
            acute_food_insecurity_score=91.0,
            food_as_weapon_score=93.0,
            agricultural_displacement_score=89.0,
            structural_hunger_score=90.0,
            primary_pattern="food_as_weapon",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-003",
            name="RDC — 28M en insécurité sévère, Est pillé, enfants malnutrition chronique 45%",
            country="RDC",
            acute_food_insecurity_score=85.0,
            food_as_weapon_score=83.0,
            agricultural_displacement_score=87.0,
            structural_hunger_score=84.0,
            primary_pattern="agricultural_displacement",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-004",
            name="Éthiopie/Tigray — Siège alimentaire ENDF/Érythrée, 900k famine, ONG expulsées",
            country="Éthiopie",
            acute_food_insecurity_score=77.0,
            food_as_weapon_score=79.0,
            agricultural_displacement_score=75.0,
            structural_hunger_score=76.0,
            primary_pattern="food_as_weapon",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-005",
            name="Haïti — 5M en insécurité aiguë, gangs bloquent aide, 115k Phase 5 catastrophe",
            country="Haïti",
            acute_food_insecurity_score=56.0,
            food_as_weapon_score=54.0,
            agricultural_displacement_score=52.0,
            structural_hunger_score=58.0,
            primary_pattern="acute_food_insecurity",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-006",
            name="Afghanistan — 15M sans sécurité alimentaire, femmes exclues aide ONG, Taliban",
            country="Afghanistan",
            acute_food_insecurity_score=46.0,
            food_as_weapon_score=50.0,
            agricultural_displacement_score=44.0,
            structural_hunger_score=48.0,
            primary_pattern="structural_hunger",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-007",
            name="USA — 44M en insécurité alimentaire, SNAP insuffisant, déserts alimentaires",
            country="USA",
            acute_food_insecurity_score=28.0,
            food_as_weapon_score=22.0,
            agricultural_displacement_score=26.0,
            structural_hunger_score=30.0,
            primary_pattern="structural_hunger",
        ),
        RightToFoodRightsEntity(
            entity_id="RTF-008",
            name="France/Brésil — Fome Zero modèle, aide alimentaire légalement garantie, PAA",
            country="France/Brésil",
            acute_food_insecurity_score=7.0,
            food_as_weapon_score=5.0,
            agricultural_displacement_score=8.0,
            structural_hunger_score=6.0,
            primary_pattern="acute_food_insecurity",
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

    return RightToFoodRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_food_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_state_food_security_nutrition_world_2024",
            "wfp_global_food_crisis_report_2024",
            "hrw_food_rights_violations_global",
            "fian_international_right_food_violations",
            "oxfam_hunger_inequality_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_food_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
