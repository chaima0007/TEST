from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class EnforcedDisappearancesEntity:
    entity_id: str
    name: str
    country: str
    state_perpetrated_disappearance_severity_score: float
    impunity_accountability_absence_scale_score: float
    family_right_to_truth_obstruction_score: float
    legal_framework_prevention_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_enforced_disappearances_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_perpetrated_disappearance_severity_score * 0.30
            + self.impunity_accountability_absence_scale_score * 0.25
            + self.family_right_to_truth_obstruction_score * 0.25
            + self.legal_framework_prevention_gap_score * 0.20,
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
        self.estimated_enforced_disappearances_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class EnforcedDisappearancesEngineResult:
    agent: str = "Enforced Disappearances Engine Agent"
    domain: str = "enforced_disappearances"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_enforced_disappearances_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[EnforcedDisappearancesEntity] = field(default_factory=list)

def run_enforced_disappearances_engine() -> EnforcedDisappearancesEngineResult:
    entities = [
        EnforcedDisappearancesEntity(
            entity_id="EDE-001",
            name="Mexique — 100 000+ Disparus, Cartels+État Complicité, Registre RENPED & Fosses Communes 4 000+",
            country="Mexique",
            state_perpetrated_disappearance_severity_score=96.0,
            impunity_accountability_absence_scale_score=93.0,
            family_right_to_truth_obstruction_score=94.0,
            legal_framework_prevention_gap_score=92.0,
            primary_pattern="state_perpetrated_disappearance_severity",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-002",
            name="Syrie — 150 000+ Disparus Depuis 2011, Détention Assad Secrète, Torture & Zéro Responsabilité",
            country="Syrie",
            state_perpetrated_disappearance_severity_score=93.0,
            impunity_accountability_absence_scale_score=90.0,
            family_right_to_truth_obstruction_score=91.0,
            legal_framework_prevention_gap_score=89.0,
            primary_pattern="impunity_accountability_absence_scale",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-003",
            name="Corée du Nord — Disparitions Politiques Généralisées, Camps Kwanliso, Familles Sans Information",
            country="Corée du Nord",
            state_perpetrated_disappearance_severity_score=90.0,
            impunity_accountability_absence_scale_score=87.0,
            family_right_to_truth_obstruction_score=88.0,
            legal_framework_prevention_gap_score=86.0,
            primary_pattern="family_right_to_truth_obstruction",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-004",
            name="Chili/Argent Legacy — 30 000 Argentins Disparus Dictature, Impunité Partielle & Bébés Volés",
            country="Chili/Argentine",
            state_perpetrated_disappearance_severity_score=87.0,
            impunity_accountability_absence_scale_score=84.0,
            family_right_to_truth_obstruction_score=85.0,
            legal_framework_prevention_gap_score=83.0,
            primary_pattern="impunity_accountability_absence_scale",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-005",
            name="Philippines — 1 200+ Disparus Guerre Drogues Duterte, Red-Tagging & Zéro Enquête",
            country="Philippines",
            state_perpetrated_disappearance_severity_score=56.0,
            impunity_accountability_absence_scale_score=53.0,
            family_right_to_truth_obstruction_score=54.0,
            legal_framework_prevention_gap_score=52.0,
            primary_pattern="state_perpetrated_disappearance_severity",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-006",
            name="Sri Lanka/Birmanie — Post-Guerre LTTE 12 000 Disparus, Militaires Impunis & Familles Obstruction",
            country="Sri Lanka/Myanmar",
            state_perpetrated_disappearance_severity_score=53.0,
            impunity_accountability_absence_scale_score=51.0,
            family_right_to_truth_obstruction_score=51.0,
            legal_framework_prevention_gap_score=49.0,
            primary_pattern="family_right_to_truth_obstruction",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-007",
            name="FEDEFAM/ICAED — Familles Disparus LATAM, Comité ONU CED & Mécanismes Vérité-Justice",
            country="Global",
            state_perpetrated_disappearance_severity_score=27.0,
            impunity_accountability_absence_scale_score=26.0,
            family_right_to_truth_obstruction_score=26.0,
            legal_framework_prevention_gap_score=25.0,
            primary_pattern="family_right_to_truth_obstruction",
        ),
        EnforcedDisappearancesEntity(
            entity_id="EDE-008",
            name="ONU/Convention CED — Convention Disparitions Forcées 2006, Comité CED & SDG 16.3 Justice",
            country="Global",
            state_perpetrated_disappearance_severity_score=4.0,
            impunity_accountability_absence_scale_score=4.0,
            family_right_to_truth_obstruction_score=4.0,
            legal_framework_prevention_gap_score=4.0,
            primary_pattern="legal_framework_prevention_gap",
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

    return EnforcedDisappearancesEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_enforced_disappearances_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_committee_on_enforced_disappearances_reports",
            "amnesty_international_enforced_disappearances_global",
            "fedefam_latin_america_missing_persons_database",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_enforced_disappearances_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_enforced_disappearances_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
