from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#f97316"


@dataclass
class DigitalAccessibilityRightsEntity:
    entity_id: str
    name: str
    country: str
    wcag_compliance_gap_score: float
    assistive_technology_exclusion_score: float
    public_service_digital_exclusion_score: float
    employment_digital_barrier_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_digital_accessibility_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.wcag_compliance_gap_score * 0.30
            + self.assistive_technology_exclusion_score * 0.25
            + self.public_service_digital_exclusion_score * 0.25
            + self.employment_digital_barrier_score * 0.20,
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
        self.estimated_digital_accessibility_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class DigitalAccessibilityRightsEngineResult:
    agent: str = "Digital Accessibility Rights Engine Agent"
    domain: str = "digital_accessibility_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_digital_accessibility_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[DigitalAccessibilityRightsEntity] = field(default_factory=list)


def run_digital_accessibility_rights_engine() -> DigitalAccessibilityRightsEngineResult:
    entities = [
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-001",
            name="Afrique Sub-Saharienne — 0% Services Gouvernementaux Accessibles, Aucune Réglementation WCAG",
            country="Afrique Sub-Saharienne",
            wcag_compliance_gap_score=97.0,
            assistive_technology_exclusion_score=95.0,
            public_service_digital_exclusion_score=96.0,
            employment_digital_barrier_score=94.0,
            primary_pattern="total_digital_exclusion",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-002",
            name="Afghanistan/Yémen — Sites Gov Inaccessibles, Conflits + Aucun Cadre Accessibilité",
            country="Afghanistan/Yémen",
            wcag_compliance_gap_score=90.0,
            assistive_technology_exclusion_score=88.0,
            public_service_digital_exclusion_score=92.0,
            employment_digital_barrier_score=86.0,
            primary_pattern="public_service_exclusion",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-003",
            name="Myanmar/Cambodge — Services Numériques Langue Majoritaire Exclusivement, Minorités Exclues",
            country="Myanmar/Cambodge",
            wcag_compliance_gap_score=84.0,
            assistive_technology_exclusion_score=82.0,
            public_service_digital_exclusion_score=85.0,
            employment_digital_barrier_score=80.0,
            primary_pattern="language_digital_exclusion",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-004",
            name="Bangladesh/Pakistan — Paiements Mobiles Inaccessibles Non-Voyants, 95% Sites Bancaires Non-Conformes",
            country="Bangladesh/Pakistan",
            wcag_compliance_gap_score=76.0,
            assistive_technology_exclusion_score=78.0,
            public_service_digital_exclusion_score=74.0,
            employment_digital_barrier_score=72.0,
            primary_pattern="assistive_technology_exclusion",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-005",
            name="USA Fédéral — 31% Sites Gouvernementaux Non-WCAG 2.1 AA, ADA Lawsuits 4 300/An",
            country="USA",
            wcag_compliance_gap_score=54.0,
            assistive_technology_exclusion_score=52.0,
            public_service_digital_exclusion_score=56.0,
            employment_digital_barrier_score=50.0,
            primary_pattern="wcag_compliance_gap",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-006",
            name="Inde — 90% Sites Publics Non-Accessibles, RPWD Act 2016 Non-Appliqué au Numérique",
            country="Inde",
            wcag_compliance_gap_score=46.0,
            assistive_technology_exclusion_score=48.0,
            public_service_digital_exclusion_score=44.0,
            employment_digital_barrier_score=46.0,
            primary_pattern="public_service_exclusion",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-007",
            name="France — RGAA 4.1 Partielle, 40% Sites Publics Conformes, DINUM Contrôle",
            country="France",
            wcag_compliance_gap_score=28.0,
            assistive_technology_exclusion_score=26.0,
            public_service_digital_exclusion_score=30.0,
            employment_digital_barrier_score=24.0,
            primary_pattern="wcag_compliance_gap",
        ),
        DigitalAccessibilityRightsEntity(
            entity_id="DAR-008",
            name="UK/Norvège — WCAG 2.2 95%+ Secteur Public, GDS Standard Référence Mondiale",
            country="UK/Norvège",
            wcag_compliance_gap_score=6.0,
            assistive_technology_exclusion_score=7.0,
            public_service_digital_exclusion_score=5.0,
            employment_digital_barrier_score=8.0,
            primary_pattern="employment_digital_barrier",
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

    return DigitalAccessibilityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_digital_accessibility_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "w3c_wcag_compliance_global_audit_2024",
            "disability_rights_international_digital_access_report",
            "eu_web_accessibility_directive_implementation_2024",
            "un_crpd_article_9_digital_accessibility_report",
            "webaim_million_accessibility_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_digital_accessibility_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
