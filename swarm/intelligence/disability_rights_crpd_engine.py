from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0891b2"


@dataclass
class DisabilityRightsCrpdEntity:
    entity_id: str
    name: str
    country: str
    crpd_implementation_gap_score: float
    institutional_segregation_score: float
    employment_exclusion_score: float
    legal_capacity_denial_crpd_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_disability_rights_crpd_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.crpd_implementation_gap_score * 0.30
            + self.institutional_segregation_score * 0.25
            + self.employment_exclusion_score * 0.25
            + self.legal_capacity_denial_crpd_score * 0.20,
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
        self.estimated_disability_rights_crpd_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class DisabilityRightsCrpdEngineResult:
    agent: str = "Disability Rights CRPD Engine Agent"
    domain: str = "disability_rights_crpd"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_disability_rights_crpd_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DisabilityRightsCrpdEntity] = field(default_factory=list)


def run_disability_rights_crpd_engine() -> DisabilityRightsCrpdEngineResult:
    entities = [
        DisabilityRightsCrpdEntity(
            entity_id="DRC-001",
            name="Russie — Internats psychiatriques 156 000 personnes, stérilisation forcée, CRPD non-respectée",
            country="Russie",
            crpd_implementation_gap_score=96.0,
            institutional_segregation_score=95.0,
            employment_exclusion_score=93.0,
            legal_capacity_denial_crpd_score=94.0,
            primary_pattern="institutional_segregation",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-002",
            name="Indonésie — Pasung (chaînes), 57 000 personnes handicapées mentales enchaînées légalement",
            country="Indonésie",
            crpd_implementation_gap_score=90.0,
            institutional_segregation_score=92.0,
            employment_exclusion_score=88.0,
            legal_capacity_denial_crpd_score=89.0,
            primary_pattern="institutional_segregation",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-003",
            name="Inde — Institutions résidentielles 800 000 personnes, tutelle totale sans recours",
            country="Inde",
            crpd_implementation_gap_score=84.0,
            institutional_segregation_score=86.0,
            employment_exclusion_score=82.0,
            legal_capacity_denial_crpd_score=80.0,
            primary_pattern="legal_capacity_denial_crpd",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-004",
            name="Afrique Sub-Saharienne — 0% CRPD appliqué, chasse sorcières albinos, exclusion totale",
            country="Afrique Sub-Saharienne",
            crpd_implementation_gap_score=76.0,
            institutional_segregation_score=74.0,
            employment_exclusion_score=78.0,
            legal_capacity_denial_crpd_score=72.0,
            primary_pattern="crpd_implementation_gap",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-005",
            name="USA — ADA partiel, 70% personnes handicapées sans emploi, Olmstead non-appliqué",
            country="USA",
            crpd_implementation_gap_score=57.0,
            institutional_segregation_score=54.0,
            employment_exclusion_score=60.0,
            legal_capacity_denial_crpd_score=52.0,
            primary_pattern="employment_exclusion",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-006",
            name="Chine — CRPD ratifiée 2008, application zéro, 85M handicapés sans protection réelle",
            country="Chine",
            crpd_implementation_gap_score=48.0,
            institutional_segregation_score=50.0,
            employment_exclusion_score=46.0,
            legal_capacity_denial_crpd_score=52.0,
            primary_pattern="crpd_implementation_gap",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-007",
            name="France — ESAT dérogation SMIC, accessibilité retardée 20 ans, CDAPH lenteur",
            country="France",
            crpd_implementation_gap_score=28.0,
            institutional_segregation_score=26.0,
            employment_exclusion_score=30.0,
            legal_capacity_denial_crpd_score=24.0,
            primary_pattern="employment_exclusion",
        ),
        DisabilityRightsCrpdEntity(
            entity_id="DRC-008",
            name="Suède/Finlande — CRPD pleinement appliqué, vie indépendante, emploi 60%+ handicapés",
            country="Suède/Finlande",
            crpd_implementation_gap_score=6.0,
            institutional_segregation_score=7.0,
            employment_exclusion_score=5.0,
            legal_capacity_denial_crpd_score=8.0,
            primary_pattern="crpd_implementation_gap",
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

    return DisabilityRightsCrpdEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_disability_rights_crpd_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "crpd_committee_state_party_reviews_2024",
            "disability_rights_international_global_report",
            "hrw_disability_rights_institutions_2024",
            "un_special_rapporteur_disability_report_2024",
            "ila_disability_rights_employment_global_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_disability_rights_crpd_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
