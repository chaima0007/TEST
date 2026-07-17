from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class MinorityReligiousFreedomRightsEntity:
    entity_id: str
    name: str
    country: str
    religious_persecution_imprisonment_severity_score: float
    place_of_worship_destruction_ban_scale_score: float
    blasphemy_apostasy_law_prosecution_score: float
    religious_minority_civil_rights_exclusion_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_minority_religious_freedom_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.religious_persecution_imprisonment_severity_score * 0.30
            + self.place_of_worship_destruction_ban_scale_score * 0.25
            + self.blasphemy_apostasy_law_prosecution_score * 0.25
            + self.religious_minority_civil_rights_exclusion_gap_score * 0.20,
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
        self.estimated_minority_religious_freedom_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class MinorityReligiousFreedomRightsEngineResult:
    agent: str = "Minority Religious Freedom Rights Engine Agent"
    domain: str = "minority_religious_freedom_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_minority_religious_freedom_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[MinorityReligiousFreedomRightsEntity] = field(default_factory=list)

def run_minority_religious_freedom_rights_engine() -> MinorityReligiousFreedomRightsEngineResult:
    entities = [
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-001",
            name="Chine — Ouïghours Mosquées Détruites, Tibétains Bouddhisme Persécuté, Falun Gong 1M Détenus & Crosses Église Retirées",
            country="Chine",
            religious_persecution_imprisonment_severity_score=96.0,
            place_of_worship_destruction_ban_scale_score=93.0,
            blasphemy_apostasy_law_prosecution_score=90.0,
            religious_minority_civil_rights_exclusion_gap_score=94.0,
            primary_pattern="religious_persecution_imprisonment_severity",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-002",
            name="Pakistan — Blasphème Loi 295-C Peine Mort, Ahmadis Minorité Persécutée, Chrétiens Villages Brûlés & Asia Bibi",
            country="Pakistan",
            religious_persecution_imprisonment_severity_score=92.0,
            place_of_worship_destruction_ban_scale_score=89.0,
            blasphemy_apostasy_law_prosecution_score=93.0,
            religious_minority_civil_rights_exclusion_gap_score=88.0,
            primary_pattern="blasphemy_apostasy_law_prosecution",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-003",
            name="Iran — Baha'is Propriétés Confisquées, Évangéliques Emprisonnés, Juifs Discrimination & Convertis Apostasie",
            country="Iran",
            religious_persecution_imprisonment_severity_score=89.0,
            place_of_worship_destruction_ban_scale_score=86.0,
            blasphemy_apostasy_law_prosecution_score=90.0,
            religious_minority_civil_rights_exclusion_gap_score=84.0,
            primary_pattern="blasphemy_apostasy_law_prosecution",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-004",
            name="Birmanie/Myanmar — Rohingyas Musulmans Génocide, Mosquées Brûlées, Statut Apatride & Lois Bouddhisme National Race",
            country="Myanmar",
            religious_persecution_imprisonment_severity_score=86.0,
            place_of_worship_destruction_ban_scale_score=84.0,
            blasphemy_apostasy_law_prosecution_score=82.0,
            religious_minority_civil_rights_exclusion_gap_score=85.0,
            primary_pattern="place_of_worship_destruction_ban_scale",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-005",
            name="Inde/Modi — Loi CAA Discrimination Musulmans, Lynchage Vache, Destructions Mosquées & RSS Violence Minorités",
            country="Inde",
            religious_persecution_imprisonment_severity_score=57.0,
            place_of_worship_destruction_ban_scale_score=55.0,
            blasphemy_apostasy_law_prosecution_score=54.0,
            religious_minority_civil_rights_exclusion_gap_score=56.0,
            primary_pattern="religious_persecution_imprisonment_severity",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-006",
            name="Russie/Biélorussie — Témoins Jéhovah Interdits, Propriétés Saisies, Catholicisme Réprimé & Sectes Loi Lutte",
            country="Russie/Biélorussie",
            religious_persecution_imprisonment_severity_score=54.0,
            place_of_worship_destruction_ban_scale_score=53.0,
            blasphemy_apostasy_law_prosecution_score=52.0,
            religious_minority_civil_rights_exclusion_gap_score=50.0,
            primary_pattern="religious_persecution_imprisonment_severity",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-007",
            name="USCIRF/Forum 18 — Commission Liberté Religieuse Internationale, Monitoring Pays Préoccupants & Rapports Annuels",
            country="Global",
            religious_persecution_imprisonment_severity_score=24.0,
            place_of_worship_destruction_ban_scale_score=28.0,
            blasphemy_apostasy_law_prosecution_score=27.0,
            religious_minority_civil_rights_exclusion_gap_score=26.0,
            primary_pattern="place_of_worship_destruction_ban_scale",
        ),
        MinorityReligiousFreedomRightsEntity(
            entity_id="MRF-008",
            name="ONU/Art.18 PIDCP — Liberté Conscience Religion, Déclaration 1981 Minorités Religieuses & SDG 16.3",
            country="Global",
            religious_persecution_imprisonment_severity_score=4.0,
            place_of_worship_destruction_ban_scale_score=5.0,
            blasphemy_apostasy_law_prosecution_score=4.0,
            religious_minority_civil_rights_exclusion_gap_score=5.0,
            primary_pattern="religious_persecution_imprisonment_severity",
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

    return MinorityReligiousFreedomRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_minority_religious_freedom_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "uscirf_annual_report_religious_freedom_violations",
            "open_doors_world_watch_list_christian_persecution",
            "forum18_central_asia_religious_freedom_monitoring",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_minority_religious_freedom_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_minority_religious_freedom_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
