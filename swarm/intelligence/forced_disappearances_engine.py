from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ForcedDisappearancesEntity:
    entity_id: str
    name: str
    country: str
    state_perpetration_scale_score: float
    body_concealment_impunity_score: float
    family_search_obstruction_score: float
    truth_justice_mechanism_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_disappearances_index: float = field(init=False)
    last_updated: str = "2026-06-20"

    def __post_init__(self):
        self.composite_score = round(
            self.state_perpetration_scale_score * 0.30
            + self.body_concealment_impunity_score * 0.25
            + self.family_search_obstruction_score * 0.25
            + self.truth_justice_mechanism_gap_score * 0.20,
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
        self.estimated_forced_disappearances_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ForcedDisappearancesEngineResult:
    agent: str = "Forced Disappearances Engine Agent"
    domain: str = "forced_disappearances"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-20"
    engine_version: str = "1.0.0"
    avg_estimated_forced_disappearances_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ForcedDisappearancesEntity] = field(default_factory=list)

def run_forced_disappearances_engine() -> ForcedDisappearancesEngineResult:
    entities = [
        ForcedDisappearancesEntity(
            entity_id="FD-001",
            name="Syrie — 100K+ Disparus Régime Assad, Prisons Secrètes Saydnaya & Fosses Communes",
            country="Moyen-Orient",
            state_perpetration_scale_score=95.0,
            body_concealment_impunity_score=92.0,
            family_search_obstruction_score=90.0,
            truth_justice_mechanism_gap_score=92.0,
            primary_pattern="state_perpetration_scale",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-002",
            name="Mexique — 110K Disparus Cartels/État, Fossés Communs & FNAILEP Sans Résultats",
            country="Amérique du Nord",
            state_perpetration_scale_score=88.0,
            body_concealment_impunity_score=90.0,
            family_search_obstruction_score=85.0,
            truth_justice_mechanism_gap_score=88.0,
            primary_pattern="body_concealment_impunity",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-003",
            name="Égypte — Disparitions Post-2013, Sisi Opposants/Journalistes & Déni Détentions Secrètes",
            country="Afrique du Nord",
            state_perpetration_scale_score=85.0,
            body_concealment_impunity_score=82.0,
            family_search_obstruction_score=88.0,
            truth_justice_mechanism_gap_score=85.0,
            primary_pattern="family_search_obstruction",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-004",
            name="Argentine/Mémoire — 30K Disparus Dictature 1976-83, ESMA & Lucha Abuelas Plaza Mayo",
            country="Amérique Latine",
            state_perpetration_scale_score=82.0,
            body_concealment_impunity_score=78.0,
            family_search_obstruction_score=80.0,
            truth_justice_mechanism_gap_score=85.0,
            primary_pattern="truth_justice_mechanism_gap",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-005",
            name="Chine/Xinjiang — Disparitions Ouïghours, Détentions Secrètes Camps & Familles Sans Nouvelles",
            country="Asie du Nord-Est",
            state_perpetration_scale_score=55.0,
            body_concealment_impunity_score=52.0,
            family_search_obstruction_score=58.0,
            truth_justice_mechanism_gap_score=55.0,
            primary_pattern="family_search_obstruction",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-006",
            name="Colombie — Paramilitaires/FARC Disparus, Unité Recherche Personnes Desaparecidas & Paix Partielle",
            country="Amérique Latine",
            state_perpetration_scale_score=48.0,
            body_concealment_impunity_score=52.0,
            family_search_obstruction_score=50.0,
            truth_justice_mechanism_gap_score=55.0,
            primary_pattern="truth_justice_mechanism_gap",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-007",
            name="FEDEFAM/ICMP — Fédération Familles Disparus, Identification ADN & Plaidoyer International",
            country="Global",
            state_perpetration_scale_score=22.0,
            body_concealment_impunity_score=25.0,
            family_search_obstruction_score=28.0,
            truth_justice_mechanism_gap_score=30.0,
            primary_pattern="state_perpetration_scale",
        ),
        ForcedDisappearancesEntity(
            entity_id="FD-008",
            name="ONU/Convention 2006 — Déclaration Disparitions Forcées, Comité CED & Rapports Périodiques",
            country="Global",
            state_perpetration_scale_score=4.0,
            body_concealment_impunity_score=5.0,
            family_search_obstruction_score=3.0,
            truth_justice_mechanism_gap_score=6.0,
            primary_pattern="body_concealment_impunity",
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

    return ForcedDisappearancesEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_forced_disappearances_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "icmp_international_commission_missing_persons_annual_report",
            "amnesty_international_enforced_disappearances_global_report",
            "un_committee_ced_enforced_disappearances_session_reports",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_forced_disappearances_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_forced_disappearances_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
