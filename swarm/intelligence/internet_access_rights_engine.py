from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#06b6d4"


@dataclass
class InternetAccessRightsEntity:
    entity_id: str
    name: str
    country: str
    internet_shutdown_score: float
    censorship_filtering_score: float
    digital_divide_score: float
    surveillance_chilling_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_internet_access_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.internet_shutdown_score * 0.30
            + self.censorship_filtering_score * 0.25
            + self.digital_divide_score * 0.25
            + self.surveillance_chilling_score * 0.20,
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
        self.estimated_internet_access_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class InternetAccessRightsEngineResult:
    agent: str = "Internet Access Rights Engine Agent"
    domain: str = "internet_access_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_internet_access_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InternetAccessRightsEntity] = field(default_factory=list)


def run_internet_access_rights_engine() -> InternetAccessRightsEngineResult:
    entities = [
        InternetAccessRightsEntity(
            entity_id="IAR-001",
            name="Corée du Nord",
            country="Corée du Nord",
            internet_shutdown_score=99.0,
            censorship_filtering_score=99.0,
            digital_divide_score=97.0,
            surveillance_chilling_score=98.0,
            primary_pattern="total_intranet_isolation",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-002",
            name="Éthiopie",
            country="Éthiopie",
            internet_shutdown_score=92.0,
            censorship_filtering_score=88.0,
            digital_divide_score=91.0,
            surveillance_chilling_score=86.0,
            primary_pattern="tigray_two_year_blackout",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-003",
            name="Myanmar",
            country="Myanmar",
            internet_shutdown_score=87.0,
            censorship_filtering_score=83.0,
            digital_divide_score=82.0,
            surveillance_chilling_score=84.0,
            primary_pattern="coup_shutdown_504_days",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-004",
            name="Iran",
            country="Iran",
            internet_shutdown_score=79.0,
            censorship_filtering_score=81.0,
            digital_divide_score=75.0,
            surveillance_chilling_score=78.0,
            primary_pattern="mahsa_amini_shutdown_filtering_80pct",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-005",
            name="Inde",
            country="Inde",
            internet_shutdown_score=57.0,
            censorship_filtering_score=52.0,
            digital_divide_score=54.0,
            surveillance_chilling_score=50.0,
            primary_pattern="kashmir_552_day_blackout",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-006",
            name="Nigeria",
            country="Nigeria",
            internet_shutdown_score=47.0,
            censorship_filtering_score=46.0,
            digital_divide_score=48.0,
            surveillance_chilling_score=43.0,
            primary_pattern="twitter_suspension_7_months",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-007",
            name="Russie",
            country="Russie",
            internet_shutdown_score=31.0,
            censorship_filtering_score=33.0,
            digital_divide_score=27.0,
            surveillance_chilling_score=30.0,
            primary_pattern="runet_partial_isolation_meta_blocked",
        ),
        InternetAccessRightsEntity(
            entity_id="IAR-008",
            name="Estonie & Islande",
            country="Estonie/Islande",
            internet_shutdown_score=8.0,
            censorship_filtering_score=9.0,
            digital_divide_score=11.0,
            surveillance_chilling_score=10.0,
            primary_pattern="e_government_universal_fibre_model",
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

    return InternetAccessRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_internet_access_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "accessnow_keepiton_internet_shutdown_tracker_2024",
            "netblocks_internet_disruption_observatory",
            "freedom_house_freedom_on_net_annual_report_2024",
            "article19_digital_rights_global_report",
            "itu_measuring_digital_development_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_internet_access_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
