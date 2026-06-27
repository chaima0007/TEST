from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#7c2d12"


@dataclass
class ReligiousMinorityRightsEntity:
    entity_id: str
    name: str
    country: str
    religious_persecution_score: float
    blasphemy_law_abuse_score: float
    place_of_worship_destruction_score: float
    forced_conversion_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_religious_minority_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.religious_persecution_score * 0.30
            + self.blasphemy_law_abuse_score * 0.25
            + self.place_of_worship_destruction_score * 0.25
            + self.forced_conversion_score * 0.20,
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
        self.estimated_religious_minority_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ReligiousMinorityRightsEngineResult:
    agent: str = "Religious Minority Rights Engine Agent"
    domain: str = "religious_minority_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_religious_minority_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ReligiousMinorityRightsEntity] = field(default_factory=list)


def run_religious_minority_rights_engine() -> ReligiousMinorityRightsEngineResult:
    entities = [
        ReligiousMinorityRightsEntity(
            entity_id="RMR-001",
            name="Chine — Ouïghours camps 1M+, Falun Gong, Tibétains bouddhistes, Catholiques souterrain",
            country="Chine",
            religious_persecution_score=97.0,
            blasphemy_law_abuse_score=95.0,
            place_of_worship_destruction_score=96.0,
            forced_conversion_score=94.0,
            primary_pattern="religious_persecution",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-002",
            name="Pakistan — Loi blasphème 295C, minorités chrétiennes/hindoues/ahmadis brûlées vives",
            country="Pakistan",
            religious_persecution_score=91.0,
            blasphemy_law_abuse_score=95.0,
            place_of_worship_destruction_score=89.0,
            forced_conversion_score=92.0,
            primary_pattern="blasphemy_law_abuse",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-003",
            name="Corée du Nord — Chrétiens camps de travail, religion interdite État, exécutions pasteurs",
            country="Corée du Nord",
            religious_persecution_score=87.0,
            blasphemy_law_abuse_score=83.0,
            place_of_worship_destruction_score=85.0,
            forced_conversion_score=88.0,
            primary_pattern="religious_persecution",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-004",
            name="Myanmar — Rohingyas musulmans génocide, mosquées brûlées, bouddhisme État arme",
            country="Myanmar",
            religious_persecution_score=78.0,
            blasphemy_law_abuse_score=76.0,
            place_of_worship_destruction_score=82.0,
            forced_conversion_score=75.0,
            primary_pattern="place_of_worship_destruction",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-005",
            name="Iran — Bahá'ís persécutés, Chrétiens convertis emprisonnés, Sunnites discriminés",
            country="Iran",
            religious_persecution_score=54.0,
            blasphemy_law_abuse_score=58.0,
            place_of_worship_destruction_score=52.0,
            forced_conversion_score=56.0,
            primary_pattern="blasphemy_law_abuse",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-006",
            name="Nigéria — Boko Haram chrétiens, Fulani herdsmen, 4 500 chrétiens tués 2023",
            country="Nigéria",
            religious_persecution_score=46.0,
            blasphemy_law_abuse_score=44.0,
            place_of_worship_destruction_score=50.0,
            forced_conversion_score=45.0,
            primary_pattern="place_of_worship_destruction",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-007",
            name="Inde — Lois anti-conversion BJP, lynchages minorités musulmanes, VHP violence",
            country="Inde",
            religious_persecution_score=28.0,
            blasphemy_law_abuse_score=26.0,
            place_of_worship_destruction_score=30.0,
            forced_conversion_score=24.0,
            primary_pattern="forced_conversion",
        ),
        ReligiousMinorityRightsEntity(
            entity_id="RMR-008",
            name="Canada/Nouvelle-Zélande — Liberté religieuse constitutionnelle, mosquées protégées, ICCPR",
            country="Canada/Nouvelle-Zélande",
            religious_persecution_score=6.0,
            blasphemy_law_abuse_score=5.0,
            place_of_worship_destruction_score=7.0,
            forced_conversion_score=8.0,
            primary_pattern="religious_persecution",
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

    return ReligiousMinorityRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_religious_minority_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "us_cirf_religious_freedom_report_2024",
            "open_doors_world_watch_list_2024",
            "hrw_religious_persecution_global_2024",
            "pew_research_religious_restrictions_global",
            "aid_to_church_in_need_persecution_report_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_religious_minority_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
