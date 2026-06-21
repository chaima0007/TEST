from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PeacekeepingAccountabilityGovernanceEntity:
    entity_id: str
    name: str
    country: str
    abuse_impunity_rate: float
    reporting_obstruction: float
    victim_remedy_gap: float
    institutional_reform_absence: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_peacekeeping_accountability_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.abuse_impunity_rate * 0.30
            + self.reporting_obstruction * 0.25
            + self.victim_remedy_gap * 0.25
            + self.institutional_reform_absence * 0.20,
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
        self.estimated_peacekeeping_accountability_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PeacekeepingAccountabilityGovernanceEngineResult:
    agent: str = "Peacekeeping Accountability Governance Engine Agent"
    domain: str = "peacekeeping_accountability_governance"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_peacekeeping_accountability_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PeacekeepingAccountabilityGovernanceEntity] = field(default_factory=list)

def run_peacekeeping_accountability_governance_engine() -> PeacekeepingAccountabilityGovernanceEngineResult:
    entities = [
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-001",
            name="RCA MINUSCA — Abus sexuels massifs, soldats francais Sangaris, ONU inaction documentee",
            country="Republique Centrafricaine",
            abuse_impunity_rate=94.0,
            reporting_obstruction=90.0,
            victim_remedy_gap=92.0,
            institutional_reform_absence=86.0,
            primary_pattern="abuse_impunity_rate",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-002",
            name="Haiti MINUSTAH — Cholera importe ONU 2010, 10K morts, deni puis accord partiel",
            country="Haiti",
            abuse_impunity_rate=88.0,
            reporting_obstruction=88.0,
            victim_remedy_gap=84.0,
            institutional_reform_absence=80.0,
            primary_pattern="reporting_obstruction",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-003",
            name="RDC MONUSCO — Abus sexuels Kivu, peacekeepers vendant armes aux rebelles",
            country="RDC",
            abuse_impunity_rate=84.0,
            reporting_obstruction=82.0,
            victim_remedy_gap=80.0,
            institutional_reform_absence=78.0,
            primary_pattern="abuse_impunity_rate",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-004",
            name="Mali MINUSMA — Accusations violations droits, retrait brusque 2023, impunite totale",
            country="Mali",
            abuse_impunity_rate=74.0,
            reporting_obstruction=72.0,
            victim_remedy_gap=70.0,
            institutional_reform_absence=68.0,
            primary_pattern="abuse_impunity_rate",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-005",
            name="Bosnie SFOR — Trafic humain peacekeeper annees 1990, lente reconnaissance ONU",
            country="Bosnie-Herzegovine",
            abuse_impunity_rate=55.0,
            reporting_obstruction=52.0,
            victim_remedy_gap=50.0,
            institutional_reform_absence=48.0,
            primary_pattern="abuse_impunity_rate",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-006",
            name="Soudan du Sud UNMISS — Abus sporadiques, mecanismes de plainte partiels",
            country="Soudan du Sud",
            abuse_impunity_rate=46.0,
            reporting_obstruction=44.0,
            victim_remedy_gap=42.0,
            institutional_reform_absence=40.0,
            primary_pattern="victim_remedy_gap",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-007",
            name="Liban FINUL — Tensions moderees, quelques incidents signales, cooperation partielle",
            country="Liban",
            abuse_impunity_rate=26.0,
            reporting_obstruction=24.0,
            victim_remedy_gap=22.0,
            institutional_reform_absence=20.0,
            primary_pattern="institutional_reform_absence",
        ),
        PeacekeepingAccountabilityGovernanceEntity(
            entity_id="PAG-008",
            name="Canada/Norvege modele — Standards conduite peacekeeper, formation DDHH obligatoire",
            country="Canada/Norvege",
            abuse_impunity_rate=6.0,
            reporting_obstruction=5.0,
            victim_remedy_gap=4.0,
            institutional_reform_absence=3.0,
            primary_pattern="institutional_reform_absence",
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

    return PeacekeepingAccountabilityGovernanceEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_peacekeeping_accountability_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "human_rights_watch_peacekeeping_accountability_report_2024",
            "amnesty_international_un_peacekeeping_abuse_study_2023",
            "un_oios_peacekeeping_conduct_discipline_report_2024",
            "global_policy_forum_peacekeeping_reform_analysis_2023",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_peacekeeping_accountability_governance_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_peacekeeping_accountability_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}] — estimated_peacekeeping_accountability_index={e.estimated_peacekeeping_accountability_index}")
