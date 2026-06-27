from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#84cc16"


@dataclass
class FoodSecurityRightsEntity:
    entity_id: str
    name: str
    country: str
    famine_severity_score: float
    food_access_barrier_score: float
    agricultural_destruction_score: float
    food_aid_obstruction_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_food_security_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.famine_severity_score * 0.30
            + self.food_access_barrier_score * 0.25
            + self.agricultural_destruction_score * 0.25
            + self.food_aid_obstruction_score * 0.20,
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
        self.estimated_food_security_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class FoodSecurityRightsEngineResult:
    agent: str = "FoodSecurityRights Engine Agent"
    domain: str = "food_security_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_food_security_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FoodSecurityRightsEntity] = field(default_factory=list)


def run_food_security_rights_engine() -> FoodSecurityRightsEngineResult:
    entities = [
        FoodSecurityRightsEntity(
            entity_id="FSR-001",
            name="Somalie — IPC Phase 5 Catastrophe",
            country="Somalie",
            famine_severity_score=96.0,
            food_access_barrier_score=94.0,
            agricultural_destruction_score=93.0,
            food_aid_obstruction_score=95.0,
            primary_pattern="famine_ipc5_aid_blockade",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-002",
            name="Gaza/Palestine — Famine délibérée IPC 2024",
            country="Palestine",
            famine_severity_score=93.0,
            food_access_barrier_score=91.0,
            agricultural_destruction_score=92.0,
            food_aid_obstruction_score=90.0,
            primary_pattern="deliberate_starvation_warfare",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-003",
            name="Éthiopie/Tigré — Blocus humanitaire",
            country="Éthiopie",
            famine_severity_score=85.0,
            food_access_barrier_score=84.0,
            agricultural_destruction_score=82.0,
            food_aid_obstruction_score=86.0,
            primary_pattern="humanitarian_blockade_conflict",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-004",
            name="Yémen — Guerre & destruction agricole",
            country="Yémen",
            famine_severity_score=80.0,
            food_access_barrier_score=79.0,
            agricultural_destruction_score=78.0,
            food_aid_obstruction_score=81.0,
            primary_pattern="war_induced_food_system_collapse",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-005",
            name="Afghanistan — Malnutrition aiguë & restrictions ONGs",
            country="Afghanistan",
            famine_severity_score=56.0,
            food_access_barrier_score=55.0,
            agricultural_destruction_score=54.0,
            food_aid_obstruction_score=57.0,
            primary_pattern="ngo_restriction_acute_malnutrition",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-006",
            name="RCA — Violences intercommunautaires & marchés détruits",
            country="République Centrafricaine",
            famine_severity_score=47.0,
            food_access_barrier_score=46.0,
            agricultural_destruction_score=48.0,
            food_aid_obstruction_score=45.0,
            primary_pattern="market_destruction_intercommunal_violence",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-007",
            name="Haïti — Gangs contrôlant distribution alimentaire",
            country="Haïti",
            famine_severity_score=31.0,
            food_access_barrier_score=30.0,
            agricultural_destruction_score=29.0,
            food_aid_obstruction_score=32.0,
            primary_pattern="gang_controlled_food_distribution",
        ),
        FoodSecurityRightsEntity(
            entity_id="FSR-008",
            name="WFP/FAO — Mécanismes alerte précoce FEWS NET",
            country="International",
            famine_severity_score=12.0,
            food_access_barrier_score=11.0,
            agricultural_destruction_score=13.0,
            food_aid_obstruction_score=10.0,
            primary_pattern="early_warning_response_framework",
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

    return FoodSecurityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_food_security_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fao_global_food_crises_report_2024",
            "wfp_hunger_map_live_data_2024",
            "ipc_global_initiative_acute_food_insecurity",
            "hrw_starvation_as_weapon_war_documentation",
            "oxfam_right_food_global_violations_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_food_security_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_food_security_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
