from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class GigEconomyRightsEntity:
    entity_id: str
    name: str
    country: str
    algorithmic_wage_theft_control_severity_score: float
    zero_hours_contract_precarity_scale_score: float
    social_protection_gig_worker_exclusion_score: float
    platform_misclassification_labor_rights_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_gig_economy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.algorithmic_wage_theft_control_severity_score * 0.30
            + self.zero_hours_contract_precarity_scale_score * 0.25
            + self.social_protection_gig_worker_exclusion_score * 0.25
            + self.platform_misclassification_labor_rights_gap_score * 0.20,
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
        self.estimated_gig_economy_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class GigEconomyRightsEngineResult:
    agent: str = "Gig Economy Rights Engine Agent"
    domain: str = "gig_economy_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_gig_economy_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[GigEconomyRightsEntity] = field(default_factory=list)

def run_gig_economy_rights_engine() -> GigEconomyRightsEngineResult:
    entities = [
        GigEconomyRightsEntity(
            entity_id="GER-001",
            name="UK/Deliveroo-Uber — 5,5M Travailleurs Plateforme, Algorithme Salaire, Zéro Congés Payés & Accidents Non Couverts",
            country="Royaume-Uni",
            algorithmic_wage_theft_control_severity_score=95.0,
            zero_hours_contract_precarity_scale_score=93.0,
            social_protection_gig_worker_exclusion_score=92.0,
            platform_misclassification_labor_rights_gap_score=91.0,
            primary_pattern="algorithmic_wage_theft_control_severity",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-002",
            name="India/Ola-Swiggy — 7,7M Livreurs Sans Statut, Désactivation Arbitraire & Absence Sécurité Sociale",
            country="Inde",
            algorithmic_wage_theft_control_severity_score=92.0,
            zero_hours_contract_precarity_scale_score=90.0,
            social_protection_gig_worker_exclusion_score=89.0,
            platform_misclassification_labor_rights_gap_score=88.0,
            primary_pattern="platform_misclassification_labor_rights_gap",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-003",
            name="USA/Amazon-DoorDash — Prop 22 Californie, Déclassification Délibérée & Accidentés Sans Indemnisation",
            country="États-Unis",
            algorithmic_wage_theft_control_severity_score=89.0,
            zero_hours_contract_precarity_scale_score=87.0,
            social_protection_gig_worker_exclusion_score=86.0,
            platform_misclassification_labor_rights_gap_score=85.0,
            primary_pattern="platform_misclassification_labor_rights_gap",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-004",
            name="Afrique Sub-Saharienne — Jumia/SafeBoda, Zéro Protection Légale, Risques Sécurité Routière & Exploitation",
            country="Afrique Sub-Saharienne",
            algorithmic_wage_theft_control_severity_score=86.0,
            zero_hours_contract_precarity_scale_score=84.0,
            social_protection_gig_worker_exclusion_score=83.0,
            platform_misclassification_labor_rights_gap_score=82.0,
            primary_pattern="social_protection_gig_worker_exclusion",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-005",
            name="EU/Directive Plateforme — Directive 2024 Implémentation Lente, États Résistants & Protection Partielle",
            country="Union Européenne",
            algorithmic_wage_theft_control_severity_score=55.0,
            zero_hours_contract_precarity_scale_score=53.0,
            social_protection_gig_worker_exclusion_score=52.0,
            platform_misclassification_labor_rights_gap_score=51.0,
            primary_pattern="algorithmic_wage_theft_control_severity",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-006",
            name="Asie du Sud-Est/Grab — Reclassification Refusée, Heures Excessives & Discrimination Algorithme",
            country="Asie du Sud-Est",
            algorithmic_wage_theft_control_severity_score=53.0,
            zero_hours_contract_precarity_scale_score=51.0,
            social_protection_gig_worker_exclusion_score=50.0,
            platform_misclassification_labor_rights_gap_score=49.0,
            primary_pattern="algorithmic_wage_theft_control_severity",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-007",
            name="ITUC/UNI Global — Droits Travailleurs Plateforme, Campagne Justice Numérique & Standards OIT",
            country="Global",
            algorithmic_wage_theft_control_severity_score=27.0,
            zero_hours_contract_precarity_scale_score=26.0,
            social_protection_gig_worker_exclusion_score=25.0,
            platform_misclassification_labor_rights_gap_score=26.0,
            primary_pattern="social_protection_gig_worker_exclusion",
        ),
        GigEconomyRightsEntity(
            entity_id="GER-008",
            name="OIT/Recommandation — R198 Relation Travail, Platerforme Work Directive & SDG 8.8 Droits Travailleurs",
            country="Global",
            algorithmic_wage_theft_control_severity_score=4.0,
            zero_hours_contract_precarity_scale_score=4.0,
            social_protection_gig_worker_exclusion_score=4.0,
            platform_misclassification_labor_rights_gap_score=4.0,
            primary_pattern="algorithmic_wage_theft_control_severity",
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

    return GigEconomyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_gig_economy_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ilo_platform_work_and_decent_work_report",
            "ituc_gig_economy_workers_rights_survey",
            "oxford_internet_institute_platform_labour_index",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_gig_economy_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_gig_economy_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
