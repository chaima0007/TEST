from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#06b6d4"


@dataclass
class NetNeutralityRightsEntity:
    entity_id: str
    name: str
    country: str
    traffic_discrimination_score: float
    zero_rating_inequity_score: float
    paid_prioritization_harm_score: float
    access_inequality_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_net_neutrality_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.traffic_discrimination_score * 0.30
            + self.zero_rating_inequity_score * 0.25
            + self.paid_prioritization_harm_score * 0.25
            + self.access_inequality_score * 0.20,
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
        self.estimated_net_neutrality_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class NetNeutralityRightsEngineResult:
    agent: str = "Net Neutrality Rights Engine Agent"
    domain: str = "net_neutrality_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_net_neutrality_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[NetNeutralityRightsEntity] = field(default_factory=list)


def run_net_neutrality_rights_engine() -> NetNeutralityRightsEngineResult:
    entities = [
        NetNeutralityRightsEntity(
            entity_id="NNR-001",
            name="Chine — Grande Muraille + État ISP Monopoly, Zéro Neutralité",
            country="Chine",
            traffic_discrimination_score=97.0,
            zero_rating_inequity_score=96.0,
            paid_prioritization_harm_score=95.0,
            access_inequality_score=97.0,
            primary_pattern="state_controlled_throttling",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-002",
            name="Russie — RuNet, Roskomnadzor Throttle Twitter/YouTube 2021, SORM",
            country="Russie",
            traffic_discrimination_score=91.0,
            zero_rating_inequity_score=89.0,
            paid_prioritization_harm_score=88.0,
            access_inequality_score=90.0,
            primary_pattern="state_controlled_throttling",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-003",
            name="Iran — Throttling WhatsApp/Instagram 0.5Mbps Permanent, VPN Seul Accès",
            country="Iran",
            traffic_discrimination_score=87.0,
            zero_rating_inequity_score=85.0,
            paid_prioritization_harm_score=84.0,
            access_inequality_score=86.0,
            primary_pattern="systematic_content_throttling",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-004",
            name="Inde — Free Basics Facebook Zero-Rating Monopole 2015-2016, TRAI Inégalités",
            country="Inde",
            traffic_discrimination_score=77.0,
            zero_rating_inequity_score=79.0,
            paid_prioritization_harm_score=76.0,
            access_inequality_score=74.0,
            primary_pattern="zero_rating_inequity",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-005",
            name="USA Post-2017 — FCC Pai Repeal, AT&T/Comcast Throttling Streaming",
            country="USA",
            traffic_discrimination_score=55.0,
            zero_rating_inequity_score=57.0,
            paid_prioritization_harm_score=54.0,
            access_inequality_score=52.0,
            primary_pattern="paid_prioritization_harm",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-006",
            name="Brésil — Opérateurs Zero-Rating WhatsApp/Globo Sans Régulation ANATEL",
            country="Brésil",
            traffic_discrimination_score=46.0,
            zero_rating_inequity_score=48.0,
            paid_prioritization_harm_score=45.0,
            access_inequality_score=44.0,
            primary_pattern="zero_rating_inequity",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-007",
            name="Portugal — Violations BEREC Zero-Rating Mineurs, Amendes Légères",
            country="Portugal",
            traffic_discrimination_score=28.0,
            zero_rating_inequity_score=30.0,
            paid_prioritization_harm_score=27.0,
            access_inequality_score=26.0,
            primary_pattern="access_inequality",
        ),
        NetNeutralityRightsEntity(
            entity_id="NNR-008",
            name="Chili/UE — Pionnier Neutralité 2010, BEREC Règlement 2015 Strict",
            country="Chili/UE",
            traffic_discrimination_score=8.0,
            zero_rating_inequity_score=7.0,
            paid_prioritization_harm_score=6.0,
            access_inequality_score=9.0,
            primary_pattern="traffic_discrimination",
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

    return NetNeutralityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_net_neutrality_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fcc_net_neutrality_restoration_order_2024",
            "berec_open_internet_regulation_eu_reports",
            "freedomhouse_internet_freedom_2024",
            "eff_net_neutrality_tracker_global",
            "itu_digital_inclusion_connectivity_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_net_neutrality_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
