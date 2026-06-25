from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class StatelessPersonsDocumentationEntity:
    entity_id: str
    name: str
    country: str
    statelessness_scale_intensity: float
    documentation_denial: float
    rights_deprivation: float
    protection_mechanism_gap: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_statelessness_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.statelessness_scale_intensity * 0.30
            + self.documentation_denial * 0.25
            + self.rights_deprivation * 0.25
            + self.protection_mechanism_gap * 0.20,
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
        self.estimated_statelessness_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class StatelessPersonsDocumentationEngineResult:
    agent: str = "Stateless Persons Documentation Engine Agent"
    domain: str = "stateless_persons_documentation"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.86
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_statelessness_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[StatelessPersonsDocumentationEntity] = field(default_factory=list)

def run_stateless_persons_documentation_engine() -> StatelessPersonsDocumentationEngineResult:
    entities = [
        StatelessPersonsDocumentationEntity(
            entity_id="STP-001",
            name="Myanmar Rohingyas — Sans nationalite depuis 1982, 1M+ apatrides, genocide documente",
            country="Myanmar",
            statelessness_scale_intensity=96.0,
            documentation_denial=94.0,
            rights_deprivation=92.0,
            protection_mechanism_gap=88.0,
            primary_pattern="statelessness_scale_intensity",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-002",
            name="Thailande Hill Tribes — 600K sans papiers, acces education et sante refuse",
            country="Thailande",
            statelessness_scale_intensity=88.0,
            documentation_denial=85.0,
            rights_deprivation=84.0,
            protection_mechanism_gap=80.0,
            primary_pattern="documentation_denial",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-003",
            name="Cote d'Ivoire — Apatridie post-conflit, Dioulas sans actes naissance",
            country="Cote d'Ivoire",
            statelessness_scale_intensity=80.0,
            documentation_denial=78.0,
            rights_deprivation=76.0,
            protection_mechanism_gap=74.0,
            primary_pattern="documentation_denial",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-004",
            name="Republique Dominicaine — Haitiens denationalises 2013, arret TC/0168/13",
            country="Republique Dominicaine",
            statelessness_scale_intensity=73.0,
            documentation_denial=70.0,
            rights_deprivation=72.0,
            protection_mechanism_gap=68.0,
            primary_pattern="rights_deprivation",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-005",
            name="Bangladesh chars et haors — Sans-papiers minorites riveraines, zones inondees",
            country="Bangladesh",
            statelessness_scale_intensity=55.0,
            documentation_denial=52.0,
            rights_deprivation=54.0,
            protection_mechanism_gap=50.0,
            primary_pattern="statelessness_scale_intensity",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-006",
            name="Europe apatrides ex-sovietiques — Lettonie/Estonie non-citoyens, russophones",
            country="Europe de l'Est",
            statelessness_scale_intensity=44.0,
            documentation_denial=42.0,
            rights_deprivation=40.0,
            protection_mechanism_gap=38.0,
            primary_pattern="protection_mechanism_gap",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-007",
            name="Kenya Nubians — Apatrides historiques depuis ere coloniale, reconnaissance partielle",
            country="Kenya",
            statelessness_scale_intensity=28.0,
            documentation_denial=26.0,
            rights_deprivation=24.0,
            protection_mechanism_gap=22.0,
            primary_pattern="statelessness_scale_intensity",
        ),
        StatelessPersonsDocumentationEntity(
            entity_id="STP-008",
            name="Portugal — Processus naturalisation rapide, enregistrement naissances universel",
            country="Portugal",
            statelessness_scale_intensity=8.0,
            documentation_denial=6.0,
            rights_deprivation=7.0,
            protection_mechanism_gap=5.0,
            primary_pattern="protection_mechanism_gap",
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
        f"{e.entity_id}: {e.primary_pattern}"
        for e in sorted_entities[:4]
    ]

    return StatelessPersonsDocumentationEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_statelessness_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unhcr_global_statelessness_report_2024",
            "institute_statelessness_inclusion_world_statelessness_report",
            "open_society_foundations_documentation_denial_study",
            "human_rights_watch_stateless_persons_documentation_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_stateless_persons_documentation_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_statelessness_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — estimated_statelessness_index={e.estimated_statelessness_index}")
