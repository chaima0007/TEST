from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0d9488"


@dataclass
class RightToWorkRightsEntity:
    entity_id: str
    name: str
    country: str
    decent_work_denial_score: float
    forced_labor_conditions_score: float
    union_access_denial_score: float
    precarious_employment_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_work_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.decent_work_denial_score * 0.30
            + self.forced_labor_conditions_score * 0.25
            + self.union_access_denial_score * 0.25
            + self.precarious_employment_score * 0.20,
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
        self.estimated_right_to_work_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToWorkRightsEngineResult:
    agent: str = "Right To Work Rights Engine Agent"
    domain: str = "right_to_work_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_work_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToWorkRightsEntity] = field(default_factory=list)


def run_right_to_work_rights_engine() -> RightToWorkRightsEngineResult:
    entities = [
        RightToWorkRightsEntity(
            entity_id="RTW-001",
            name="Qatar — Kafala système, 6 500 morts Coupe du Monde construction, passeports confisqués",
            country="Qatar",
            decent_work_denial_score=97.0,
            forced_labor_conditions_score=96.0,
            union_access_denial_score=95.0,
            precarious_employment_score=94.0,
            primary_pattern="forced_labor_conditions",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-002",
            name="Corée du Nord — Travail forcé État, exportation main d'oeuvre Russie/Chine, zéro syndicats",
            country="Corée du Nord",
            decent_work_denial_score=91.0,
            forced_labor_conditions_score=93.0,
            union_access_denial_score=92.0,
            precarious_employment_score=89.0,
            primary_pattern="forced_labor_conditions",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-003",
            name="Éthiopie/Bangladesh — Textile sweatshops, salaire 40$/mois, heures illimitées, feux Rana Plaza",
            country="Éthiopie/Bangladesh",
            decent_work_denial_score=85.0,
            forced_labor_conditions_score=83.0,
            union_access_denial_score=84.0,
            precarious_employment_score=87.0,
            primary_pattern="decent_work_denial",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-004",
            name="Arabie Saoudite — Travailleurs migrants kafala, 12M sans droits, licenciements arbitraires",
            country="Arabie Saoudite",
            decent_work_denial_score=77.0,
            forced_labor_conditions_score=79.0,
            union_access_denial_score=78.0,
            precarious_employment_score=75.0,
            primary_pattern="union_access_denial",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-005",
            name="USA — Gig economy 60M, Uber/Amazon workers' rights, syndicats 10%, salaire minimum 7.25$",
            country="USA",
            decent_work_denial_score=54.0,
            forced_labor_conditions_score=52.0,
            union_access_denial_score=56.0,
            precarious_employment_score=58.0,
            primary_pattern="precarious_employment",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-006",
            name="Inde — 90% économie informelle, MGNREGA insuffisant, bonded labour 23M",
            country="Inde",
            decent_work_denial_score=46.0,
            forced_labor_conditions_score=48.0,
            union_access_denial_score=44.0,
            precarious_employment_score=50.0,
            primary_pattern="precarious_employment",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-007",
            name="France — Ubérisation, auto-entrepreneurs sans protection, réforme retraites contestée",
            country="France",
            decent_work_denial_score=28.0,
            forced_labor_conditions_score=26.0,
            union_access_denial_score=24.0,
            precarious_employment_score=30.0,
            primary_pattern="precarious_employment",
        ),
        RightToWorkRightsEntity(
            entity_id="RTW-008",
            name="Allemagne/Danemark — Co-gestion syndicale, salaire min 12€+, protection chômage universelle",
            country="Allemagne/Danemark",
            decent_work_denial_score=7.0,
            forced_labor_conditions_score=6.0,
            union_access_denial_score=8.0,
            precarious_employment_score=5.0,
            primary_pattern="union_access_denial",
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

    return RightToWorkRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_work_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_decent_work_global_report_2024",
            "ituc_global_rights_index_2024",
            "hrw_labor_rights_violations_global",
            "clean_clothes_campaign_garment_workers_2024",
            "business_human_rights_resource_center_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_work_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
