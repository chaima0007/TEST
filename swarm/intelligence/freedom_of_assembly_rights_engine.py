from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#f43f5e"


@dataclass
class FreedomOfAssemblyRightsEntity:
    entity_id: str
    name: str
    country: str
    protest_crackdown_score: float
    arbitrary_arrest_assembly_score: float
    civil_society_ban_score: float
    permit_denial_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_freedom_of_assembly_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.protest_crackdown_score * 0.30
            + self.arbitrary_arrest_assembly_score * 0.25
            + self.civil_society_ban_score * 0.25
            + self.permit_denial_score * 0.20,
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
        self.estimated_freedom_of_assembly_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class FreedomOfAssemblyRightsEngineResult:
    agent: str = "Freedom Of Assembly Rights Engine Agent"
    domain: str = "freedom_of_assembly_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_freedom_of_assembly_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[FreedomOfAssemblyRightsEntity] = field(default_factory=list)


def run_freedom_of_assembly_rights_engine() -> FreedomOfAssemblyRightsEngineResult:
    entities = [
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-001",
            name="Biélorussie — Répression 2020 Manifestations Loukachenko, 35 000 Arrestations",
            country="Biélorussie",
            protest_crackdown_score=97.0,
            arbitrary_arrest_assembly_score=96.0,
            civil_society_ban_score=95.0,
            permit_denial_score=94.0,
            primary_pattern="mass_protest_repression",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-002",
            name="Myanmar — Coup 2021, 5 000 Tués Manifestants, Juntes Militaires Loi Martiale",
            country="Myanmar",
            protest_crackdown_score=91.0,
            arbitrary_arrest_assembly_score=93.0,
            civil_society_ban_score=90.0,
            permit_denial_score=89.0,
            primary_pattern="military_repression",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-003",
            name="Iran — Mahsa Amini 2022, 15 000 Arrestations, 500 Tués, Loi Anti-Manifestation",
            country="Iran",
            protest_crackdown_score=87.0,
            arbitrary_arrest_assembly_score=88.0,
            civil_society_ban_score=85.0,
            permit_denial_score=84.0,
            primary_pattern="mass_protest_repression",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-004",
            name="Chine — Tiananmen Héritage, Hong Kong NSL 2020, Manifestations Interdites",
            country="Chine",
            protest_crackdown_score=80.0,
            arbitrary_arrest_assembly_score=78.0,
            civil_society_ban_score=82.0,
            permit_denial_score=77.0,
            primary_pattern="civil_society_ban",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-005",
            name="Russie — Loi Anti-Manifestation 2022, OVD-Info 20 000 Arrestations, NGO Agent Étranger",
            country="Russie",
            protest_crackdown_score=54.0,
            arbitrary_arrest_assembly_score=56.0,
            civil_society_ban_score=58.0,
            permit_denial_score=52.0,
            primary_pattern="civil_society_ban",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-006",
            name="Égypte — Loi 107/2013 Permis Refusés, 60 000 Prisonniers Politiques",
            country="Égypte",
            protest_crackdown_score=46.0,
            arbitrary_arrest_assembly_score=48.0,
            civil_society_ban_score=44.0,
            permit_denial_score=50.0,
            primary_pattern="permit_denial",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-007",
            name="France — Loi Séparatisme + BRAV-M, Zones Interdites Gilets Jaunes, 11 000 Gardes à Vue",
            country="France",
            protest_crackdown_score=28.0,
            arbitrary_arrest_assembly_score=30.0,
            civil_society_ban_score=22.0,
            permit_denial_score=26.0,
            primary_pattern="arbitrary_arrest_assembly",
        ),
        FreedomOfAssemblyRightsEntity(
            entity_id="FAR-008",
            name="Allemagne/Canada — Droit Manifestation Constitutionnel, Plaintes Instruites, ICCPR Complet",
            country="Allemagne/Canada",
            protest_crackdown_score=7.0,
            arbitrary_arrest_assembly_score=8.0,
            civil_society_ban_score=6.0,
            permit_denial_score=9.0,
            primary_pattern="permit_denial",
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

    return FreedomOfAssemblyRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_freedom_of_assembly_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "civicus_monitor_civic_freedoms_2024",
            "amnesty_protest_crackdowns_global_2024",
            "hrw_freedom_assembly_association_violations",
            "acled_protest_repression_database_2024",
            "article_19_right_to_protest_global_report",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_freedom_of_assembly_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
