from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class GenderPayGapEntity:
    entity_id: str
    name: str
    country: str
    wage_discrimination_scale_score: float
    occupational_segregation_score: float
    unpaid_care_work_burden_score: float
    legal_enforcement_transparency_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_gender_pay_gap_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.wage_discrimination_scale_score * 0.30
            + self.occupational_segregation_score * 0.25
            + self.unpaid_care_work_burden_score * 0.25
            + self.legal_enforcement_transparency_gap_score * 0.20,
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
        self.estimated_gender_pay_gap_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class GenderPayGapEngineResult:
    agent: str = "Gender Pay Gap Engine Agent"
    domain: str = "gender_pay_gap"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_gender_pay_gap_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[GenderPayGapEntity] = field(default_factory=list)

def run_gender_pay_gap_engine() -> GenderPayGapEngineResult:
    entities = [
        GenderPayGapEntity(
            entity_id="GP-001",
            name="Pakistan/Asie Sud — Écart 51%, Exclusion Marché Travail & Travail Domestique Non Rémunéré",
            country="Asie du Sud",
            wage_discrimination_scale_score=95.0,
            occupational_segregation_score=92.0,
            unpaid_care_work_burden_score=95.0,
            legal_enforcement_transparency_gap_score=90.0,
            primary_pattern="unpaid_care_work_burden",
        ),
        GenderPayGapEntity(
            entity_id="GP-002",
            name="Afrique Sub-Saharienne — Secteur Informel Féminin 90%, Zéro Protection Sociale & Écarts Massifs",
            country="Afrique Sub-Saharienne",
            wage_discrimination_scale_score=90.0,
            occupational_segregation_score=88.0,
            unpaid_care_work_burden_score=92.0,
            legal_enforcement_transparency_gap_score=88.0,
            primary_pattern="unpaid_care_work_burden",
        ),
        GenderPayGapEntity(
            entity_id="GP-003",
            name="Moyen-Orient — Participation Féminine 20%, Gardiennage Masculin & Discriminations Légales",
            country="Moyen-Orient",
            wage_discrimination_scale_score=88.0,
            occupational_segregation_score=90.0,
            unpaid_care_work_burden_score=85.0,
            legal_enforcement_transparency_gap_score=88.0,
            primary_pattern="occupational_segregation",
        ),
        GenderPayGapEntity(
            entity_id="GP-004",
            name="Corée du Sud/Japon — Écart 30-31%, Plafond Verre Corporate & Démission Mariage Culturelle",
            country="Asie du Nord-Est",
            wage_discrimination_scale_score=82.0,
            occupational_segregation_score=85.0,
            unpaid_care_work_burden_score=82.0,
            legal_enforcement_transparency_gap_score=80.0,
            primary_pattern="occupational_segregation",
        ),
        GenderPayGapEntity(
            entity_id="GP-005",
            name="USA — Écart 18%, Motherhood Penalty, Négociation Salariale Biaisée & Secteurs Ségrégués",
            country="Amérique du Nord",
            wage_discrimination_scale_score=52.0,
            occupational_segregation_score=55.0,
            unpaid_care_work_burden_score=58.0,
            legal_enforcement_transparency_gap_score=50.0,
            primary_pattern="wage_discrimination_scale",
        ),
        GenderPayGapEntity(
            entity_id="GP-006",
            name="UE — Directive Transparence Salariale 2023, Écart Moyen 13% & Application Inégale États",
            country="Europe",
            wage_discrimination_scale_score=48.0,
            occupational_segregation_score=52.0,
            unpaid_care_work_burden_score=50.0,
            legal_enforcement_transparency_gap_score=48.0,
            primary_pattern="legal_enforcement_transparency_gap",
        ),
        GenderPayGapEntity(
            entity_id="GP-007",
            name="Equal Pay International Coalition — OIT/ONU/ONU Femmes, Objectif 2030 & Plaidoyer Global",
            country="Global",
            wage_discrimination_scale_score=22.0,
            occupational_segregation_score=25.0,
            unpaid_care_work_burden_score=28.0,
            legal_enforcement_transparency_gap_score=30.0,
            primary_pattern="wage_discrimination_scale",
        ),
        GenderPayGapEntity(
            entity_id="GP-008",
            name="ONU/CEDAW — Convention Élimination Discriminations Femmes, Comité & Protocole Facultatif",
            country="Global",
            wage_discrimination_scale_score=4.0,
            occupational_segregation_score=5.0,
            unpaid_care_work_burden_score=3.0,
            legal_enforcement_transparency_gap_score=6.0,
            primary_pattern="legal_enforcement_transparency_gap",
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

    return GenderPayGapEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_gender_pay_gap_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_global_wage_report_gender_pay_gap_analysis",
            "world_economic_forum_global_gender_gap_report",
            "eu_directive_pay_transparency_implementation_review_2024",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_gender_pay_gap_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_gender_pay_gap_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
