from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class InformalEconomyRightsEntity:
    entity_id: str
    name: str
    country: str
    social_protection_exclusion_scale_score: float
    legal_status_vulnerability_severity_score: float
    workplace_safety_absence_pattern_score: float
    income_instability_poverty_trap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_informal_economy_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.social_protection_exclusion_scale_score * 0.30
            + self.legal_status_vulnerability_severity_score * 0.25
            + self.workplace_safety_absence_pattern_score * 0.25
            + self.income_instability_poverty_trap_score * 0.20,
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
        self.estimated_informal_economy_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class InformalEconomyRightsEngineResult:
    agent: str = "Informal Economy Rights Engine Agent"
    domain: str = "informal_economy_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_informal_economy_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[InformalEconomyRightsEntity] = field(default_factory=list)

def run_informal_economy_rights_engine() -> InformalEconomyRightsEngineResult:
    entities = [
        InformalEconomyRightsEntity(
            entity_id="IER-001",
            name="Inde — 90% Économie Informelle, 500M Travailleurs Sans Protection Sociale & Caste Emploi",
            country="Asie du Sud",
            social_protection_exclusion_scale_score=95.0,
            legal_status_vulnerability_severity_score=92.0,
            workplace_safety_absence_pattern_score=92.0,
            income_instability_poverty_trap_score=92.0,
            primary_pattern="social_protection_exclusion_scale",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-002",
            name="Bangladesh — 80% Emplois Informels, Usines Sans Contrat, Rana Plaza 2013 & Syndicats Interdits",
            country="Asie du Sud",
            social_protection_exclusion_scale_score=88.0,
            legal_status_vulnerability_severity_score=90.0,
            workplace_safety_absence_pattern_score=95.0,
            income_instability_poverty_trap_score=88.0,
            primary_pattern="workplace_safety_absence_pattern",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-003",
            name="Nigeria/Afrique Sub-Sah. — 85% Informel, Vendeurs Rue Expulsés, Zéro Assurance Chômage",
            country="Afrique de l'Ouest",
            social_protection_exclusion_scale_score=90.0,
            legal_status_vulnerability_severity_score=88.0,
            workplace_safety_absence_pattern_score=88.0,
            income_instability_poverty_trap_score=88.0,
            primary_pattern="social_protection_exclusion_scale",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-004",
            name="Pérou/Amérique Latine — 70% Informel, Micro-Commerce Femmes, Harcèlement Police & Précarité",
            country="Amérique Latine",
            social_protection_exclusion_scale_score=85.0,
            legal_status_vulnerability_severity_score=88.0,
            workplace_safety_absence_pattern_score=85.0,
            income_instability_poverty_trap_score=88.0,
            primary_pattern="income_instability_poverty_trap",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-005",
            name="Égypte/MENA — 40%+ Informel, Charbonniers/Pêcheurs Sans Contrat, Risques Chimiques & Chaleur",
            country="Moyen-Orient/Afrique du Nord",
            social_protection_exclusion_scale_score=52.0,
            legal_status_vulnerability_severity_score=55.0,
            workplace_safety_absence_pattern_score=55.0,
            income_instability_poverty_trap_score=50.0,
            primary_pattern="legal_status_vulnerability_severity",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-006",
            name="Mexique — 57% Informel, Travailleurs Domestiques Sans IMSS, Enfants Champs Agricoles & Précarité",
            country="Amérique Latine",
            social_protection_exclusion_scale_score=50.0,
            legal_status_vulnerability_severity_score=52.0,
            workplace_safety_absence_pattern_score=52.0,
            income_instability_poverty_trap_score=55.0,
            primary_pattern="income_instability_poverty_trap",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-007",
            name="WIEGO/StreetNet — Droits Travailleurs Informels, Collecte Données & Plaidoyer OIT Convention",
            country="Global",
            social_protection_exclusion_scale_score=22.0,
            legal_status_vulnerability_severity_score=28.0,
            workplace_safety_absence_pattern_score=25.0,
            income_instability_poverty_trap_score=30.0,
            primary_pattern="legal_status_vulnerability_severity",
        ),
        InformalEconomyRightsEntity(
            entity_id="IER-008",
            name="OIT/Convention C189 — Travailleurs Domestiques, SDG 8.3 Emploi Décent & Protection Sociale",
            country="Global",
            social_protection_exclusion_scale_score=4.0,
            legal_status_vulnerability_severity_score=5.0,
            workplace_safety_absence_pattern_score=3.0,
            income_instability_poverty_trap_score=6.0,
            primary_pattern="workplace_safety_absence_pattern",
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

    return InformalEconomyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_informal_economy_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "wiego_women_informal_employment_global_local_rights_report",
            "ilo_world_employment_social_outlook_informal_economy_2023",
            "streetnet_international_street_vendor_rights_monitoring",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_informal_economy_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_informal_economy_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
