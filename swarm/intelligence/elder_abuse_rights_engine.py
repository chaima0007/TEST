from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#a78bfa"


@dataclass
class ElderAbuseRightsEntity:
    entity_id: str
    name: str
    country: str
    physical_abuse_neglect_score: float
    financial_exploitation_score: float
    institutional_neglect_score: float
    legal_protection_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_elder_abuse_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.physical_abuse_neglect_score * 0.30
            + self.financial_exploitation_score * 0.25
            + self.institutional_neglect_score * 0.25
            + self.legal_protection_gap_score * 0.20,
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
        self.estimated_elder_abuse_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ElderAbuseRightsEngineResult:
    agent: str = "Elder Abuse Rights Engine Agent"
    domain: str = "elder_abuse_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_elder_abuse_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ElderAbuseRightsEntity] = field(default_factory=list)


def run_elder_abuse_rights_engine() -> ElderAbuseRightsEngineResult:
    entities = [
        ElderAbuseRightsEntity(
            entity_id="EAR-001",
            name="Chine",
            country="Chine",
            physical_abuse_neglect_score=96.0,
            financial_exploitation_score=92.0,
            institutional_neglect_score=94.0,
            legal_protection_gap_score=93.0,
            primary_pattern="unregulated_private_care_facilities",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-002",
            name="Inde",
            country="Inde",
            physical_abuse_neglect_score=89.0,
            financial_exploitation_score=87.0,
            institutional_neglect_score=85.0,
            legal_protection_gap_score=91.0,
            primary_pattern="family_abandonment_pension_gap",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-003",
            name="Russie",
            country="Russie",
            physical_abuse_neglect_score=83.0,
            financial_exploitation_score=84.0,
            institutional_neglect_score=80.0,
            legal_protection_gap_score=82.0,
            primary_pattern="oligarchy_pension_capture",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-004",
            name="Brésil",
            country="Brésil",
            physical_abuse_neglect_score=78.0,
            financial_exploitation_score=74.0,
            institutional_neglect_score=76.0,
            legal_protection_gap_score=75.0,
            primary_pattern="domestic_violence_underreporting",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-005",
            name="États-Unis",
            country="USA",
            physical_abuse_neglect_score=55.0,
            financial_exploitation_score=58.0,
            institutional_neglect_score=52.0,
            legal_protection_gap_score=50.0,
            primary_pattern="financial_exploitation_scale",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-006",
            name="Espagne & Italie",
            country="Espagne/Italie",
            physical_abuse_neglect_score=46.0,
            financial_exploitation_score=44.0,
            institutional_neglect_score=49.0,
            legal_protection_gap_score=43.0,
            primary_pattern="nursing_home_covid_scandal",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-007",
            name="France",
            country="France",
            physical_abuse_neglect_score=30.0,
            financial_exploitation_score=29.0,
            institutional_neglect_score=32.0,
            legal_protection_gap_score=28.0,
            primary_pattern="orpea_scandal_reform_underway",
        ),
        ElderAbuseRightsEntity(
            entity_id="EAR-008",
            name="Pays-Bas",
            country="Pays-Bas",
            physical_abuse_neglect_score=11.0,
            financial_exploitation_score=13.0,
            institutional_neglect_score=10.0,
            legal_protection_gap_score=14.0,
            primary_pattern="care_at_home_community_model",
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

    return ElderAbuseRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_elder_abuse_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_global_report_ageism_elder_abuse_2021",
            "un_open_ended_working_group_ageing_reports",
            "hrw_elder_abuse_nursing_homes_global",
            "inpea_international_elder_abuse_awareness_data",
            "oecd_long_term_care_quality_standards_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_elder_abuse_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
