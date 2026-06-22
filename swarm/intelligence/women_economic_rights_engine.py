from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#db2777"


@dataclass
class WomenEconomicRightsEntity:
    entity_id: str
    name: str
    country: str
    property_rights_gap_score: float
    equal_pay_gap_score: float
    financial_exclusion_score: float
    legal_employment_barriers_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_women_economic_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.property_rights_gap_score * 0.30
            + self.equal_pay_gap_score * 0.25
            + self.financial_exclusion_score * 0.25
            + self.legal_employment_barriers_score * 0.20,
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
        self.estimated_women_economic_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class WomenEconomicRightsEngineResult:
    agent: str = "Women Economic Rights Engine Agent"
    domain: str = "women_economic_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_women_economic_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[WomenEconomicRightsEntity] = field(default_factory=list)


def run_women_economic_rights_engine() -> WomenEconomicRightsEngineResult:
    entities = [
        WomenEconomicRightsEntity(
            entity_id="WER-001",
            name="Afghanistan — Taliban interdiction travail femmes, 100% emplois perdus 2021",
            country="Afghanistan",
            property_rights_gap_score=97.0,
            equal_pay_gap_score=96.0,
            financial_exclusion_score=98.0,
            legal_employment_barriers_score=97.0,
            primary_pattern="legal_employment_barriers",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-002",
            name="Yémen — Conflit détruit économie femmes, garde-chiourme, 80% emplois informels perdus",
            country="Yémen",
            property_rights_gap_score=90.0,
            equal_pay_gap_score=88.0,
            financial_exclusion_score=91.0,
            legal_employment_barriers_score=89.0,
            primary_pattern="financial_exclusion",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-003",
            name="Soudan/Sahel — Lois personnelles discriminatoires, héritage 1/2 part, banques interdites",
            country="Soudan/Sahel",
            property_rights_gap_score=84.0,
            equal_pay_gap_score=82.0,
            financial_exclusion_score=85.0,
            legal_employment_barriers_score=80.0,
            primary_pattern="property_rights_gap",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-004",
            name="Pakistan — Loi héritages islamiques, propriétaires foncières 3%, banque 7% femmes",
            country="Pakistan",
            property_rights_gap_score=76.0,
            equal_pay_gap_score=74.0,
            financial_exclusion_score=78.0,
            legal_employment_barriers_score=72.0,
            primary_pattern="property_rights_gap",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-005",
            name="Inde — Écart salaire 28%, successions rurales bafouées, accès microcrédit limité",
            country="Inde",
            property_rights_gap_score=57.0,
            equal_pay_gap_score=58.0,
            financial_exclusion_score=56.0,
            legal_employment_barriers_score=56.0,
            primary_pattern="equal_pay_gap",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-006",
            name="Nigéria — Lois coutumières héritages, écart salaire 35%, secteur informel 90% femmes",
            country="Nigéria",
            property_rights_gap_score=46.0,
            equal_pay_gap_score=48.0,
            financial_exclusion_score=50.0,
            legal_employment_barriers_score=44.0,
            primary_pattern="equal_pay_gap",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-007",
            name="USA — Écart salaire 18%, Glass ceiling Fortune 500, congé maternité non-fédéral",
            country="USA",
            property_rights_gap_score=26.0,
            equal_pay_gap_score=30.0,
            financial_exclusion_score=24.0,
            legal_employment_barriers_score=22.0,
            primary_pattern="equal_pay_gap",
        ),
        WomenEconomicRightsEntity(
            entity_id="WER-008",
            name="Islande/Suède — Égalité salariale certifiée, parité CA 40%+, congé parental 50/50",
            country="Islande/Suède",
            property_rights_gap_score=6.0,
            equal_pay_gap_score=7.0,
            financial_exclusion_score=5.0,
            legal_employment_barriers_score=8.0,
            primary_pattern="legal_employment_barriers",
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

    return WomenEconomicRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_women_economic_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "world_bank_women_business_law_report_2024",
            "ilo_gender_pay_gap_global_2024",
            "wef_global_gender_gap_report_2024",
            "un_women_economic_empowerment_report",
            "oxfam_women_economic_rights_violations_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_women_economic_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
