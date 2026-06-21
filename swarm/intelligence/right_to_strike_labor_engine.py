from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RightToStrikeLaborEntity:
    entity_id: str
    name: str
    country: str
    strike_prohibition_criminalization_severity_score: float
    essential_services_overclassification_scope_scale_score: float
    union_busting_retaliation_workers_score: float
    precarious_workers_strike_exclusion_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_strike_labor_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.strike_prohibition_criminalization_severity_score * 0.30
            + self.essential_services_overclassification_scope_scale_score * 0.25
            + self.union_busting_retaliation_workers_score * 0.25
            + self.precarious_workers_strike_exclusion_gap_score * 0.20,
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
        self.estimated_right_to_strike_labor_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RightToStrikeLaborEngineResult:
    agent: str = "Right to Strike Labor Engine Agent"
    domain: str = "right_to_strike_labor"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_strike_labor_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToStrikeLaborEntity] = field(default_factory=list)

def run_right_to_strike_labor_engine() -> RightToStrikeLaborEngineResult:
    entities = [
        RightToStrikeLaborEntity(
            entity_id="RSL-001",
            name="Chine/Vietnam — Grèves Illégales Officiellement, 300+ Grèves/An Réprimées Foxconn/Nike, Syndicalistes Arrêtés & ACFTU Contrôlé État",
            country="Chine/Vietnam",
            strike_prohibition_criminalization_severity_score=95.0,
            essential_services_overclassification_scope_scale_score=93.0,
            union_busting_retaliation_workers_score=92.0,
            precarious_workers_strike_exclusion_gap_score=91.0,
            primary_pattern="strike_prohibition_criminalization_severity",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-002",
            name="Arabie Saoudite/Qatar — Grèves Totalement Interdites, Travailleurs Migrants Deportés si Grève, Kafala & Syndicats Criminalisés",
            country="Arabie Saoudite/Qatar",
            strike_prohibition_criminalization_severity_score=92.0,
            essential_services_overclassification_scope_scale_score=89.0,
            union_busting_retaliation_workers_score=88.0,
            precarious_workers_strike_exclusion_gap_score=90.0,
            primary_pattern="strike_prohibition_criminalization_severity",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-003",
            name="Bangladesh/Rana Plaza Aftermath — Grèves Réprimées Usines Vêtements, Licenciements Organisateurs, Police Anti-Grève & Peur Représailles",
            country="Bangladesh",
            strike_prohibition_criminalization_severity_score=89.0,
            essential_services_overclassification_scope_scale_score=86.0,
            union_busting_retaliation_workers_score=86.0,
            precarious_workers_strike_exclusion_gap_score=86.0,
            primary_pattern="union_busting_retaliation_workers",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-004",
            name="Colombie/Amérique Latine — 3 000 Syndicalistes Assassinés 1986-2023, Grèves Minières Réprimées Armée & Impunité Tueurs",
            country="Colombie",
            strike_prohibition_criminalization_severity_score=86.0,
            essential_services_overclassification_scope_scale_score=83.0,
            union_busting_retaliation_workers_score=82.0,
            precarious_workers_strike_exclusion_gap_score=84.0,
            primary_pattern="union_busting_retaliation_workers",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-005",
            name="UK Post-2023 — Strikes Act 2023 Minimum Service Levels, Transport/Santé Grèves Restreintes & Sanctions Anti-Grévistes",
            country="Royaume-Uni",
            strike_prohibition_criminalization_severity_score=57.0,
            essential_services_overclassification_scope_scale_score=54.0,
            union_busting_retaliation_workers_score=53.0,
            precarious_workers_strike_exclusion_gap_score=55.0,
            primary_pattern="essential_services_overclassification_scope_scale",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-006",
            name="USA — Taft-Hartley Interdictions Syndicats, Amazon/Starbucks Union Busting, Grévistes Remplacés Permanents & Gig Workers Exclus",
            country="USA",
            strike_prohibition_criminalization_severity_score=54.0,
            essential_services_overclassification_scope_scale_score=51.0,
            union_busting_retaliation_workers_score=50.0,
            precarious_workers_strike_exclusion_gap_score=52.0,
            primary_pattern="precarious_workers_strike_exclusion_gap",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-007",
            name="ITUC/CSI — Indice Mondial Droits Syndicaux, Cas Violations & Plaidoyer ILO Convention 87/98",
            country="Global",
            strike_prohibition_criminalization_severity_score=28.0,
            essential_services_overclassification_scope_scale_score=26.0,
            union_busting_retaliation_workers_score=27.0,
            precarious_workers_strike_exclusion_gap_score=27.0,
            primary_pattern="strike_prohibition_criminalization_severity",
        ),
        RightToStrikeLaborEntity(
            entity_id="RSL-008",
            name="OIT/C087-C098 — Convention Liberté Syndicale 87, Droit Organisation Collective 98 & SDG 8.8 Droits Travail",
            country="Global",
            strike_prohibition_criminalization_severity_score=4.0,
            essential_services_overclassification_scope_scale_score=4.0,
            union_busting_retaliation_workers_score=5.0,
            precarious_workers_strike_exclusion_gap_score=4.0,
            primary_pattern="essential_services_overclassification_scope_scale",
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

    return RightToStrikeLaborEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_strike_labor_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ituc_global_rights_index_annual_report",
            "ilo_convention_87_98_compliance_monitoring",
            "human_rights_watch_labor_rights_global_survey",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_right_to_strike_labor_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_right_to_strike_labor_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
