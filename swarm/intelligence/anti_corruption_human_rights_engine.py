from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#b45309"


@dataclass
class AntiCorruptionHumanRightsEntity:
    entity_id: str
    name: str
    country: str
    public_resource_embezzlement_score: float
    judicial_corruption_score: float
    impunity_of_officials_score: float
    civil_society_repression_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_anti_corruption_human_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.public_resource_embezzlement_score * 0.30
            + self.judicial_corruption_score * 0.25
            + self.impunity_of_officials_score * 0.25
            + self.civil_society_repression_score * 0.20,
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
        self.estimated_anti_corruption_human_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class AntiCorruptionHumanRightsEngineResult:
    agent: str = "Anti Corruption Human Rights Engine Agent"
    domain: str = "anti_corruption_human_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_anti_corruption_human_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AntiCorruptionHumanRightsEntity] = field(default_factory=list)


def run_anti_corruption_human_rights_engine() -> AntiCorruptionHumanRightsEngineResult:
    entities = [
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-001",
            name="Soudan du Sud — Corruption systémique, 4Md$ détournés depuis indépendance, famine résultante",
            country="Soudan du Sud",
            public_resource_embezzlement_score=97.0,
            judicial_corruption_score=96.0,
            impunity_of_officials_score=95.0,
            civil_society_repression_score=94.0,
            primary_pattern="public_resource_embezzlement",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-002",
            name="Venezuela — Maduro kleptocracie, 30Md$ PDVSA détournés, CPI 14/100",
            country="Venezuela",
            public_resource_embezzlement_score=91.0,
            judicial_corruption_score=89.0,
            impunity_of_officials_score=90.0,
            civil_society_repression_score=88.0,
            primary_pattern="judicial_corruption",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-003",
            name="Libye — Fonds pétroliers pillés milices, LNA vs GNU corruption bi-latérale",
            country="Libye",
            public_resource_embezzlement_score=85.0,
            judicial_corruption_score=83.0,
            impunity_of_officials_score=84.0,
            civil_society_repression_score=82.0,
            primary_pattern="public_resource_embezzlement",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-004",
            name="Afghanistan — Taliban corruption + héritage Ghani, aide humanitaire détournée",
            country="Afghanistan",
            public_resource_embezzlement_score=76.0,
            judicial_corruption_score=78.0,
            impunity_of_officials_score=74.0,
            civil_society_repression_score=80.0,
            primary_pattern="civil_society_repression",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-005",
            name="Nigéria — NNPC 6Md$ non-comptabilisés, EFCC impuissante, gouverneurs immunisés",
            country="Nigéria",
            public_resource_embezzlement_score=55.0,
            judicial_corruption_score=57.0,
            impunity_of_officials_score=58.0,
            civil_society_repression_score=52.0,
            primary_pattern="impunity_of_officials",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-006",
            name="Brésil — Lava Jato partiellement réversé, Bolsonaro immunité, corruption institutionnelle",
            country="Brésil",
            public_resource_embezzlement_score=44.0,
            judicial_corruption_score=46.0,
            impunity_of_officials_score=48.0,
            civil_society_repression_score=42.0,
            primary_pattern="impunity_of_officials",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-007",
            name="Italie — Mafia Cosa Nostra/Ndrangheta, flux financiers illicites, lenteur judiciaire",
            country="Italie",
            public_resource_embezzlement_score=28.0,
            judicial_corruption_score=30.0,
            impunity_of_officials_score=26.0,
            civil_society_repression_score=24.0,
            primary_pattern="judicial_corruption",
        ),
        AntiCorruptionHumanRightsEntity(
            entity_id="ACH-008",
            name="Danemark/Nouvelle-Zélande — CPI 90+/100, whistleblowers protégés, tribunaux indépendants",
            country="Danemark/Nouvelle-Zélande",
            public_resource_embezzlement_score=6.0,
            judicial_corruption_score=7.0,
            impunity_of_officials_score=5.0,
            civil_society_repression_score=8.0,
            primary_pattern="civil_society_repression",
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

    return AntiCorruptionHumanRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_anti_corruption_human_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "transparency_international_cpi_2024",
            "un_convention_against_corruption_implementation",
            "hrw_corruption_human_rights_nexus_2024",
            "global_witness_corruption_report_2024",
            "anticorruption_resource_centre_u4_reports",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_anti_corruption_human_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
