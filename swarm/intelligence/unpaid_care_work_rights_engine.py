from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class UnpaidCareWorkRightsEntity:
    entity_id: str
    name: str
    country: str
    domestic_care_burden_gender_gap_score: float
    economic_recognition_unpaid_work_absence_score: float
    childcare_eldercare_infrastructure_gap_score: float
    pension_social_protection_care_exclusion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_unpaid_care_work_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.domestic_care_burden_gender_gap_score * 0.30
            + self.economic_recognition_unpaid_work_absence_score * 0.25
            + self.childcare_eldercare_infrastructure_gap_score * 0.25
            + self.pension_social_protection_care_exclusion_score * 0.20,
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
        self.estimated_unpaid_care_work_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class UnpaidCareWorkRightsEngineResult:
    agent: str = "Unpaid Care Work Rights Engine Agent"
    domain: str = "unpaid_care_work_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_unpaid_care_work_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[UnpaidCareWorkRightsEntity] = field(default_factory=list)

def run_unpaid_care_work_rights_engine() -> UnpaidCareWorkRightsEngineResult:
    entities = [
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-001",
            name="Inde — Femmes 5h/Jour Travail Care Non Rémunéré, Zéro Reconnaissance Légale & Retraite Nulle",
            country="Inde",
            domestic_care_burden_gender_gap_score=96.0,
            economic_recognition_unpaid_work_absence_score=92.0,
            childcare_eldercare_infrastructure_gap_score=91.0,
            pension_social_protection_care_exclusion_score=90.0,
            primary_pattern="domestic_care_burden_gender_gap",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-002",
            name="Afrique Sub-Saharienne — 6h Care Quotidien Non Comptabilisé, PIB Shadow Economy 40% & Exclusion Sociale",
            country="Afrique Sub-Saharienne",
            domestic_care_burden_gender_gap_score=93.0,
            economic_recognition_unpaid_work_absence_score=89.0,
            childcare_eldercare_infrastructure_gap_score=90.0,
            pension_social_protection_care_exclusion_score=86.0,
            primary_pattern="economic_recognition_unpaid_work_absence",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-003",
            name="Moyen-Orient — Travail Domestique Féminin Obligatoire, Zéro Politique Parentalité & Retraite Conditionnelle",
            country="Moyen-Orient",
            domestic_care_burden_gender_gap_score=91.0,
            economic_recognition_unpaid_work_absence_score=87.0,
            childcare_eldercare_infrastructure_gap_score=88.0,
            pension_social_protection_care_exclusion_score=84.0,
            primary_pattern="childcare_eldercare_infrastructure_gap",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-004",
            name="Asie du Sud-Est — Gap Care Genré 4:1, Infantilisation Travail Domestique & Pensions Familles Monoparentales",
            country="Asie du Sud-Est",
            domestic_care_burden_gender_gap_score=89.0,
            economic_recognition_unpaid_work_absence_score=85.0,
            childcare_eldercare_infrastructure_gap_score=86.0,
            pension_social_protection_care_exclusion_score=82.0,
            primary_pattern="domestic_care_burden_gender_gap",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-005",
            name="USA — 32h/Semaine Care Non Rémunéré Femmes, Congé Parental Insuffisant & Retraite Care Gap",
            country="États-Unis",
            domestic_care_burden_gender_gap_score=55.0,
            economic_recognition_unpaid_work_absence_score=53.0,
            childcare_eldercare_infrastructure_gap_score=52.0,
            pension_social_protection_care_exclusion_score=52.0,
            primary_pattern="pension_social_protection_care_exclusion",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-006",
            name="France/UE — Inégalité Care Résiduelle, Réforme Retraites Pénalise Carrières Interrompues & Crèches Insuffisantes",
            country="France/UE",
            domestic_care_burden_gender_gap_score=54.0,
            economic_recognition_unpaid_work_absence_score=51.0,
            childcare_eldercare_infrastructure_gap_score=52.0,
            pension_social_protection_care_exclusion_score=50.0,
            primary_pattern="childcare_eldercare_infrastructure_gap",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-007",
            name="ILO/Oxfam — Care Economy 10,8 Trilliards $/An, Politique Redistribution Travail & Plaidoyer Rémunération",
            country="Global",
            domestic_care_burden_gender_gap_score=22.0,
            economic_recognition_unpaid_work_absence_score=28.0,
            childcare_eldercare_infrastructure_gap_score=27.0,
            pension_social_protection_care_exclusion_score=30.0,
            primary_pattern="economic_recognition_unpaid_work_absence",
        ),
        UnpaidCareWorkRightsEntity(
            entity_id="UCW-008",
            name="ONU/CEDAW — Convention Discrimination Femmes, Résolution Care Economy & Recommandation Politique Sociale",
            country="Global",
            domestic_care_burden_gender_gap_score=4.0,
            economic_recognition_unpaid_work_absence_score=5.0,
            childcare_eldercare_infrastructure_gap_score=4.0,
            pension_social_protection_care_exclusion_score=5.0,
            primary_pattern="domestic_care_burden_gender_gap",
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

    return UnpaidCareWorkRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_unpaid_care_work_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "oxfam_time_to_care_unpaid_work_gender_global_report",
            "ilo_global_estimates_unpaid_care_work_wcms_report",
            "un_women_care_economy_invest_now_policy_brief",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_unpaid_care_work_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_unpaid_care_work_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
