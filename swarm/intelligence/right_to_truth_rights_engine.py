from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#7c3aed"


@dataclass
class RightToTruthRightsEntity:
    entity_id: str
    name: str
    country: str
    truth_commission_denial_score: float
    enforced_disappearance_impunity_score: float
    archive_destruction_score: float
    victim_reparation_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_right_to_truth_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.truth_commission_denial_score * 0.30
            + self.enforced_disappearance_impunity_score * 0.25
            + self.archive_destruction_score * 0.25
            + self.victim_reparation_gap_score * 0.20,
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
        self.estimated_right_to_truth_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class RightToTruthRightsEngineResult:
    agent: str = "Right To Truth Rights Engine Agent"
    domain: str = "right_to_truth_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_right_to_truth_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RightToTruthRightsEntity] = field(default_factory=list)


def run_right_to_truth_rights_engine() -> RightToTruthRightsEngineResult:
    entities = [
        RightToTruthRightsEntity(
            entity_id="RTT-001",
            name="Syrie — 130 000 disparus forcés, aucune commission vérité, Assad impuni",
            country="Syrie",
            truth_commission_denial_score=97.0,
            enforced_disappearance_impunity_score=96.0,
            archive_destruction_score=94.0,
            victim_reparation_gap_score=95.0,
            primary_pattern="truth_commission_denial",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-002",
            name="Chine — Tiananmen tabou officiel, 1989 dossiers détruits, familles Mères Tiananmen harcelées",
            country="Chine",
            truth_commission_denial_score=91.0,
            enforced_disappearance_impunity_score=89.0,
            archive_destruction_score=93.0,
            victim_reparation_gap_score=88.0,
            primary_pattern="archive_destruction",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-003",
            name="Algérie — Décennie noire 1990s, 8 000 disparus, archives militaires scellées",
            country="Algérie",
            truth_commission_denial_score=85.0,
            enforced_disappearance_impunity_score=83.0,
            archive_destruction_score=81.0,
            victim_reparation_gap_score=84.0,
            primary_pattern="enforced_disappearance_impunity",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-004",
            name="Sri Lanka — 40 000 Tamouls disparus 2009, Gotabaya amnistié, OMP sans mandat",
            country="Sri Lanka",
            truth_commission_denial_score=76.0,
            enforced_disappearance_impunity_score=78.0,
            archive_destruction_score=72.0,
            victim_reparation_gap_score=74.0,
            primary_pattern="enforced_disappearance_impunity",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-005",
            name="Colombie — JEP partielle, FARC impunités négociées, 80 000 disparus non-élucidés",
            country="Colombie",
            truth_commission_denial_score=54.0,
            enforced_disappearance_impunity_score=56.0,
            archive_destruction_score=50.0,
            victim_reparation_gap_score=52.0,
            primary_pattern="victim_reparation_gap",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-006",
            name="Mexique — 100 000 disparus cartel, bases de données ADN insuffisantes, impunité 95%",
            country="Mexique",
            truth_commission_denial_score=46.0,
            enforced_disappearance_impunity_score=48.0,
            archive_destruction_score=42.0,
            victim_reparation_gap_score=44.0,
            primary_pattern="enforced_disappearance_impunity",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-007",
            name="Argentine — CONADEP modèle 1984, 30% condamnations, archives partiellement ouvertes",
            country="Argentine",
            truth_commission_denial_score=28.0,
            enforced_disappearance_impunity_score=26.0,
            archive_destruction_score=30.0,
            victim_reparation_gap_score=24.0,
            primary_pattern="victim_reparation_gap",
        ),
        RightToTruthRightsEntity(
            entity_id="RTT-008",
            name="Rwanda/Afrique du Sud — Gacaca/TRC modèle, archives ouvertes, réparations partielles",
            country="Rwanda/Afrique du Sud",
            truth_commission_denial_score=8.0,
            enforced_disappearance_impunity_score=6.0,
            archive_destruction_score=7.0,
            victim_reparation_gap_score=9.0,
            primary_pattern="truth_commission_denial",
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

    return RightToTruthRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_right_to_truth_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_special_rapporteur_truth_justice_reparation_2024",
            "ictj_transitional_justice_global_review",
            "amnesty_enforced_disappearances_documentation",
            "hrw_justice_accountability_violations_2024",
            "icmp_missing_persons_global_database",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_right_to_truth_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
