from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#1a0a05"

@dataclass
class ArmsTradeRightsEntity:
    entity_id: str
    name: str
    country: str
    illegal_arms_transfer_score: float
    child_soldier_recruitment_score: float
    civilian_targeting_score: float
    conflict_perpetuation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_arms_trade_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.illegal_arms_transfer_score * 0.30
            + self.child_soldier_recruitment_score * 0.25
            + self.civilian_targeting_score * 0.25
            + self.conflict_perpetuation_score * 0.20,
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
        self.estimated_arms_trade_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ArmsTradeRightsEngineResult:
    agent: str = "Arms Trade Rights Engine Agent"
    domain: str = "arms_trade_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_arms_trade_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArmsTradeRightsEntity] = field(default_factory=list)


def run_arms_trade_rights_engine() -> ArmsTradeRightsEngineResult:
    entities = [
        ArmsTradeRightsEntity(
            entity_id="ATR-001",
            name="Wagner Group (Russie) — Mercenaires Trafic Armes Afrique, Violations Droits Humains Mali/CAR/Soudan & Transferts Illégaux Systématiques",
            country="Russie/Afrique",
            illegal_arms_transfer_score=96.0,
            child_soldier_recruitment_score=91.0,
            civilian_targeting_score=94.0,
            conflict_perpetuation_score=93.0,
            primary_pattern="illegal_arms_transfer",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-002",
            name="Houthi Arms Networks (Yémen) — Trafic Armes Iran-Yémen, Missiles Ciblant Civils Saoudiens, Enfants Soldats & Embargo ONU Violé",
            country="Yémen/Iran",
            illegal_arms_transfer_score=90.0,
            child_soldier_recruitment_score=89.0,
            civilian_targeting_score=88.0,
            conflict_perpetuation_score=87.0,
            primary_pattern="child_soldier_recruitment",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-003",
            name="Janjaweed/RSF (Soudan) — Génocide Darfour, Recrutement Massif Enfants Soldats, Armes Légères Trafic & Ciblage Systématique Civils",
            country="Soudan",
            illegal_arms_transfer_score=83.0,
            child_soldier_recruitment_score=85.0,
            civilian_targeting_score=84.0,
            conflict_perpetuation_score=82.0,
            primary_pattern="child_soldier_recruitment",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-004",
            name="ISIS Weapons Supply Chains — Réseau Trafic Armes Transnational, Financement Terrorisme, Armes OTAN Capturées & Recrutement Mineurs",
            country="Irak/Syrie/Global",
            illegal_arms_transfer_score=78.0,
            child_soldier_recruitment_score=76.0,
            civilian_targeting_score=80.0,
            conflict_perpetuation_score=75.0,
            primary_pattern="civilian_targeting",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-005",
            name="Saudi Arabia Arms Purchases (BAE Systems/USA) — Ventes Légales Usage Contre Civils Yémen, Bombes Interdites & Cluster Munitions",
            country="Arabie Saoudite/UK/USA",
            illegal_arms_transfer_score=58.0,
            child_soldier_recruitment_score=42.0,
            civilian_targeting_score=60.0,
            conflict_perpetuation_score=55.0,
            primary_pattern="civilian_targeting",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-006",
            name="USA Military-Industrial Complex (Lockheed/Raytheon Exports) — Exportations Zones Conflits, Contournement ATT & Responsabilité Limitée",
            country="USA",
            illegal_arms_transfer_score=46.0,
            child_soldier_recruitment_score=40.0,
            civilian_targeting_score=52.0,
            conflict_perpetuation_score=48.0,
            primary_pattern="conflict_perpetuation",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-007",
            name="UN Arms Embargo Monitoring — Surveillance Partielle Embargos, Application Limitée Sanctions & Lacunes Reporting États Membres",
            country="Global/ONU",
            illegal_arms_transfer_score=32.0,
            child_soldier_recruitment_score=28.0,
            civilian_targeting_score=30.0,
            conflict_perpetuation_score=26.0,
            primary_pattern="illegal_arms_transfer",
        ),
        ArmsTradeRightsEntity(
            entity_id="ATR-008",
            name="ICAN / ATT Treaty Framework — Contrôle Armes Prix Nobel 2017, Traité Commerce Armes Ratifié 113 États & Meilleure Pratique Transparence",
            country="Global",
            illegal_arms_transfer_score=12.0,
            child_soldier_recruitment_score=10.0,
            civilian_targeting_score=11.0,
            conflict_perpetuation_score=9.0,
            primary_pattern="conflict_perpetuation",
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

    return ArmsTradeRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_arms_trade_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "sipri_arms_transfer_database_annual_report",
            "arms_trade_treaty_annual_conference_reports",
            "hrw_child_soldiers_global_report",
            "un_panel_experts_arms_embargo_monitoring",
            "amnesty_international_arms_trade_violations",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_arms_trade_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_arms_trade_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
