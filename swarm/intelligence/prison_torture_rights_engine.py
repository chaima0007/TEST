from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class PrisonTortureRightsEntity:
    entity_id: str
    name: str
    country: str
    torture_cruel_treatment_custodial_severity_score: float
    prison_overcrowding_inhuman_conditions_scale_score: float
    solitary_confinement_prolonged_abuse_score: float
    accountability_impunity_custodial_deaths_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_prison_torture_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.torture_cruel_treatment_custodial_severity_score * 0.30
            + self.prison_overcrowding_inhuman_conditions_scale_score * 0.25
            + self.solitary_confinement_prolonged_abuse_score * 0.25
            + self.accountability_impunity_custodial_deaths_gap_score * 0.20,
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
        self.estimated_prison_torture_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class PrisonTortureRightsEngineResult:
    agent: str = "Prison Torture Rights Engine Agent"
    domain: str = "prison_torture_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_prison_torture_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[PrisonTortureRightsEntity] = field(default_factory=list)

def run_prison_torture_rights_engine() -> PrisonTortureRightsEngineResult:
    entities = [
        PrisonTortureRightsEntity(
            entity_id="PTR-001",
            name="Mexique/Amérique Centrale — Torture Systématique Police, Prisons Surpeuplées 300%, Disparitions Custodiales & Narco-Corruption",
            country="Mexique",
            torture_cruel_treatment_custodial_severity_score=95.0,
            prison_overcrowding_inhuman_conditions_scale_score=93.0,
            solitary_confinement_prolonged_abuse_score=91.0,
            accountability_impunity_custodial_deaths_gap_score=93.0,
            primary_pattern="torture_cruel_treatment_custodial_severity",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-002",
            name="Chine/Xinjiang — Torture Ouïghours Camps Détention, Soins Médicaux Refusés, Disparitions & Morts Politiques Étranges",
            country="Chine",
            torture_cruel_treatment_custodial_severity_score=92.0,
            prison_overcrowding_inhuman_conditions_scale_score=89.0,
            solitary_confinement_prolonged_abuse_score=91.0,
            accountability_impunity_custodial_deaths_gap_score=89.0,
            primary_pattern="solitary_confinement_prolonged_abuse",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-003",
            name="Philippines/Guerre Drogue — 30 000 Tués Custodiales Duterte, Torture Arrêtés, Prisons 500% & Impunité Totale",
            country="Philippines",
            torture_cruel_treatment_custodial_severity_score=89.0,
            prison_overcrowding_inhuman_conditions_scale_score=88.0,
            solitary_confinement_prolonged_abuse_score=85.0,
            accountability_impunity_custodial_deaths_gap_score=87.0,
            primary_pattern="prison_overcrowding_inhuman_conditions_scale",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-004",
            name="Arabie Saoudite/Émirats — Torture Prisonniers Politiques, Isolement, Électrochocs & Aveux Forcés Dissidents",
            country="Arabie Saoudite",
            torture_cruel_treatment_custodial_severity_score=86.0,
            prison_overcrowding_inhuman_conditions_scale_score=82.0,
            solitary_confinement_prolonged_abuse_score=86.0,
            accountability_impunity_custodial_deaths_gap_score=84.0,
            primary_pattern="solitary_confinement_prolonged_abuse",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-005",
            name="USA/Solitary Confinement — 80 000 Prisonniers Isolement, SHU California 10+ Ans & Violence Guards Impunie",
            country="USA",
            torture_cruel_treatment_custodial_severity_score=55.0,
            prison_overcrowding_inhuman_conditions_scale_score=52.0,
            solitary_confinement_prolonged_abuse_score=57.0,
            accountability_impunity_custodial_deaths_gap_score=52.0,
            primary_pattern="solitary_confinement_prolonged_abuse",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-006",
            name="Inde/Détentions Arbitraires — Custodial Deaths 1700/An, Torture Dalits/Minorités, Prisons Surpeuplées & UAPA",
            country="Inde",
            torture_cruel_treatment_custodial_severity_score=53.0,
            prison_overcrowding_inhuman_conditions_scale_score=52.0,
            solitary_confinement_prolonged_abuse_score=50.0,
            accountability_impunity_custodial_deaths_gap_score=49.0,
            primary_pattern="torture_cruel_treatment_custodial_severity",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-007",
            name="CPT/SPT/APT — Comité Prévention Torture ONU, Visites Préventives & Lignes Directrices Nelson Mandela",
            country="Global",
            torture_cruel_treatment_custodial_severity_score=27.0,
            prison_overcrowding_inhuman_conditions_scale_score=26.0,
            solitary_confinement_prolonged_abuse_score=25.0,
            accountability_impunity_custodial_deaths_gap_score=26.0,
            primary_pattern="accountability_impunity_custodial_deaths_gap",
        ),
        PrisonTortureRightsEntity(
            entity_id="PTR-008",
            name="ONU/CAT/OPCAT — Convention Anti-Torture 1984, Protocole Facultatif OPCAT & SDG 16.3 État de Droit",
            country="Global",
            torture_cruel_treatment_custodial_severity_score=4.0,
            prison_overcrowding_inhuman_conditions_scale_score=4.0,
            solitary_confinement_prolonged_abuse_score=4.0,
            accountability_impunity_custodial_deaths_gap_score=5.0,
            primary_pattern="accountability_impunity_custodial_deaths_gap",
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

    return PrisonTortureRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_prison_torture_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "un_committee_against_torture_annual_report",
            "amnesty_international_custodial_torture_global_review",
            "human_rights_watch_prison_conditions_overcrowding_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_prison_torture_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_prison_torture_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
