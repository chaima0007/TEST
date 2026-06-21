from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ChildSoldiersRightsEntity:
    entity_id: str
    name: str
    country: str
    forced_recruitment_underage_severity_score: float
    demobilization_reintegration_failure_scale_score: float
    sexual_violence_child_combatant_score: float
    accountability_commander_liability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_child_soldiers_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.forced_recruitment_underage_severity_score * 0.30
            + self.demobilization_reintegration_failure_scale_score * 0.25
            + self.sexual_violence_child_combatant_score * 0.25
            + self.accountability_commander_liability_gap_score * 0.20,
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
        self.estimated_child_soldiers_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ChildSoldiersRightsEngineResult:
    agent: str = "Child Soldiers Rights Engine Agent"
    domain: str = "child_soldiers_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_child_soldiers_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ChildSoldiersRightsEntity] = field(default_factory=list)

def run_child_soldiers_rights_engine() -> ChildSoldiersRightsEngineResult:
    entities = [
        ChildSoldiersRightsEntity(
            entity_id="CSR-001",
            name="DRC — 15 000+ Enfants Soldats Actifs, M23/ADF & Muliples Groupes Armés, Recrutement Continu",
            country="RDC",
            forced_recruitment_underage_severity_score=96.0,
            demobilization_reintegration_failure_scale_score=93.0,
            sexual_violence_child_combatant_score=94.0,
            accountability_commander_liability_gap_score=92.0,
            primary_pattern="forced_recruitment_underage_severity",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-002",
            name="South Sudan — 19 000 Enfants Libérés 2018-23, Rechutes Recrutement & Viols Systématiques",
            country="Soudan du Sud",
            forced_recruitment_underage_severity_score=93.0,
            demobilization_reintegration_failure_scale_score=90.0,
            sexual_violence_child_combatant_score=91.0,
            accountability_commander_liability_gap_score=89.0,
            primary_pattern="sexual_violence_child_combatant",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-003",
            name="Myanmar — Tatmadaw Recrutement Enfants Documenté ONU, Post-Coup 2021 & Groupes Ethniques",
            country="Myanmar",
            forced_recruitment_underage_severity_score=90.0,
            demobilization_reintegration_failure_scale_score=87.0,
            sexual_violence_child_combatant_score=88.0,
            accountability_commander_liability_gap_score=86.0,
            primary_pattern="forced_recruitment_underage_severity",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-004",
            name="Sahel/Mali-Burkina — JNIM/GSIM Recrutement Enfants, Kamikazes Mineurs & Zéro DDR Fonctionnel",
            country="Sahel",
            forced_recruitment_underage_severity_score=87.0,
            demobilization_reintegration_failure_scale_score=84.0,
            sexual_violence_child_combatant_score=85.0,
            accountability_commander_liability_gap_score=83.0,
            primary_pattern="demobilization_reintegration_failure_scale",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-005",
            name="Yémen — Coalition+Houthis Recrutement Documenté, 3 700+ Enfants Vérifiés UNICEF 2023",
            country="Yémen",
            forced_recruitment_underage_severity_score=56.0,
            demobilization_reintegration_failure_scale_score=53.0,
            sexual_violence_child_combatant_score=54.0,
            accountability_commander_liability_gap_score=52.0,
            primary_pattern="forced_recruitment_underage_severity",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-006",
            name="Somalie/Al-Shabaab — Recrutement Forcé Madrasas, Attentats Mineurs & AMISOM Incapacité",
            country="Somalie",
            forced_recruitment_underage_severity_score=53.0,
            demobilization_reintegration_failure_scale_score=50.0,
            sexual_violence_child_combatant_score=51.0,
            accountability_commander_liability_gap_score=49.0,
            primary_pattern="accountability_commander_liability_gap",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-007",
            name="UNICEF/Child Soldiers International — DDR Enfants, Plaidoyer Protocole Facultatif & Réhabilitation",
            country="Global",
            forced_recruitment_underage_severity_score=27.0,
            demobilization_reintegration_failure_scale_score=26.0,
            sexual_violence_child_combatant_score=25.0,
            accountability_commander_liability_gap_score=26.0,
            primary_pattern="demobilization_reintegration_failure_scale",
        ),
        ChildSoldiersRightsEntity(
            entity_id="CSR-008",
            name="ONU/Protocole Facultatif — OPAC 2002, Mécanisme MRM Surveillance & SDG 16.2 Violence Enfants",
            country="Global",
            forced_recruitment_underage_severity_score=4.0,
            demobilization_reintegration_failure_scale_score=4.0,
            sexual_violence_child_combatant_score=4.0,
            accountability_commander_liability_gap_score=4.0,
            primary_pattern="accountability_commander_liability_gap",
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

    return ChildSoldiersRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_child_soldiers_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "unicef_children_and_armed_conflict_annual_report",
            "child_soldiers_international_global_report",
            "un_security_council_mrm_monitoring_reporting_mechanism",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_child_soldiers_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_child_soldiers_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
