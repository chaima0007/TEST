from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class AiSurveillanceRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_surveillance_biometric_severity_score: float
    social_scoring_behavioral_control_scale_score: float
    predictive_policing_racial_targeting_score: float
    data_privacy_algorithmic_accountability_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_ai_surveillance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_surveillance_biometric_severity_score * 0.30
            + self.social_scoring_behavioral_control_scale_score * 0.25
            + self.predictive_policing_racial_targeting_score * 0.25
            + self.data_privacy_algorithmic_accountability_gap_score * 0.20,
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
        self.estimated_ai_surveillance_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class AiSurveillanceRightsEngineResult:
    agent: str = "AI Surveillance Rights Engine Agent"
    domain: str = "ai_surveillance_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_ai_surveillance_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[AiSurveillanceRightsEntity] = field(default_factory=list)

def run_ai_surveillance_rights_engine() -> AiSurveillanceRightsEngineResult:
    entities = [
        AiSurveillanceRightsEntity(
            entity_id="ASR-001",
            name="China — SCS Social Credit System 1,4Md, Xinjiang Surveillance Totale & 700M Caméras CCTV AI",
            country="Chine",
            mass_surveillance_biometric_severity_score=96.0,
            social_scoring_behavioral_control_scale_score=94.0,
            predictive_policing_racial_targeting_score=93.0,
            data_privacy_algorithmic_accountability_gap_score=92.0,
            primary_pattern="mass_surveillance_biometric_severity",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-002",
            name="Russia — SORM Surveillance Totale, Reconnaissance Faciale Moscou 200k Caméras & Militants Ciblés",
            country="Russie",
            mass_surveillance_biometric_severity_score=93.0,
            social_scoring_behavioral_control_scale_score=90.0,
            predictive_policing_racial_targeting_score=91.0,
            data_privacy_algorithmic_accountability_gap_score=89.0,
            primary_pattern="mass_surveillance_biometric_severity",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-003",
            name="Iran — Surveillance Internet Filtrée, AI Reconnaisance Protestataires 2022 & Arrestations Algorithme",
            country="Iran",
            mass_surveillance_biometric_severity_score=90.0,
            social_scoring_behavioral_control_scale_score=87.0,
            predictive_policing_racial_targeting_score=88.0,
            data_privacy_algorithmic_accountability_gap_score=86.0,
            primary_pattern="predictive_policing_racial_targeting",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-004",
            name="India — Aadhaar Biométrique 1,4Md, Surveillance Cachemire & Facial Recognition Manifestants CAA",
            country="Inde",
            mass_surveillance_biometric_severity_score=87.0,
            social_scoring_behavioral_control_scale_score=84.0,
            predictive_policing_racial_targeting_score=85.0,
            data_privacy_algorithmic_accountability_gap_score=83.0,
            primary_pattern="mass_surveillance_biometric_severity",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-005",
            name="USA — Clearview AI 30Md Visages, Predictive Policing Chicago/LA & NYPD Drone Surveillance",
            country="USA",
            mass_surveillance_biometric_severity_score=56.0,
            social_scoring_behavioral_control_scale_score=53.0,
            predictive_policing_racial_targeting_score=55.0,
            data_privacy_algorithmic_accountability_gap_score=51.0,
            primary_pattern="predictive_policing_racial_targeting",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-006",
            name="Europe — ANPR London Ring of Steel, Belgique Clearview Ban, IA Act Implemention Gap",
            country="Europe",
            mass_surveillance_biometric_severity_score=53.0,
            social_scoring_behavioral_control_scale_score=50.0,
            predictive_policing_racial_targeting_score=51.0,
            data_privacy_algorithmic_accountability_gap_score=49.0,
            primary_pattern="data_privacy_algorithmic_accountability_gap",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-007",
            name="EFF/Amnesty Tech — Ban Facial Recognition Campagne, Algorithmic Accountability & GDPR Enforcement",
            country="Global",
            mass_surveillance_biometric_severity_score=27.0,
            social_scoring_behavioral_control_scale_score=25.0,
            predictive_policing_racial_targeting_score=26.0,
            data_privacy_algorithmic_accountability_gap_score=25.0,
            primary_pattern="mass_surveillance_biometric_severity",
        ),
        AiSurveillanceRightsEntity(
            entity_id="ASR-008",
            name="ONU/OHCHR — Rapport IA Droits Homme, Cadre Réglementation & SDG 16.10 Accès Information",
            country="Global",
            mass_surveillance_biometric_severity_score=4.0,
            social_scoring_behavioral_control_scale_score=4.0,
            predictive_policing_racial_targeting_score=4.0,
            data_privacy_algorithmic_accountability_gap_score=5.0,
            primary_pattern="data_privacy_algorithmic_accountability_gap",
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

    return AiSurveillanceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_ai_surveillance_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "amnesty_international_surveillance_giants_ai_report",
            "eff_atlas_of_surveillance_2023",
            "ohchr_right_to_privacy_digital_age_report",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_ai_surveillance_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_ai_surveillance_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
