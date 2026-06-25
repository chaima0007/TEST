"""Forced Disappearance Extrajudicial Killing Engine — Disparitions forcées, exécutions extrajudiciaires, impunité état."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics


@dataclass
class ForcedDisappearanceExtrajudicialKillingEntity:
    entity_id: str
    name: str
    country: str
    enforced_disappearance_scale_impunity_score: float
    extrajudicial_execution_state_sanction_score: float
    family_truth_justice_reparation_denial_score: float
    international_accountability_mechanism_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_forced_disappearance_extrajudicial_killing_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.enforced_disappearance_scale_impunity_score * 0.30
            + self.extrajudicial_execution_state_sanction_score * 0.25
            + self.family_truth_justice_reparation_denial_score * 0.25
            + self.international_accountability_mechanism_gap_score * 0.20,
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
        self.estimated_forced_disappearance_extrajudicial_killing_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class ForcedDisappearanceExtrajudicialKillingEngineResult:
    agent: str
    domain: str
    entities: List[ForcedDisappearanceExtrajudicialKillingEntity]
    total_entities: int = field(init=False)
    avg_composite: float = field(init=False)
    avg_estimated_forced_disappearance_extrajudicial_killing_index: float = field(init=False)
    risk_distribution: dict = field(init=False)
    pattern_distribution: dict = field(init=False)
    top_risk_entities: List[str] = field(init=False)
    critical_alerts: List[str] = field(init=False)
    confidence_score: float = 0.89
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    data_sources: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.total_entities = len(self.entities)
        scores = [e.composite_score for e in self.entities]
        self.avg_composite = round(statistics.mean(scores), 2)
        self.avg_estimated_forced_disappearance_extrajudicial_killing_index = round(
            self.avg_composite / 100 * 10, 2
        )
        self.risk_distribution = {
            level: sum(1 for e in self.entities if e.risk_level == level)
            for level in ["critique", "élevé", "modéré", "faible"]
        }
        pattern_counts: dict = {}
        for e in self.entities:
            pattern_counts[e.primary_pattern] = pattern_counts.get(e.primary_pattern, 0) + 1
        self.pattern_distribution = pattern_counts
        critique_entities = sorted(
            [e for e in self.entities if e.risk_level == "critique"],
            key=lambda x: x.composite_score,
            reverse=True,
        )
        self.top_risk_entities = [e.entity_id for e in critique_entities[:3]]
        self.critical_alerts = [
            f"{e.entity_id} ({e.name}): composite={e.composite_score} — {e.primary_pattern}"
            for e in critique_entities
        ]


def run_forced_disappearance_extrajudicial_killing_engine() -> ForcedDisappearanceExtrajudicialKillingEngineResult:
    entities = [
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-001",
            name="Syrie/Assad Détentions — 130 000 Disparus, Centres Secrets, Torture Systématique & Charniers Post-Chute Régime",
            country="Syrie",
            enforced_disappearance_scale_impunity_score=92.0,
            extrajudicial_execution_state_sanction_score=90.0,
            family_truth_justice_reparation_denial_score=88.0,
            international_accountability_mechanism_gap_score=85.0,
            primary_pattern="enforced_disappearance_scale_impunity",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-002",
            name="Mexique/Cartels Complicité État — 100 000 Disparus, Ayotzinapa 43 Étudiants, Police Impliquée & Fosses Communes",
            country="Mexique",
            enforced_disappearance_scale_impunity_score=88.0,
            extrajudicial_execution_state_sanction_score=82.0,
            family_truth_justice_reparation_denial_score=85.0,
            international_accountability_mechanism_gap_score=80.0,
            primary_pattern="enforced_disappearance_scale_impunity",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-003",
            name="Philippines/Duterte Héritage — 30 000 Tués Guerre Drogue, Escadrons Mort PNP, Familles Sans Recours & Impunité Totale",
            country="Philippines",
            enforced_disappearance_scale_impunity_score=85.0,
            extrajudicial_execution_state_sanction_score=88.0,
            family_truth_justice_reparation_denial_score=80.0,
            international_accountability_mechanism_gap_score=78.0,
            primary_pattern="extrajudicial_execution_state_sanction",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-004",
            name="Égypte/Sisi Disparitions — Militants Disparus Post-2013, Torture Prisons Secrètes, Familles Harcelées & Aucune Enquête",
            country="Égypte",
            enforced_disappearance_scale_impunity_score=82.0,
            extrajudicial_execution_state_sanction_score=80.0,
            family_truth_justice_reparation_denial_score=85.0,
            international_accountability_mechanism_gap_score=75.0,
            primary_pattern="family_truth_justice_reparation_denial",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-005",
            name="Sri Lanka/Post-Guerre — Tamouls Disparus 2009, Commission Vérité Bloquée, Familles Attendent Décennies & Justice Partielle",
            country="Sri Lanka",
            enforced_disappearance_scale_impunity_score=55.0,
            extrajudicial_execution_state_sanction_score=52.0,
            family_truth_justice_reparation_denial_score=58.0,
            international_accountability_mechanism_gap_score=50.0,
            primary_pattern="family_truth_justice_reparation_denial",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-006",
            name="Bangladesh/RAB Exécutions — Rapid Action Battalion Tirs Croisés, Disparitions Opposants, Impunité Légale & HRW Documenter",
            country="Bangladesh",
            enforced_disappearance_scale_impunity_score=50.0,
            extrajudicial_execution_state_sanction_score=55.0,
            family_truth_justice_reparation_denial_score=48.0,
            international_accountability_mechanism_gap_score=52.0,
            primary_pattern="extrajudicial_execution_state_sanction",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-007",
            name="Colombie/FARC Paix Partielle — Accord 2016 Partiellement Appliqué, Ex-Combattants Tués, Leaders Sociaux Assassinés & JEP Justice",
            country="Colombie",
            enforced_disappearance_scale_impunity_score=28.0,
            extrajudicial_execution_state_sanction_score=25.0,
            family_truth_justice_reparation_denial_score=32.0,
            international_accountability_mechanism_gap_score=22.0,
            primary_pattern="family_truth_justice_reparation_denial",
        ),
        ForcedDisappearanceExtrajudicialKillingEntity(
            entity_id="FDEK-008",
            name="Argentine/CONADEP Modèle — Commission Vérité 1984, Procès Juntes, Réparations Familles & Référence Mondiale Justice Transitionnelle",
            country="Argentine",
            enforced_disappearance_scale_impunity_score=5.0,
            extrajudicial_execution_state_sanction_score=4.0,
            family_truth_justice_reparation_denial_score=8.0,
            international_accountability_mechanism_gap_score=6.0,
            primary_pattern="international_accountability_mechanism_gap",
        ),
    ]

    return ForcedDisappearanceExtrajudicialKillingEngineResult(
        agent="Forced Disappearance Extrajudicial Killing Engine Agent",
        domain="forced_disappearance_extrajudicial_killing",
        entities=entities,
        data_sources=[
            "un_committee_enforced_disappearances_2023",
            "amnesty_international_extrajudicial_killings_2023",
            "human_rights_watch_disappearances_database",
            "trial_international_fight_impunity_report_2023",
        ],
    )


if __name__ == "__main__":
    result = run_forced_disappearance_extrajudicial_killing_engine()
    print(f"Agent       : {result.agent}")
    print(f"Domain      : {result.domain}")
    print(f"Total       : {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index   : {result.avg_estimated_forced_disappearance_extrajudicial_killing_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print()
    for e in result.entities:
        print(f"  {e.entity_id} | {e.risk_level:8s} | {e.composite_score:5.2f} | {e.name[:60]}")
