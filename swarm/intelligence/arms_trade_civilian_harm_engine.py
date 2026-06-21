from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ArmsTradeClvilianHarmEntity:
    entity_id: str
    name: str
    country: str
    arms_transfers_rights_abusing_states_score: float
    explosive_weapons_populated_areas_score: float
    illicit_arms_trafficking_diversion_score: float
    arms_trade_accountability_transparency_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_arms_trade_civilian_harm_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.arms_transfers_rights_abusing_states_score * 0.30
            + self.explosive_weapons_populated_areas_score * 0.25
            + self.illicit_arms_trafficking_diversion_score * 0.25
            + self.arms_trade_accountability_transparency_gap_score * 0.20,
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
        self.estimated_arms_trade_civilian_harm_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ArmsTradeClvilianHarmEngineResult:
    agent: str = "Arms Trade Civilian Harm Engine Agent"
    domain: str = "arms_trade_civilian_harm"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.88
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_arms_trade_civilian_harm_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArmsTradeClvilianHarmEntity] = field(default_factory=list)

def run_arms_trade_civilian_harm_engine() -> ArmsTradeClvilianHarmEngineResult:
    entities = [
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-001",
            name="Yémen/Coalition Arabie Saoudite — bombes à sous-munitions UK/US, frappes hôpitaux & marchés documentées",
            country="Moyen-Orient",
            arms_transfers_rights_abusing_states_score=96.0,
            explosive_weapons_populated_areas_score=95.0,
            illicit_arms_trafficking_diversion_score=88.0,
            arms_trade_accountability_transparency_gap_score=93.0,
            primary_pattern="explosive_weapons_populated_areas",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-002",
            name="Myanmar — armes importées utilisées génocide Rohingya, junta armée post-coup 2021",
            country="Asie du Sud-Est",
            arms_transfers_rights_abusing_states_score=90.0,
            explosive_weapons_populated_areas_score=85.0,
            illicit_arms_trafficking_diversion_score=82.0,
            arms_trade_accountability_transparency_gap_score=88.0,
            primary_pattern="arms_transfers_rights_abusing_states",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-003",
            name="Soudan — RSF armée par Émirats, massacres Darfour 2023-2024, embargo violé ouvertement",
            country="Afrique du Nord-Est",
            arms_transfers_rights_abusing_states_score=88.0,
            explosive_weapons_populated_areas_score=90.0,
            illicit_arms_trafficking_diversion_score=85.0,
            arms_trade_accountability_transparency_gap_score=87.0,
            primary_pattern="explosive_weapons_populated_areas",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-004",
            name="Libye — embargo ONU violé par multiples acteurs, milices armées, civils victimes trafics",
            country="Afrique du Nord",
            arms_transfers_rights_abusing_states_score=85.0,
            explosive_weapons_populated_areas_score=80.0,
            illicit_arms_trafficking_diversion_score=90.0,
            arms_trade_accountability_transparency_gap_score=86.0,
            primary_pattern="illicit_arms_trafficking_diversion",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-005",
            name="Ukraine/Russie — EWIPA massif zones peuplées, armes à sous-munitions Russie, usage civils illicite",
            country="Europe de l'Est",
            arms_transfers_rights_abusing_states_score=58.0,
            explosive_weapons_populated_areas_score=72.0,
            illicit_arms_trafficking_diversion_score=52.0,
            arms_trade_accountability_transparency_gap_score=55.0,
            primary_pattern="explosive_weapons_populated_areas",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-006",
            name="Philippines — armes US utilisées guerre drogue extrajudiciaire, 30 000 morts impunité Duterte",
            country="Asie du Sud-Est",
            arms_transfers_rights_abusing_states_score=55.0,
            explosive_weapons_populated_areas_score=45.0,
            illicit_arms_trafficking_diversion_score=48.0,
            arms_trade_accountability_transparency_gap_score=52.0,
            primary_pattern="arms_transfers_rights_abusing_states",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-007",
            name="Brésil — armes légères trafiquées vers favelas, détournements stocks militaires documentés",
            country="Amérique du Sud",
            arms_transfers_rights_abusing_states_score=28.0,
            explosive_weapons_populated_areas_score=22.0,
            illicit_arms_trafficking_diversion_score=35.0,
            arms_trade_accountability_transparency_gap_score=30.0,
            primary_pattern="illicit_arms_trafficking_diversion",
        ),
        ArmsTradeClvilianHarmEntity(
            entity_id="ATCH-008",
            name="Norvège — politique stricte transferts armes, rapport ATT exemplaire, aucune vente régimes abusifs",
            country="Europe du Nord",
            arms_transfers_rights_abusing_states_score=4.0,
            explosive_weapons_populated_areas_score=3.0,
            illicit_arms_trafficking_diversion_score=5.0,
            arms_trade_accountability_transparency_gap_score=4.0,
            primary_pattern="arms_trade_accountability_transparency_gap",
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

    return ArmsTradeClvilianHarmEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_arms_trade_civilian_harm_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "sipri_arms_transfers_2023",
            "arms_control_association_2023",
            "amnesty_arms_trade_2022",
            "un_arms_trade_treaty_report_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_arms_trade_civilian_harm_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_arms_trade_civilian_harm_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
