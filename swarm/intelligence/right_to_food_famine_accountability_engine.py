from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RightToFoodFamineAccountabilityEntity:
    entity_id: str
    name: str
    country: str
    acute_food_insecurity_score: float
    famine_policy_accountability_score: float
    aid_blockage_obstruction_score: float
    legal_right_to_food_enforcement_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_food_famine_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.acute_food_insecurity_score * 0.30
            + self.famine_policy_accountability_score * 0.25
            + self.aid_blockage_obstruction_score * 0.25
            + self.legal_right_to_food_enforcement_score * 0.20,
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
        self.estimated_right_to_food_famine_accountability_index = round(
            self.composite_score / 100 * 10, 2
        )

@dataclass
class RightToFoodFamineAccountabilityEngineResult:
    agent: str = "Right to Food Famine Accountability Engine Agent"
    domain: str = "right_to_food_famine_accountability"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.87
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_food_famine_accountability_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToFoodFamineAccountabilityEntity] = field(default_factory=list)

def run_right_to_food_famine_accountability_engine() -> RightToFoodFamineAccountabilityEngineResult:
    entities = [
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-001",
            name="Gaza — Famine Induite, Blocus Total Aide Alimentaire & Armement Faim comme Arme de Guerre",
            country="Palestine/Moyen-Orient",
            acute_food_insecurity_score=98.0,
            famine_policy_accountability_score=97.0,
            aid_blockage_obstruction_score=99.0,
            legal_right_to_food_enforcement_score=96.0,
            primary_pattern="aid_blockage_obstruction",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-002",
            name="Soudan — Famine Résultant du Conflit RSF/SAF, 8,5M Déplacés & Obstruction Aide Humanitaire",
            country="Afrique du Nord-Est",
            acute_food_insecurity_score=93.0,
            famine_policy_accountability_score=90.0,
            aid_blockage_obstruction_score=92.0,
            legal_right_to_food_enforcement_score=88.0,
            primary_pattern="acute_food_insecurity",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-003",
            name="Éthiopie/Tigray — Famine Délibérée 2020-2022, Siège & Impunité Gouvernementale Documentée",
            country="Afrique de l'Est",
            acute_food_insecurity_score=87.0,
            famine_policy_accountability_score=88.0,
            aid_blockage_obstruction_score=85.0,
            legal_right_to_food_enforcement_score=90.0,
            primary_pattern="famine_policy_accountability",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-004",
            name="Yemen — 21M Personnes Insécurité Alimentaire, Blocus Ports & Absence Mécanismes Responsabilité",
            country="Moyen-Orient",
            acute_food_insecurity_score=88.0,
            famine_policy_accountability_score=82.0,
            aid_blockage_obstruction_score=86.0,
            legal_right_to_food_enforcement_score=80.0,
            primary_pattern="aid_blockage_obstruction",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-005",
            name="Sahel (Mali/Burkina/Niger) — 15M Affamés, Coups d'État & Expulsion ONG Humanitaires",
            country="Afrique de l'Ouest",
            acute_food_insecurity_score=58.0,
            famine_policy_accountability_score=60.0,
            aid_blockage_obstruction_score=55.0,
            legal_right_to_food_enforcement_score=52.0,
            primary_pattern="famine_policy_accountability",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-006",
            name="Haiti — Gangs Contrôlant Routes Alimentaires, Effondrement État & 5M en Famine Aiguë",
            country="Caraïbes",
            acute_food_insecurity_score=52.0,
            famine_policy_accountability_score=48.0,
            aid_blockage_obstruction_score=50.0,
            legal_right_to_food_enforcement_score=45.0,
            primary_pattern="acute_food_insecurity",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-007",
            name="PAM/FAO — Système Alerte IPC Phase 4-5, Coordination Humanitaire & Financement Insuffisant",
            country="Global",
            acute_food_insecurity_score=28.0,
            famine_policy_accountability_score=30.0,
            aid_blockage_obstruction_score=25.0,
            legal_right_to_food_enforcement_score=32.0,
            primary_pattern="legal_right_to_food_enforcement",
        ),
        RightToFoodFamineAccountabilityEntity(
            entity_id="RTFFA-008",
            name="ONU/Rapporteur Spécial Alimentation — Art.11 PIDESC, Jurisprudence & Obligations Extraterritoriales",
            country="Global",
            acute_food_insecurity_score=7.0,
            famine_policy_accountability_score=10.0,
            aid_blockage_obstruction_score=5.0,
            legal_right_to_food_enforcement_score=12.0,
            primary_pattern="legal_right_to_food_enforcement",
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

    return RightToFoodFamineAccountabilityEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_food_famine_accountability_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_wfp_ipc_acute_food_insecurity_global_report_2025",
            "un_special_rapporteur_right_to_food_annual_report",
            "oxfam_hunger_in_a_warming_world_2024",
            "human_rights_watch_famine_crimes_accountability_2025",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_right_to_food_famine_accountability_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_right_to_food_famine_accountability_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
