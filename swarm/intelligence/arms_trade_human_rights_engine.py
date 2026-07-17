from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#dc2626"


@dataclass
class ArmsTradeHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    arms_to_abusers_score: float
    civilian_harm_arms_score: float
    export_control_failure_score: float
    accountability_impunity_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_arms_trade_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.arms_to_abusers_score * 0.30
            + self.civilian_harm_arms_score * 0.25
            + self.export_control_failure_score * 0.25
            + self.accountability_impunity_score * 0.20,
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
        self.estimated_arms_trade_human_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ArmsTradeHumanRightsEngineResult:
    agent: str = "Arms Trade Human Rights Engine Agent"
    domain: str = "arms_trade_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_arms_trade_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArmsTradeHumanRightsEntity] = field(default_factory=list)


def run_arms_trade_human_rights_engine() -> ArmsTradeHumanRightsEngineResult:
    entities = [
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-001",
            name="Arabie Saoudite/Yémen — USA/UK/France vendent bombes malgré 25 000 frappes civiles",
            country="Arabie Saoudite",
            arms_to_abusers_score=97.0,
            civilian_harm_arms_score=96.0,
            export_control_failure_score=95.0,
            accountability_impunity_score=94.0,
            primary_pattern="arms_to_abusers",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-002",
            name="Myanmar — Junta TATMADAW armes Chine/Russie/Inde malgré génocide Rohingya",
            country="Myanmar",
            arms_to_abusers_score=91.0,
            civilian_harm_arms_score=89.0,
            export_control_failure_score=90.0,
            accountability_impunity_score=88.0,
            primary_pattern="arms_to_abusers",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-003",
            name="Russie/Ukraine — Exportations armes vers zones conflits, cluster bombs interdites utilisées",
            country="Russie",
            arms_to_abusers_score=85.0,
            civilian_harm_arms_score=87.0,
            export_control_failure_score=83.0,
            accountability_impunity_score=84.0,
            primary_pattern="civilian_harm_arms",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-004",
            name="Israël/Gaza — Frappes civiles, USA transferts armes malgré CIJ, violations DIH",
            country="Israël/Gaza",
            arms_to_abusers_score=77.0,
            civilian_harm_arms_score=80.0,
            export_control_failure_score=76.0,
            accountability_impunity_score=75.0,
            primary_pattern="civilian_harm_arms",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-005",
            name="USA — Plus grand exportateur armes 42% mondial, ventes régimes autoritaires",
            country="USA",
            arms_to_abusers_score=54.0,
            civilian_harm_arms_score=52.0,
            export_control_failure_score=56.0,
            accountability_impunity_score=50.0,
            primary_pattern="export_control_failure",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-006",
            name="France/UK — Ventes Émirats/Egypte/Inde malgré rapports ONU, profit avant droits",
            country="France/UK",
            arms_to_abusers_score=44.0,
            civilian_harm_arms_score=46.0,
            export_control_failure_score=48.0,
            accountability_impunity_score=42.0,
            primary_pattern="export_control_failure",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-007",
            name="Allemagne — ATT ratifié, suspensions partielles Turquie/Egypte, contrôles lacunaires",
            country="Allemagne",
            arms_to_abusers_score=27.0,
            civilian_harm_arms_score=29.0,
            export_control_failure_score=30.0,
            accountability_impunity_score=26.0,
            primary_pattern="export_control_failure",
        ),
        ArmsTradeHumanRightsEntity(
            entity_id="ATH-008",
            name="Norvège/Suède — ATT respecté, refus ventes régimes autoritaires, transparence totale",
            country="Norvège/Suède",
            arms_to_abusers_score=7.0,
            civilian_harm_arms_score=8.0,
            export_control_failure_score=6.0,
            accountability_impunity_score=9.0,
            primary_pattern="accountability_impunity",
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

    return ArmsTradeHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_arms_trade_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "sipri_arms_transfer_database_2024",
            "amnesty_arms_trade_treaty_violations_2024",
            "hrw_weapons_civilian_harm_documentation",
            "oxfam_arms_trade_human_rights_report",
            "campaign_against_arms_trade_global_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_arms_trade_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
