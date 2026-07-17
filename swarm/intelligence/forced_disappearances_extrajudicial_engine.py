"""Forced Disappearances Extrajudicial Engine — Disparitions forcées, enlèvements état, familles sans recours."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ForcedDisappearancesExtrajudicialEntity:
    entity_id: str
    name: str
    country: str
    state_enforced_disappearance_severity_score: float
    family_notification_denial_body_concealment_scale_score: float
    impunity_perpetrators_accountability_gap_score: float
    truth_commission_reparation_mechanism_deficit_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_disappearances_extrajudicial_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.state_enforced_disappearance_severity_score * 0.30
            + self.family_notification_denial_body_concealment_scale_score * 0.25
            + self.impunity_perpetrators_accountability_gap_score * 0.25
            + self.truth_commission_reparation_mechanism_deficit_gap_score * 0.20,
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
        self.estimated_forced_disappearances_extrajudicial_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class ForcedDisappearancesExtrajudicialEngineResult:
    agent: str = "Forced Disappearances Extrajudicial Engine Agent"
    domain: str = "forced_disappearances_extrajudicial"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_forced_disappearances_extrajudicial_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ForcedDisappearancesExtrajudicialEntity] = field(default_factory=list)


def run_forced_disappearances_extrajudicial_engine() -> ForcedDisappearancesExtrajudicialEngineResult:
    entities = [
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-001",
            name="Syrie/Assad — 130 000 Disparus Confirmés, Centres Détention Secrets, Familles Sans Informations & Charniers Découverts Post-Chute",
            country="Syrie",
            state_enforced_disappearance_severity_score=96.0,
            family_notification_denial_body_concealment_scale_score=94.0,
            impunity_perpetrators_accountability_gap_score=93.0,
            truth_commission_reparation_mechanism_deficit_gap_score=95.0,
            primary_pattern="state_enforced_disappearance_severity",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-002",
            name="Argentine 1976-83 — 30 000 Disparus Junte, ESMA Torture, Enfants Volés Adoptions Forcées & Mères Plaza Mayo",
            country="Argentine",
            state_enforced_disappearance_severity_score=92.0,
            family_notification_denial_body_concealment_scale_score=93.0,
            impunity_perpetrators_accountability_gap_score=90.0,
            truth_commission_reparation_mechanism_deficit_gap_score=91.0,
            primary_pattern="family_notification_denial_body_concealment_scale",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-003",
            name="Mexique/Cartels — 100 000 Disparus 2006-24, 50 000 Corps Non-Identifiés, Étudiants Ayotzinapa 43 & Police Complicité",
            country="Mexique",
            state_enforced_disappearance_severity_score=88.0,
            family_notification_denial_body_concealment_scale_score=86.0,
            impunity_perpetrators_accountability_gap_score=89.0,
            truth_commission_reparation_mechanism_deficit_gap_score=87.0,
            primary_pattern="impunity_perpetrators_accountability_gap",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-004",
            name="Chine/Xinjiang — Disparitions Forcées Uyghures, Avocats 709 Disparus, Silence Familles Étranger Menacées & Localisation Inconnue",
            country="Chine",
            state_enforced_disappearance_severity_score=84.0,
            family_notification_denial_body_concealment_scale_score=82.0,
            impunity_perpetrators_accountability_gap_score=85.0,
            truth_commission_reparation_mechanism_deficit_gap_score=83.0,
            primary_pattern="state_enforced_disappearance_severity",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-005",
            name="Sri Lanka — Disparus Guerre Civile 2009, Tamouls Remis Armée Disparus, Commission Vérité Bloquée & Familles Manifester Interdit",
            country="Sri Lanka",
            state_enforced_disappearance_severity_score=56.0,
            family_notification_denial_body_concealment_scale_score=54.0,
            impunity_perpetrators_accountability_gap_score=55.0,
            truth_commission_reparation_mechanism_deficit_gap_score=57.0,
            primary_pattern="truth_commission_reparation_mechanism_deficit_gap",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-006",
            name="Russie/Tchétchénie — Disparitions Tchétchènes 2000-24, Kadyrov Ennemis Disparus, Memorial Fermé & Familles Intimidées",
            country="Russie",
            state_enforced_disappearance_severity_score=52.0,
            family_notification_denial_body_concealment_scale_score=51.0,
            impunity_perpetrators_accountability_gap_score=54.0,
            truth_commission_reparation_mechanism_deficit_gap_score=53.0,
            primary_pattern="impunity_perpetrators_accountability_gap",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-007",
            name="FEDEFAM/ASFADDES — Fédération Latinoaméricaine Associations Familles Disparus, Colombie ASFADDES & Réseau International Disparus",
            country="Global",
            state_enforced_disappearance_severity_score=27.0,
            family_notification_denial_body_concealment_scale_score=25.0,
            impunity_perpetrators_accountability_gap_score=28.0,
            truth_commission_reparation_mechanism_deficit_gap_score=26.0,
            primary_pattern="truth_commission_reparation_mechanism_deficit_gap",
        ),
        ForcedDisappearancesExtrajudicialEntity(
            entity_id="FDE-008",
            name="ONU/Conv 2006 — Convention Internationale Disparitions Forcées 2006, Comité Disparitions Forcées & SDG 16.3 Justice",
            country="Global",
            state_enforced_disappearance_severity_score=4.0,
            family_notification_denial_body_concealment_scale_score=4.0,
            impunity_perpetrators_accountability_gap_score=4.0,
            truth_commission_reparation_mechanism_deficit_gap_score=4.0,
            primary_pattern="state_enforced_disappearance_severity",
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
        for e in sorted_entities if e.risk_level == "critique"
    ]

    return ForcedDisappearancesExtrajudicialEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_forced_disappearances_extrajudicial_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_committee_enforced_disappearances_report",
            "fedefam_latin_america_disappearances_report",
            "human_rights_watch_enforced_disappearances",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_forced_disappearances_extrajudicial_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_forced_disappearances_extrajudicial_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
