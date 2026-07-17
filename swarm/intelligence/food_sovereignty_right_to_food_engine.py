"""Food Sovereignty Right to Food Engine — FAO SOFI 2023, WFP & Rapporteur ONU Droit à l'Alimentation."""

from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class FoodSovereigntyRightToFoodEntity:
    entity_id: str
    name: str
    country: str
    food_insecurity_famine_severity_score: float
    right_to_food_legal_protection_gap_score: float
    food_system_collapse_conflict_score: float
    structural_hunger_exclusion_score: float
    primary_pattern: str = ""
    last_updated: str = "2026-06-21"

    @property
    def composite_score(self) -> float:
        return round(
            self.food_insecurity_famine_severity_score * 0.30
            + self.right_to_food_legal_protection_gap_score * 0.25
            + self.food_system_collapse_conflict_score * 0.25
            + self.structural_hunger_exclusion_score * 0.20,
            2,
        )

    @property
    def risk_level(self) -> str:
        s = self.composite_score
        if s >= 60:
            return "critique"
        if s >= 40:
            return "élevé"
        if s >= 20:
            return "modéré"
        return "faible"

    @property
    def estimated_food_sovereignty_right_to_food_index(self) -> float:
        return round(self.composite_score / 100 * 10, 2)

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "name": self.name,
            "country": self.country,
            "composite_score": self.composite_score,
            "food_insecurity_famine_severity_score": self.food_insecurity_famine_severity_score,
            "right_to_food_legal_protection_gap_score": self.right_to_food_legal_protection_gap_score,
            "food_system_collapse_conflict_score": self.food_system_collapse_conflict_score,
            "structural_hunger_exclusion_score": self.structural_hunger_exclusion_score,
            "risk_level": self.risk_level,
            "primary_pattern": self.primary_pattern,
            "estimated_food_sovereignty_right_to_food_index": self.estimated_food_sovereignty_right_to_food_index,
            "last_updated": self.last_updated,
        }


@dataclass
class FoodSovereigntyRightToFoodEngineResult:
    agent: str = "Food Sovereignty Right to Food Engine Agent"
    domain: str = "food_sovereignty_right_to_food"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_food_sovereignty_right_to_food_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FoodSovereigntyRightToFoodEntity] = field(default_factory=list)


def run_food_sovereignty_right_to_food_engine() -> FoodSovereigntyRightToFoodEngineResult:
    entities = [
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-001",
            name="Yémen/Famine IPC5 — 21M en Insécurité Alimentaire, 160K Phase Catastrophe IPC5, Blocus Ports & Destruction Infrastructure Agricole par Coalition",
            country="Yémen",
            food_insecurity_famine_severity_score=95.0,
            right_to_food_legal_protection_gap_score=90.0,
            food_system_collapse_conflict_score=92.0,
            structural_hunger_exclusion_score=88.0,
            primary_pattern="food_insecurity_famine_severity",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-002",
            name="Somalie/Sécheresse & Al-Shabaab — Famine Récurrente, 6.5M en Crise Alimentaire, Sécheresses La Niña Cumulées & Insécurité Al-Shabaab Bloquant Aide Humanitaire",
            country="Somalie",
            food_insecurity_famine_severity_score=90.0,
            right_to_food_legal_protection_gap_score=85.0,
            food_system_collapse_conflict_score=88.0,
            structural_hunger_exclusion_score=82.0,
            primary_pattern="food_system_collapse_conflict",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-003",
            name="Éthiopie/Tigré — Famine Arme de Guerre, 900K Phase Urgence, Siège Militaire Tigré & Destruction Cultures par Forces Armées Documentée ONU",
            country="Éthiopie",
            food_insecurity_famine_severity_score=88.0,
            right_to_food_legal_protection_gap_score=82.0,
            food_system_collapse_conflict_score=90.0,
            structural_hunger_exclusion_score=80.0,
            primary_pattern="food_system_collapse_conflict",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-004",
            name="Haïti/Crise Alimentaire & Gangs — 5.2M en Insécurité Alimentaire Aigüe, Contrôle Gangs 85% Port-au-Prince, Effondrement Agriculture & Blocage Aide",
            country="Haïti",
            food_insecurity_famine_severity_score=85.0,
            right_to_food_legal_protection_gap_score=80.0,
            food_system_collapse_conflict_score=82.0,
            structural_hunger_exclusion_score=78.0,
            primary_pattern="food_insecurity_famine_severity",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-005",
            name="RCA/Conflit & 2.5M Déplacés — République Centrafricaine, 2.5M Déplacés Affamés, Groupes Armés Pillant Ressources Alimentaires & Effondrement Services Agricoles",
            country="République Centrafricaine",
            food_insecurity_famine_severity_score=58.0,
            right_to_food_legal_protection_gap_score=52.0,
            food_system_collapse_conflict_score=55.0,
            structural_hunger_exclusion_score=50.0,
            primary_pattern="structural_hunger_exclusion",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-006",
            name="Madagascar/Sécheresse Sud Kere — 1.3M Personnes Phase Crise-Urgence, Sécheresse Sud Grand-Sud Exceptionnelle, Kere (Famine Traditionnelle) & Malnutrition Enfants 20%",
            country="Madagascar",
            food_insecurity_famine_severity_score=60.0,
            right_to_food_legal_protection_gap_score=55.0,
            food_system_collapse_conflict_score=58.0,
            structural_hunger_exclusion_score=62.0,
            primary_pattern="structural_hunger_exclusion",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-007",
            name="Venezuela/Effondrement Économique — Hyperinflation 2019-2023, 7.7M en Insécurité Alimentaire Modérée-Sévère, Pénuries Chroniques & Émigration 7.7M Réfugiés",
            country="Venezuela",
            food_insecurity_famine_severity_score=40.0,
            right_to_food_legal_protection_gap_score=38.0,
            food_system_collapse_conflict_score=35.0,
            structural_hunger_exclusion_score=42.0,
            primary_pattern="right_to_food_legal_protection_gap",
        ),
        FoodSovereigntyRightToFoodEntity(
            entity_id="FSRF-008",
            name="Brésil/Fome Zero 2.0 Lula — Programme Bolsa Família Relancé, 33M Sortis Faim Sous Lula 2023, Politique Alimentaire Nationale & Droit Constitutionnel à l'Alimentation",
            country="Brésil",
            food_insecurity_famine_severity_score=8.0,
            right_to_food_legal_protection_gap_score=12.0,
            food_system_collapse_conflict_score=6.0,
            structural_hunger_exclusion_score=15.0,
            primary_pattern="right_to_food_legal_protection_gap",
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

    return FoodSovereigntyRightToFoodEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_food_sovereignty_right_to_food_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_sofi_2023",
            "wfp_global_report_food_crises_2023",
            "un_sr_right_to_food_2023",
            "ihh_humanitarian_right_food_2022",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_food_sovereignty_right_to_food_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_food_sovereignty_right_to_food_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
