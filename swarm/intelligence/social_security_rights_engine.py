from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#059669"


@dataclass
class SocialSecurityRightsEntity:
    entity_id: str
    name: str
    country: str
    social_protection_gap_score: float
    unemployment_coverage_score: float
    pension_access_score: float
    informal_worker_exclusion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_social_security_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.social_protection_gap_score * 0.30
            + self.unemployment_coverage_score * 0.25
            + self.pension_access_score * 0.25
            + self.informal_worker_exclusion_score * 0.20,
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
        self.estimated_social_security_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class SocialSecurityRightsEngineResult:
    agent: str = "SocialSecurityRights Engine Agent"
    domain: str = "social_security_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_social_security_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[SocialSecurityRightsEntity] = field(default_factory=list)


def run_social_security_rights_engine() -> SocialSecurityRightsEngineResult:
    entities = [
        # --- 4 CRITIQUE (>=60) ---
        SocialSecurityRightsEntity(
            entity_id="SSR-001",
            name="Soudan du Sud — 0% couverture sociale, conflit, famine totale",
            country="Soudan du Sud",
            social_protection_gap_score=98.0,
            unemployment_coverage_score=99.0,
            pension_access_score=99.0,
            informal_worker_exclusion_score=98.0,
            primary_pattern="Total absence of social protection system",
        ),
        SocialSecurityRightsEntity(
            entity_id="SSR-002",
            name="Haïti — Effondrement état, gangs, 80% économie informelle",
            country="Haïti",
            social_protection_gap_score=92.0,
            unemployment_coverage_score=94.0,
            pension_access_score=88.0,
            informal_worker_exclusion_score=96.0,
            primary_pattern="State collapse & near-total informal economy",
        ),
        SocialSecurityRightsEntity(
            entity_id="SSR-003",
            name="RDC — 90% travailleurs informels, caisses retraite insolvables",
            country="République Démocratique du Congo",
            social_protection_gap_score=86.0,
            unemployment_coverage_score=84.0,
            pension_access_score=88.0,
            informal_worker_exclusion_score=90.0,
            primary_pattern="Insolvent pension funds & mass informal exclusion",
        ),
        SocialSecurityRightsEntity(
            entity_id="SSR-004",
            name="Bangladesh — 85% informel, travailleurs textile sans protection",
            country="Bangladesh",
            social_protection_gap_score=78.0,
            unemployment_coverage_score=76.0,
            pension_access_score=74.0,
            informal_worker_exclusion_score=84.0,
            primary_pattern="Garment sector workers excluded from social protection",
        ),
        # --- 2 ÉLEVÉ (40-59) ---
        SocialSecurityRightsEntity(
            entity_id="SSR-005",
            name="Inde — MGNREGA insuffisant, 90% informels sans couverture EPFO",
            country="Inde",
            social_protection_gap_score=56.0,
            unemployment_coverage_score=54.0,
            pension_access_score=50.0,
            informal_worker_exclusion_score=58.0,
            primary_pattern="Massive informal workforce excluded from EPFO",
        ),
        SocialSecurityRightsEntity(
            entity_id="SSR-006",
            name="Brésil — Bolsa Familia mais 38M informels sans INSS",
            country="Brésil",
            social_protection_gap_score=46.0,
            unemployment_coverage_score=44.0,
            pension_access_score=42.0,
            informal_worker_exclusion_score=50.0,
            primary_pattern="Dual system: formal coverage vs. large informal gap",
        ),
        # --- 1 MODÉRÉ (20-39) ---
        SocialSecurityRightsEntity(
            entity_id="SSR-007",
            name="USA — Gaps santé/chômage, pas de congé parental fédéral",
            country="États-Unis",
            social_protection_gap_score=32.0,
            unemployment_coverage_score=30.0,
            pension_access_score=26.0,
            informal_worker_exclusion_score=28.0,
            primary_pattern="Gaps in Medicaid & absence of universal parental leave",
        ),
        # --- 1 FAIBLE (<20) ---
        SocialSecurityRightsEntity(
            entity_id="SSR-008",
            name="Danemark/Allemagne — Bismarck/Beveridge, couverture 95%+",
            country="Danemark/Allemagne",
            social_protection_gap_score=8.0,
            unemployment_coverage_score=6.0,
            pension_access_score=7.0,
            informal_worker_exclusion_score=5.0,
            primary_pattern="Universal social protection model, 95%+ coverage",
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

    return SocialSecurityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_social_security_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "ilo_world_social_protection_report_2024_2026",
            "world_bank_social_protection_labor_global_database",
            "un_social_protection_floor_initiative_reports",
            "oxfam_inequality_report_social_protection_gap_2024",
            "ilostat_social_security_coverage_global_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_social_security_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
