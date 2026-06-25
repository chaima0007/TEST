from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EconomicDomesticAbuseEntity:
    entity_id: str
    name: str
    country: str
    financial_control_coercion_severity_score: float
    legal_economic_protection_absence_score: float
    asset_debt_exploitation_scale_score: float
    economic_recovery_support_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_economic_domestic_abuse_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.financial_control_coercion_severity_score * 0.30
            + self.legal_economic_protection_absence_score * 0.25
            + self.asset_debt_exploitation_scale_score * 0.25
            + self.economic_recovery_support_gap_score * 0.20,
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
        self.estimated_economic_domestic_abuse_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EconomicDomesticAbuseEngineResult:
    agent: str = "Economic Domestic Abuse Engine Agent"
    domain: str = "economic_domestic_abuse"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_economic_domestic_abuse_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EconomicDomesticAbuseEntity] = field(default_factory=list)

def run_economic_domestic_abuse_engine() -> EconomicDomesticAbuseEngineResult:
    entities = [
        EconomicDomesticAbuseEntity(
            entity_id="EDA-001",
            name="Afghanistan/Taliban — Interdiction Travail Femmes, Contrôle Total Finances & Zéro Recours Légal",
            country="Asie du Sud",
            financial_control_coercion_severity_score=95.0,
            legal_economic_protection_absence_score=95.0,
            asset_debt_exploitation_scale_score=92.0,
            economic_recovery_support_gap_score=92.0,
            primary_pattern="financial_control_coercion_severity",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-002",
            name="Arabie Saoudite/MENA — Tutelle Masculine, Compte Bloqué, Divorce Économique Impossible",
            country="Moyen-Orient",
            financial_control_coercion_severity_score=92.0,
            legal_economic_protection_absence_score=90.0,
            asset_debt_exploitation_scale_score=88.0,
            economic_recovery_support_gap_score=88.0,
            primary_pattern="legal_economic_protection_absence",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-003",
            name="USA — 99% Survivantes DV Subissent Abus Économique, 72% Restent Pour Raisons Financières",
            country="Amérique du Nord",
            financial_control_coercion_severity_score=88.0,
            legal_economic_protection_absence_score=88.0,
            asset_debt_exploitation_scale_score=88.0,
            economic_recovery_support_gap_score=88.0,
            primary_pattern="asset_debt_exploitation_scale",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-004",
            name="Afrique Sub-Sah. — Dot Piège Économique, Terres Au Nom Mari & Zéro Recours Légal",
            country="Afrique",
            financial_control_coercion_severity_score=85.0,
            legal_economic_protection_absence_score=88.0,
            asset_debt_exploitation_scale_score=85.0,
            economic_recovery_support_gap_score=88.0,
            primary_pattern="economic_recovery_support_gap",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-005",
            name="Inde — Dot Comme Levier de Contrôle, 70% Femmes Rurales Sans Compte Bancaire Personnel",
            country="Asie du Sud",
            financial_control_coercion_severity_score=52.0,
            legal_economic_protection_absence_score=55.0,
            asset_debt_exploitation_scale_score=55.0,
            economic_recovery_support_gap_score=50.0,
            primary_pattern="legal_economic_protection_absence",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-006",
            name="Amérique Latine/Brésil — Machisme Économique, Dépendance Forcée & Zéro Allocation Séparation",
            country="Amérique Latine",
            financial_control_coercion_severity_score=50.0,
            legal_economic_protection_absence_score=52.0,
            asset_debt_exploitation_scale_score=52.0,
            economic_recovery_support_gap_score=55.0,
            primary_pattern="economic_recovery_support_gap",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-007",
            name="Purple Purse/NNEDV — Indépendance Financière Survivantes, Programmes Refuges Économiques",
            country="Global",
            financial_control_coercion_severity_score=22.0,
            legal_economic_protection_absence_score=28.0,
            asset_debt_exploitation_scale_score=25.0,
            economic_recovery_support_gap_score=30.0,
            primary_pattern="financial_control_coercion_severity",
        ),
        EconomicDomesticAbuseEntity(
            entity_id="EDA-008",
            name="ONU Femmes/CEDAW — Art.16 Égalité Mariage/Divorce, SDG 5 Autonomisation Économique",
            country="Global",
            financial_control_coercion_severity_score=4.0,
            legal_economic_protection_absence_score=5.0,
            asset_debt_exploitation_scale_score=3.0,
            economic_recovery_support_gap_score=6.0,
            primary_pattern="asset_debt_exploitation_scale",
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

    return EconomicDomesticAbuseEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_economic_domestic_abuse_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "nnedv_purple_purse_financial_abuse_domestic_violence_report",
            "un_women_cedaw_economic_rights_intimate_partner_violence_review",
            "world_bank_women_property_rights_financial_inclusion_global_study",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_economic_domestic_abuse_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_economic_domestic_abuse_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
