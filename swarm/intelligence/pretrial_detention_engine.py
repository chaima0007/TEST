from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PretrialDetentionEntity:
    entity_id: str
    name: str
    country: str
    detention_duration_excess_score: float
    inhumane_conditions_score: float
    legal_access_denial_score: float
    presumption_innocence_violation_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_pretrial_detention_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.detention_duration_excess_score * 0.30
            + self.inhumane_conditions_score * 0.25
            + self.legal_access_denial_score * 0.25
            + self.presumption_innocence_violation_score * 0.20,
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
        self.estimated_pretrial_detention_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PretrialDetentionEngineResult:
    agent: str = "Pretrial Detention Engine Agent"
    domain: str = "pretrial_detention"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_pretrial_detention_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PretrialDetentionEntity] = field(default_factory=list)

def run_pretrial_detention_engine() -> PretrialDetentionEngineResult:
    entities = [
        PretrialDetentionEntity(
            entity_id="PD-001",
            name="Philippines — Geôles 500%+ Surpeuplées, Détention Préventive 5 Ans Moy. & Torture Documentée",
            country="Asie du Sud-Est",
            detention_duration_excess_score=95.0,
            inhumane_conditions_score=95.0,
            legal_access_denial_score=92.0,
            presumption_innocence_violation_score=90.0,
            primary_pattern="detention_duration_excess",
        ),
        PretrialDetentionEntity(
            entity_id="PD-002",
            name="RDC — Cachots Illégaux, 80%+ Prévenus Sans Jugement & Détention Arbitraire Systémique",
            country="Afrique Centrale",
            detention_duration_excess_score=92.0,
            inhumane_conditions_score=90.0,
            legal_access_denial_score=88.0,
            presumption_innocence_violation_score=92.0,
            primary_pattern="presumption_innocence_violation",
        ),
        PretrialDetentionEntity(
            entity_id="PD-003",
            name="Haïti — Pénitencier National Effondré, Gangs Contrôlent Prisons & ONU 98% Prévenus",
            country="Caraïbes",
            detention_duration_excess_score=88.0,
            inhumane_conditions_score=92.0,
            legal_access_denial_score=85.0,
            presumption_innocence_violation_score=88.0,
            primary_pattern="inhumane_conditions",
        ),
        PretrialDetentionEntity(
            entity_id="PD-004",
            name="Mexique — Arraigo 80 Jours Légal, 40%+ Prévenus & Corruption Judiciaire Systémique",
            country="Amérique Latine",
            detention_duration_excess_score=85.0,
            inhumane_conditions_score=82.0,
            legal_access_denial_score=88.0,
            presumption_innocence_violation_score=85.0,
            primary_pattern="legal_access_denial",
        ),
        PretrialDetentionEntity(
            entity_id="PD-005",
            name="USA — Rikers Island, Cash Bail Système Pauvres, Kalief Browder 3 Ans Rikers Mineur",
            country="Amérique du Nord",
            detention_duration_excess_score=52.0,
            inhumane_conditions_score=55.0,
            legal_access_denial_score=58.0,
            presumption_innocence_violation_score=52.0,
            primary_pattern="legal_access_denial",
        ),
        PretrialDetentionEntity(
            entity_id="PD-006",
            name="France — Détention Provisoire 30%+ Population Carcérale, MAJ Prolongés & Surpopulation",
            country="Europe",
            detention_duration_excess_score=48.0,
            inhumane_conditions_score=52.0,
            legal_access_denial_score=50.0,
            presumption_innocence_violation_score=48.0,
            primary_pattern="inhumane_conditions",
        ),
        PretrialDetentionEntity(
            entity_id="PD-007",
            name="Fair Trials International/Penal Reform — Monitoring Détention Préventive & Plaidoyer",
            country="Global",
            detention_duration_excess_score=22.0,
            inhumane_conditions_score=25.0,
            legal_access_denial_score=28.0,
            presumption_innocence_violation_score=30.0,
            primary_pattern="presumption_innocence_violation",
        ),
        PretrialDetentionEntity(
            entity_id="PD-008",
            name="ONU/CCPR — Art.9 PIDCP Liberté Personne, Groupe Travail Détention Arbitraire",
            country="Global",
            detention_duration_excess_score=4.0,
            inhumane_conditions_score=5.0,
            legal_access_denial_score=3.0,
            presumption_innocence_violation_score=6.0,
            primary_pattern="legal_access_denial",
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

    return PretrialDetentionEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_pretrial_detention_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "fair_trials_international_pretrial_detention_global_report",
            "penal_reform_international_global_prison_trends",
            "un_working_group_arbitrary_detention_annual_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_pretrial_detention_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_pretrial_detention_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
