from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MinorityReligiousRightsPersecutionEntity:
    entity_id: str
    name: str
    country: str
    state_religious_persecution_severity_score: float
    blasphemy_apostasy_law_enforcement_scale_score: float
    minority_worship_restriction_destruction_score: float
    religious_conversion_prohibition_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_minority_religious_rights_persecution_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_religious_persecution_severity_score * 0.30
            + self.blasphemy_apostasy_law_enforcement_scale_score * 0.25
            + self.minority_worship_restriction_destruction_score * 0.25
            + self.religious_conversion_prohibition_deficit_gap_score * 0.20,
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
        self.estimated_minority_religious_rights_persecution_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class MinorityReligiousRightsPersecutionEngineResult:
    agent: str = "Minority Religious Rights Persecution Engine Agent"
    domain: str = "minority_religious_rights_persecution"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_minority_religious_rights_persecution_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MinorityReligiousRightsPersecutionEntity] = field(default_factory=list)


def run_minority_religious_rights_persecution_engine() -> MinorityReligiousRightsPersecutionEngineResult:
    entities = [
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-001",
            name="Chine/Ouïghours — Mosquées Détruites Reeducation Camps Xinjiang, Prières Interdites & Hajj Contrôlé État",
            country="Chine",
            state_religious_persecution_severity_score=96.0,
            blasphemy_apostasy_law_enforcement_scale_score=94.0,
            minority_worship_restriction_destruction_score=95.0,
            religious_conversion_prohibition_deficit_gap_score=93.0,
            primary_pattern="state_religious_persecution_severity",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-002",
            name="Iran/Bahais Chrétiens — Emprisonnés Apostasie Peine Mort, Eglises Maisons Fermées & Convertis Torturés",
            country="Iran",
            state_religious_persecution_severity_score=93.0,
            blasphemy_apostasy_law_enforcement_scale_score=95.0,
            minority_worship_restriction_destruction_score=91.0,
            religious_conversion_prohibition_deficit_gap_score=92.0,
            primary_pattern="blasphemy_apostasy_law_enforcement_scale",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-003",
            name="Pakistan/Ahmadis Chrétiens — Blasphème Peine Mort, Ahmadis Déclarés Non-Musulmans & Eglises Brûlées Foules",
            country="Pakistan",
            state_religious_persecution_severity_score=91.0,
            blasphemy_apostasy_law_enforcement_scale_score=93.0,
            minority_worship_restriction_destruction_score=89.0,
            religious_conversion_prohibition_deficit_gap_score=90.0,
            primary_pattern="blasphemy_apostasy_law_enforcement_scale",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-004",
            name="Inde/Lynchages Minorités — BJP Lois Anti-Conversion, Muslimans Lynchés Vache & Démolitions Mosquées Bulldozer",
            country="Inde",
            state_religious_persecution_severity_score=88.0,
            blasphemy_apostasy_law_enforcement_scale_score=85.0,
            minority_worship_restriction_destruction_score=87.0,
            religious_conversion_prohibition_deficit_gap_score=89.0,
            primary_pattern="religious_conversion_prohibition_deficit_gap",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-005",
            name="Myanmar/Rohingya — Mosquées Brûlées Génocide, Statut Apatride 1982 & Moine Wirathu Haine Anti-Islam",
            country="Myanmar",
            state_religious_persecution_severity_score=58.0,
            blasphemy_apostasy_law_enforcement_scale_score=55.0,
            minority_worship_restriction_destruction_score=60.0,
            religious_conversion_prohibition_deficit_gap_score=57.0,
            primary_pattern="minority_worship_restriction_destruction",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-006",
            name="Égypte/Coptes — Discriminés Emploi État, Eglises Démolies Permis Refusés & Blasphème Procès Chrétiens",
            country="Égypte",
            state_religious_persecution_severity_score=55.0,
            blasphemy_apostasy_law_enforcement_scale_score=57.0,
            minority_worship_restriction_destruction_score=58.0,
            religious_conversion_prohibition_deficit_gap_score=54.0,
            primary_pattern="minority_worship_restriction_destruction",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-007",
            name="USCIRF/Forum 18 — Monitoring Liberté Religieuse, Rapport Annuel Violations & Commission Internationale",
            country="Global",
            state_religious_persecution_severity_score=28.0,
            blasphemy_apostasy_law_enforcement_scale_score=27.0,
            minority_worship_restriction_destruction_score=26.0,
            religious_conversion_prohibition_deficit_gap_score=25.0,
            primary_pattern="state_religious_persecution_severity",
        ),
        MinorityReligiousRightsPersecutionEntity(
            entity_id="MRR-008",
            name="ONU/PIDCP Art.18 — Liberté Religion & Déclaration 1981 Intolérance Religieuse Rapporteur Spécial",
            country="Global",
            state_religious_persecution_severity_score=5.0,
            blasphemy_apostasy_law_enforcement_scale_score=5.0,
            minority_worship_restriction_destruction_score=5.0,
            religious_conversion_prohibition_deficit_gap_score=4.0,
            primary_pattern="state_religious_persecution_severity",
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

    return MinorityReligiousRightsPersecutionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_minority_religious_rights_persecution_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "uscirf_annual_report_religious_freedom",
            "forum_18_religious_freedom_monitoring",
            "hrw_religious_persecution_documentation",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_minority_religious_rights_persecution_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_minority_religious_rights_persecution_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
