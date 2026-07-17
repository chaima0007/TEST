from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PeasantRightsEntity:
    entity_id: str
    name: str
    country: str
    land_dispossession_score: float
    seed_criminalization_score: float
    legal_framework_absence_score: float
    corporate_agro_domination_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_peasant_rights_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.land_dispossession_score * 0.30
            + self.seed_criminalization_score * 0.25
            + self.legal_framework_absence_score * 0.25
            + self.corporate_agro_domination_score * 0.20,
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
        self.estimated_peasant_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PeasantRightsEngineResult:
    agent: str = "Peasant Rights Engine Agent"
    domain: str = "peasant_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.83
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_peasant_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PeasantRightsEntity] = field(default_factory=list)

def run_peasant_rights_engine() -> PeasantRightsEngineResult:
    entities = [
        PeasantRightsEntity(
            entity_id="PR-001",
            name="Honduras/Colombie/Guatemala — Syndicalistes Paysans Assassinés & Narco-Latifundisme",
            country="Amérique Latine",
            land_dispossession_score=92.0,
            seed_criminalization_score=82.0,
            legal_framework_absence_score=88.0,
            corporate_agro_domination_score=85.0,
            primary_pattern="land_dispossession",
        ),
        PeasantRightsEntity(
            entity_id="PR-002",
            name="Myanmar/Birmanie — Confiscation 5M Hectares, Junte Militaire & Entreprises Chinoises",
            country="Asie du Sud-Est",
            land_dispossession_score=90.0,
            seed_criminalization_score=78.0,
            legal_framework_absence_score=85.0,
            corporate_agro_domination_score=88.0,
            primary_pattern="corporate_agro_domination",
        ),
        PeasantRightsEntity(
            entity_id="PR-003",
            name="Inde — Lois Agricoles Libéralisation Forcée, Protestations Paysannes & MSP Menacé",
            country="Asie du Sud",
            land_dispossession_score=78.0,
            seed_criminalization_score=82.0,
            legal_framework_absence_score=80.0,
            corporate_agro_domination_score=85.0,
            primary_pattern="seed_criminalization",
        ),
        PeasantRightsEntity(
            entity_id="PR-004",
            name="Afrique/Sahel — Accaparement Terres, Code Semencier UPOV & Paysans Sans Droits",
            country="Afrique Sub-Saharienne",
            land_dispossession_score=72.0,
            seed_criminalization_score=80.0,
            legal_framework_absence_score=78.0,
            corporate_agro_domination_score=75.0,
            primary_pattern="legal_framework_absence",
        ),
        PeasantRightsEntity(
            entity_id="PR-005",
            name="Brésil — Agrobusiness, Déforestation Amazonie & Mouvement Sans Terre MST Réprimé",
            country="Amérique Latine",
            land_dispossession_score=52.0,
            seed_criminalization_score=55.0,
            legal_framework_absence_score=58.0,
            corporate_agro_domination_score=60.0,
            primary_pattern="land_dispossession",
        ),
        PeasantRightsEntity(
            entity_id="PR-006",
            name="Philippines — Réforme Agraire Inachevée, Haciendas & Paysans Assassinés Mindanao",
            country="Asie du Sud-Est",
            land_dispossession_score=50.0,
            seed_criminalization_score=48.0,
            legal_framework_absence_score=55.0,
            corporate_agro_domination_score=52.0,
            primary_pattern="legal_framework_absence",
        ),
        PeasantRightsEntity(
            entity_id="PR-007",
            name="UE — PAC Lobby Agro-Industriel, Disparition Petites Exploitations & Semences Brevetées",
            country="Europe",
            land_dispossession_score=25.0,
            seed_criminalization_score=30.0,
            legal_framework_absence_score=28.0,
            corporate_agro_domination_score=32.0,
            primary_pattern="corporate_agro_domination",
        ),
        PeasantRightsEntity(
            entity_id="PR-008",
            name="ONU/UNDROP/Via Campesina — Déclaration Droits Paysans 2018, FAO & Agroécologie",
            country="Global",
            land_dispossession_score=4.0,
            seed_criminalization_score=5.0,
            legal_framework_absence_score=3.0,
            corporate_agro_domination_score=6.0,
            primary_pattern="seed_criminalization",
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

    return PeasantRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_peasant_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "via_campesina_international_peasant_movement_annual_report",
            "grain_org_land_grabbing_corporate_food_regime_report",
            "un_special_rapporteur_right_food_peasants_undrop_implementation_review",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_peasant_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_peasant_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
