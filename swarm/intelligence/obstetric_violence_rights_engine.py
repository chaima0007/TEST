from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class ObstetricViolenceRightsEntity:
    entity_id: str
    name: str
    country: str
    physical_obstetric_abuse_severity_score: float
    informed_consent_violation_scale_score: float
    legal_accountability_gap_score: float
    institutional_denial_minimization_pattern_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_obstetric_violence_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.physical_obstetric_abuse_severity_score * 0.30
            + self.informed_consent_violation_scale_score * 0.25
            + self.legal_accountability_gap_score * 0.25
            + self.institutional_denial_minimization_pattern_score * 0.20,
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
        self.estimated_obstetric_violence_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class ObstetricViolenceRightsEngineResult:
    agent: str = "Obstetric Violence Rights Engine Agent"
    domain: str = "obstetric_violence_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_obstetric_violence_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[ObstetricViolenceRightsEntity] = field(default_factory=list)

def run_obstetric_violence_rights_engine() -> ObstetricViolenceRightsEngineResult:
    entities = [
        ObstetricViolenceRightsEntity(
            entity_id="OVR-001",
            name="Venezuela/Amérique Latine — Stérilisations Forcées, Épisiotomies Non Consenties & Zéro Recours",
            country="Amérique Latine",
            physical_obstetric_abuse_severity_score=95.0,
            informed_consent_violation_scale_score=92.0,
            legal_accountability_gap_score=95.0,
            institutional_denial_minimization_pattern_score=92.0,
            primary_pattern="physical_obstetric_abuse_severity",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-002",
            name="Inde — 45% Accouchements Sans Consentement, Humiliations Publiques & Discrimination Caste Maternité",
            country="Asie du Sud",
            physical_obstetric_abuse_severity_score=90.0,
            informed_consent_violation_scale_score=95.0,
            legal_accountability_gap_score=88.0,
            institutional_denial_minimization_pattern_score=88.0,
            primary_pattern="informed_consent_violation_scale",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-003",
            name="Afrique Sub-Sah. — Mortalité Maternelle 542/100K, Violences Obstétriques Documentées OMS",
            country="Afrique",
            physical_obstetric_abuse_severity_score=92.0,
            informed_consent_violation_scale_score=88.0,
            legal_accountability_gap_score=88.0,
            institutional_denial_minimization_pattern_score=85.0,
            primary_pattern="physical_obstetric_abuse_severity",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-004",
            name="Mexique/Brésil — Terme Légal 'Violence Obstétricale' 2007, 90% Cas Non Poursuivis",
            country="Amérique Latine",
            physical_obstetric_abuse_severity_score=85.0,
            informed_consent_violation_scale_score=85.0,
            legal_accountability_gap_score=90.0,
            institutional_denial_minimization_pattern_score=88.0,
            primary_pattern="legal_accountability_gap",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-005",
            name="USA — 1/6 Femmes Reportent Maltraitance Maternité, Mortalité Noires 3x Plus & Silence Médical",
            country="Amérique du Nord",
            physical_obstetric_abuse_severity_score=52.0,
            informed_consent_violation_scale_score=55.0,
            legal_accountability_gap_score=55.0,
            institutional_denial_minimization_pattern_score=52.0,
            primary_pattern="informed_consent_violation_scale",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-006",
            name="France — 1 Femme/5 Victime Maltraitance Maternité (Rapport HCE 2018), Déni Institutionnel",
            country="Europe",
            physical_obstetric_abuse_severity_score=50.0,
            informed_consent_violation_scale_score=52.0,
            legal_accountability_gap_score=52.0,
            institutional_denial_minimization_pattern_score=55.0,
            primary_pattern="institutional_denial_minimization_pattern",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-007",
            name="FIGO/OMS — Déclaration Prévention Violence Obstétricale 2019, Standards Consentement",
            country="Global",
            physical_obstetric_abuse_severity_score=22.0,
            informed_consent_violation_scale_score=28.0,
            legal_accountability_gap_score=25.0,
            institutional_denial_minimization_pattern_score=30.0,
            primary_pattern="legal_accountability_gap",
        ),
        ObstetricViolenceRightsEntity(
            entity_id="OVR-008",
            name="ONU/OHCHR — Rapport Spécial Torture Soins Santé, CEDAW Art.12 Santé Reproductive",
            country="Global",
            physical_obstetric_abuse_severity_score=4.0,
            informed_consent_violation_scale_score=5.0,
            legal_accountability_gap_score=3.0,
            institutional_denial_minimization_pattern_score=6.0,
            primary_pattern="institutional_denial_minimization_pattern",
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

    return ObstetricViolenceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_obstetric_violence_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "who_figo_prevention_elimination_disrespect_abuse_childbirth_report",
            "ohchr_special_rapporteur_torture_healthcare_obstetric_violence_review",
            "human_rights_watch_obstetric_violence_latin_america_india_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_obstetric_violence_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_obstetric_violence_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
