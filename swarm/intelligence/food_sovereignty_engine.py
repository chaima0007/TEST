from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class FoodSovereigntyEntity:
    entity_id: str
    name: str
    country: str
    seed_patent_monopoly_score: float
    agribusiness_market_control_score: float
    small_farmer_displacement_score: float
    traditional_knowledge_erasure_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_food_sovereignty_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.seed_patent_monopoly_score * 0.30
            + self.agribusiness_market_control_score * 0.25
            + self.small_farmer_displacement_score * 0.25
            + self.traditional_knowledge_erasure_score * 0.20,
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
        self.estimated_food_sovereignty_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class FoodSovereigntyEngineResult:
    agent: str = "Food Sovereignty Engine Agent"
    domain: str = "food_sovereignty"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_food_sovereignty_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FoodSovereigntyEntity] = field(default_factory=list)

def run_food_sovereignty_engine() -> FoodSovereigntyEngineResult:
    entities = [
        FoodSovereigntyEntity(
            entity_id="FS-001",
            name="Inde/Asie du Sud — Brevets Semences Monsanto/Bayer, Suicides Agriculteurs & Dépendance GMO",
            country="Asie du Sud",
            seed_patent_monopoly_score=92.0,
            agribusiness_market_control_score=88.0,
            small_farmer_displacement_score=90.0,
            traditional_knowledge_erasure_score=85.0,
            primary_pattern="seed_patent_monopoly",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-002",
            name="Afrique/Sahel — Alliance pour la Révolution Verte (AGRA), Semences Hybrides & Dépendance Intrants",
            country="Afrique Sub-Saharienne",
            seed_patent_monopoly_score=85.0,
            agribusiness_market_control_score=90.0,
            small_farmer_displacement_score=88.0,
            traditional_knowledge_erasure_score=82.0,
            primary_pattern="agribusiness_market_control",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-003",
            name="USA — Oligopole Semencier Bayer-Corteva-Syngenta, Lobbying TRIPS & Brevet Vivant",
            country="Amérique du Nord",
            seed_patent_monopoly_score=88.0,
            agribusiness_market_control_score=92.0,
            small_farmer_displacement_score=78.0,
            traditional_knowledge_erasure_score=75.0,
            primary_pattern="agribusiness_market_control",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-004",
            name="Brésil — Déforestation Amazonie pour Soja, Latifundias & Criminalisation MST",
            country="Amérique Latine",
            seed_patent_monopoly_score=72.0,
            agribusiness_market_control_score=80.0,
            small_farmer_displacement_score=78.0,
            traditional_knowledge_erasure_score=75.0,
            primary_pattern="small_farmer_displacement",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-005",
            name="Europe/PAC — Subventions Agro-Industrielles, Baisse Exploitations Familiales & Normes GMO",
            country="Europe",
            seed_patent_monopoly_score=52.0,
            agribusiness_market_control_score=55.0,
            small_farmer_displacement_score=58.0,
            traditional_knowledge_erasure_score=50.0,
            primary_pattern="small_farmer_displacement",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-006",
            name="Chine — Concentration Agraire, Disparition Variétés Locales & Contrôle Étatique Semences",
            country="Asie du Nord-Est",
            seed_patent_monopoly_score=48.0,
            agribusiness_market_control_score=52.0,
            small_farmer_displacement_score=55.0,
            traditional_knowledge_erasure_score=50.0,
            primary_pattern="traditional_knowledge_erasure",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-007",
            name="Via Campesina/Nyéléni — Déclaration Souveraineté Alimentaire & Traité Semences FAO",
            country="Global",
            seed_patent_monopoly_score=22.0,
            agribusiness_market_control_score=28.0,
            small_farmer_displacement_score=30.0,
            traditional_knowledge_erasure_score=32.0,
            primary_pattern="seed_patent_monopoly",
        ),
        FoodSovereigntyEntity(
            entity_id="FS-008",
            name="ONU/FAO/TIRPAA — Traité International Ressources Phytogénétiques & Rapporteur Alimentation",
            country="Global",
            seed_patent_monopoly_score=4.0,
            agribusiness_market_control_score=5.0,
            small_farmer_displacement_score=3.0,
            traditional_knowledge_erasure_score=6.0,
            primary_pattern="traditional_knowledge_erasure",
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

    return FoodSovereigntyEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_food_sovereignty_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "grain_org_seed_patent_monopoly_corporate_control_food_report",
            "un_special_rapporteur_right_food_annual_report_seed_sovereignty",
            "itpgrfa_fao_treaty_plant_genetic_resources_food_agriculture",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_food_sovereignty_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_food_sovereignty_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
