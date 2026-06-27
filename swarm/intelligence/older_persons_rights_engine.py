from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class OlderPersonsRightsEntity:
    entity_id: str
    name: str
    country: str
    elder_abuse_neglect_institution_severity_score: float
    age_discrimination_employment_exclusion_scale_score: float
    pension_social_protection_adequacy_gap_score: float
    healthcare_long_term_care_access_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_older_persons_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.elder_abuse_neglect_institution_severity_score * 0.30
            + self.age_discrimination_employment_exclusion_scale_score * 0.25
            + self.pension_social_protection_adequacy_gap_score * 0.25
            + self.healthcare_long_term_care_access_barrier_score * 0.20,
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
        self.estimated_older_persons_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class OlderPersonsRightsEngineResult:
    agent: str = "Older Persons Rights Engine Agent"
    domain: str = "older_persons_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_older_persons_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[OlderPersonsRightsEntity] = field(default_factory=list)

def run_older_persons_rights_engine() -> OlderPersonsRightsEngineResult:
    entities = [
        OlderPersonsRightsEntity(
            entity_id="OPR-001",
            name="Inde — 104M Personnes Âgées, Violence Familiale 60%, Abandon Centres & Zéro Pension Universelle",
            country="Inde",
            elder_abuse_neglect_institution_severity_score=95.0,
            age_discrimination_employment_exclusion_scale_score=93.0,
            pension_social_protection_adequacy_gap_score=92.0,
            healthcare_long_term_care_access_barrier_score=91.0,
            primary_pattern="elder_abuse_neglect_institution_severity",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-002",
            name="Afrique Sub-Saharienne — Accusations Sorcellerie Personnes Âgées, Expulsions Terres & Zéro Soins Long Terme",
            country="Afrique Sub-Saharienne",
            elder_abuse_neglect_institution_severity_score=92.0,
            age_discrimination_employment_exclusion_scale_score=89.0,
            pension_social_protection_adequacy_gap_score=90.0,
            healthcare_long_term_care_access_barrier_score=87.0,
            primary_pattern="elder_abuse_neglect_institution_severity",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-003",
            name="Chine — 260M +60 Ans, Discrimination Emploi, Soins EHPAD Sous-Financés & Abandon Rural",
            country="Chine",
            elder_abuse_neglect_institution_severity_score=89.0,
            age_discrimination_employment_exclusion_scale_score=87.0,
            pension_social_protection_adequacy_gap_score=86.0,
            healthcare_long_term_care_access_barrier_score=84.0,
            primary_pattern="age_discrimination_employment_exclusion_scale",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-004",
            name="Russie/Europe Est — Retraites Insuffisantes, Institutions Soviétiques, Violence Abus Non Signalés",
            country="Russie/Europe Est",
            elder_abuse_neglect_institution_severity_score=86.0,
            age_discrimination_employment_exclusion_scale_score=84.0,
            pension_social_protection_adequacy_gap_score=83.0,
            healthcare_long_term_care_access_barrier_score=82.0,
            primary_pattern="pension_social_protection_adequacy_gap",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-005",
            name="USA — Nursing Homes Covid 130k Morts, Abus Financier Tuteurs & Age Discrimination Emploi",
            country="USA",
            elder_abuse_neglect_institution_severity_score=55.0,
            age_discrimination_employment_exclusion_scale_score=53.0,
            pension_social_protection_adequacy_gap_score=51.0,
            healthcare_long_term_care_access_barrier_score=52.0,
            primary_pattern="elder_abuse_neglect_institution_severity",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-006",
            name="Japon — Hyper-Vieillissement, Karoshi Retraités Travailleurs, Isolement & Soins Famille Épuisement",
            country="Japon",
            elder_abuse_neglect_institution_severity_score=53.0,
            age_discrimination_employment_exclusion_scale_score=51.0,
            pension_social_protection_adequacy_gap_score=49.0,
            healthcare_long_term_care_access_barrier_score=50.0,
            primary_pattern="age_discrimination_employment_exclusion_scale",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-007",
            name="HelpAge International/IFA — Droits Seniors, Plaidoyer Convention ONU & Standards Madrid Plan",
            country="Global",
            elder_abuse_neglect_institution_severity_score=27.0,
            age_discrimination_employment_exclusion_scale_score=26.0,
            pension_social_protection_adequacy_gap_score=25.0,
            healthcare_long_term_care_access_barrier_score=26.0,
            primary_pattern="elder_abuse_neglect_institution_severity",
        ),
        OlderPersonsRightsEntity(
            entity_id="OPR-008",
            name="ONU/Plan Madrid 2002 — Plan International Vieillissement, MIPAA & SDG 3.8 Couverture Santé Universelle",
            country="Global",
            elder_abuse_neglect_institution_severity_score=4.0,
            age_discrimination_employment_exclusion_scale_score=4.0,
            pension_social_protection_adequacy_gap_score=5.0,
            healthcare_long_term_care_access_barrier_score=4.0,
            primary_pattern="pension_social_protection_adequacy_gap",
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

    return OlderPersonsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_older_persons_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "helpage_international_global_agewatch_index",
            "who_global_report_ageism_abuse_older_persons",
            "un_mipaa_madrid_international_plan_ageing_2002",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_older_persons_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_older_persons_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
