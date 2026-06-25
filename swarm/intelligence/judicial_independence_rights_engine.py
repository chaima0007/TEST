from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class JudicialIndependenceRightsEntity:
    entity_id: str
    name: str
    country: str
    executive_judiciary_capture_severity_score: float
    judicial_appointment_politicization_scale_score: float
    judge_persecution_harassment_risk_score: float
    court_packing_restructuring_abuse_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_judicial_independence_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.executive_judiciary_capture_severity_score * 0.30
            + self.judicial_appointment_politicization_scale_score * 0.25
            + self.judge_persecution_harassment_risk_score * 0.25
            + self.court_packing_restructuring_abuse_gap_score * 0.20,
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
        self.estimated_judicial_independence_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class JudicialIndependenceRightsEngineResult:
    agent: str = "Judicial Independence Rights Engine Agent"
    domain: str = "judicial_independence_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_judicial_independence_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[JudicialIndependenceRightsEntity] = field(default_factory=list)

def run_judicial_independence_rights_engine() -> JudicialIndependenceRightsEngineResult:
    entities = [
        JudicialIndependenceRightsEntity(
            entity_id="JIR-001",
            name="Hongrie/Orbán — Réforme Constitutionnelle 2011-19, Cour Suprême Vidée, Procureur Général Allié & Juges Fidèles Nommés",
            country="Hongrie",
            executive_judiciary_capture_severity_score=96.0,
            judicial_appointment_politicization_scale_score=94.0,
            judge_persecution_harassment_risk_score=91.0,
            court_packing_restructuring_abuse_gap_score=93.0,
            primary_pattern="executive_judiciary_capture_severity",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-002",
            name="Turquie Post-2016 — 4 000 Juges Destitués Coup d'État, Tribunaux Spéciaux Terrorisme, Erdoğan Contrôle Judiciaire",
            country="Turquie",
            executive_judiciary_capture_severity_score=93.0,
            judicial_appointment_politicization_scale_score=91.0,
            judge_persecution_harassment_risk_score=92.0,
            court_packing_restructuring_abuse_gap_score=88.0,
            primary_pattern="judge_persecution_harassment_risk",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-003",
            name="Venezuela/Maduro — CSJ Peuplée Chavistes, 100% Acquittements Demandés Exécutif, Juges Exil & Prisonniers Politiques",
            country="Venezuela",
            executive_judiciary_capture_severity_score=91.0,
            judicial_appointment_politicization_scale_score=89.0,
            judge_persecution_harassment_risk_score=85.0,
            court_packing_restructuring_abuse_gap_score=86.0,
            primary_pattern="executive_judiciary_capture_severity",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-004",
            name="Pologne/PiS 2015-23 — Tribunal Constitutionnel Paralysé, KRS Politisé, Sanctions EU Infringement & Réforme Réversée",
            country="Pologne",
            executive_judiciary_capture_severity_score=87.0,
            judicial_appointment_politicization_scale_score=86.0,
            judge_persecution_harassment_risk_score=82.0,
            court_packing_restructuring_abuse_gap_score=84.0,
            primary_pattern="court_packing_restructuring_abuse_gap",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-005",
            name="Pakistan/Bangladesh — ISI Pression Magistrats, Arrêts Politiques Opportuns, Blasphème Poursuites & Avocats Attaqués",
            country="Pakistan",
            executive_judiciary_capture_severity_score=57.0,
            judicial_appointment_politicization_scale_score=55.0,
            judge_persecution_harassment_risk_score=54.0,
            court_packing_restructuring_abuse_gap_score=52.0,
            primary_pattern="executive_judiciary_capture_severity",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-006",
            name="USA/Trump 2025 — Tentatives Influence SCOTUS, Purge FBI/DOJ, Procureurs Spéciaux Révoqués & Juges Fédéraux Intimidés",
            country="USA",
            executive_judiciary_capture_severity_score=54.0,
            judicial_appointment_politicization_scale_score=53.0,
            judge_persecution_harassment_risk_score=51.0,
            court_packing_restructuring_abuse_gap_score=50.0,
            primary_pattern="executive_judiciary_capture_severity",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-007",
            name="ICJ/Venice Commission — Avis Conformité État de Droit, Indépendance Standards & Rapports Commission Venise",
            country="Global",
            executive_judiciary_capture_severity_score=28.0,
            judicial_appointment_politicization_scale_score=27.0,
            judge_persecution_harassment_risk_score=26.0,
            court_packing_restructuring_abuse_gap_score=25.0,
            primary_pattern="court_packing_restructuring_abuse_gap",
        ),
        JudicialIndependenceRightsEntity(
            entity_id="JIR-008",
            name="ONU/CCPR — Principe Indépendance Judiciaire 1985, CCPR Art.14 Procès Équitable & SDG 16.3 Accès Justice",
            country="Global",
            executive_judiciary_capture_severity_score=4.0,
            judicial_appointment_politicization_scale_score=4.0,
            judge_persecution_harassment_risk_score=4.0,
            court_packing_restructuring_abuse_gap_score=4.0,
            primary_pattern="executive_judiciary_capture_severity",
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

    return JudicialIndependenceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_judicial_independence_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "venice_commission_rule_of_law_reports",
            "icj_judicial_independence_standards",
            "amnesty_international_judicial_persecution_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_judicial_independence_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_judicial_independence_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
