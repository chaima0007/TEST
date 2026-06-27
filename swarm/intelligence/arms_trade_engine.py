from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ArmsTradeEntity:
    entity_id: str
    name: str
    country: str
    atrocity_enabling_transfers_score: float
    export_control_circumvention_score: float
    civilian_harm_documentation_score: float
    arms_embargo_violation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_arms_trade_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.atrocity_enabling_transfers_score * 0.30
            + self.export_control_circumvention_score * 0.25
            + self.civilian_harm_documentation_score * 0.25
            + self.arms_embargo_violation_score * 0.20,
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
        self.estimated_arms_trade_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ArmsTradeEngineResult:
    agent: str = "Arms Trade Engine Agent"
    domain: str = "arms_trade"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_arms_trade_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ArmsTradeEntity] = field(default_factory=list)

def run_arms_trade_engine() -> ArmsTradeEngineResult:
    entities = [
        ArmsTradeEntity(
            entity_id="AT-001",
            name="USA/Arabie Saoudite — 100Mrd$ Armes Yémen, Bombes Écoles/Hôpitaux & Impunité Exportateur",
            country="Amérique du Nord / Moyen-Orient",
            atrocity_enabling_transfers_score=95.0,
            export_control_circumvention_score=88.0,
            civilian_harm_documentation_score=95.0,
            arms_embargo_violation_score=90.0,
            primary_pattern="atrocity_enabling_transfers",
        ),
        ArmsTradeEntity(
            entity_id="AT-002",
            name="Russie/Ukraine — Bombardements Civils, Missiles Interdits & Violations DIH Documentées",
            country="Europe de l'Est",
            atrocity_enabling_transfers_score=92.0,
            export_control_circumvention_score=85.0,
            civilian_harm_documentation_score=92.0,
            arms_embargo_violation_score=92.0,
            primary_pattern="civilian_harm_documentation",
        ),
        ArmsTradeEntity(
            entity_id="AT-003",
            name="Israël/Gaza — Armes Occidentales Utilisées Populations Civiles & Génocide Allégué CIJ",
            country="Moyen-Orient",
            atrocity_enabling_transfers_score=90.0,
            export_control_circumvention_score=82.0,
            civilian_harm_documentation_score=95.0,
            arms_embargo_violation_score=85.0,
            primary_pattern="civilian_harm_documentation",
        ),
        ArmsTradeEntity(
            entity_id="AT-004",
            name="Chine/Myanmar — Armes Post-Coup, Junta Massacres & Complicité Transferts Embargo",
            country="Asie du Nord-Est / Asie du Sud-Est",
            atrocity_enabling_transfers_score=85.0,
            export_control_circumvention_score=88.0,
            civilian_harm_documentation_score=82.0,
            arms_embargo_violation_score=85.0,
            primary_pattern="export_control_circumvention",
        ),
        ArmsTradeEntity(
            entity_id="AT-005",
            name="UE/Exportateurs — France/Allemagne/Italie Ventes Régimes Autoritaires & Contrôles Lacunaires",
            country="Europe",
            atrocity_enabling_transfers_score=55.0,
            export_control_circumvention_score=58.0,
            civilian_harm_documentation_score=52.0,
            arms_embargo_violation_score=50.0,
            primary_pattern="export_control_circumvention",
        ),
        ArmsTradeEntity(
            entity_id="AT-006",
            name="Courtiers Illicites — Réseaux Viktor Bout Type, États Faillis & Circuits Parallèles",
            country="Global",
            atrocity_enabling_transfers_score=52.0,
            export_control_circumvention_score=58.0,
            civilian_harm_documentation_score=48.0,
            arms_embargo_violation_score=55.0,
            primary_pattern="arms_embargo_violation",
        ),
        ArmsTradeEntity(
            entity_id="AT-007",
            name="CAAT/Amnesty Arms — Campagne Contre Commerce Armes, ATT Ratification & Plaidoyer Suspensions",
            country="Global",
            atrocity_enabling_transfers_score=22.0,
            export_control_circumvention_score=25.0,
            civilian_harm_documentation_score=28.0,
            arms_embargo_violation_score=30.0,
            primary_pattern="atrocity_enabling_transfers",
        ),
        ArmsTradeEntity(
            entity_id="AT-008",
            name="ONU/Traité Commerce Armes 2014 — ATT, Registre Armes Classiques & Comité États Parties",
            country="Global",
            atrocity_enabling_transfers_score=4.0,
            export_control_circumvention_score=5.0,
            civilian_harm_documentation_score=3.0,
            arms_embargo_violation_score=6.0,
            primary_pattern="arms_embargo_violation",
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

    return ArmsTradeEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_arms_trade_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "sipri_arms_transfers_database_global_trends_report",
            "amnesty_international_arms_trade_atrocities_annual_report",
            "arms_control_association_treaty_compliance_global_monitor",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_arms_trade_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_arms_trade_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
