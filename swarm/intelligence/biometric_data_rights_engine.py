from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#0284c7"


@dataclass
class BiometricDataRightsEntity:
    entity_id: str
    name: str
    country: str
    mass_biometric_collection_score: float
    facial_recognition_misuse_score: float
    biometric_database_leak_score: float
    consent_framework_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_biometric_data_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.mass_biometric_collection_score * 0.30
            + self.facial_recognition_misuse_score * 0.25
            + self.biometric_database_leak_score * 0.25
            + self.consent_framework_gap_score * 0.20,
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
        self.estimated_biometric_data_rights_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class BiometricDataRightsEngineResult:
    agent: str = "Biometric Data Rights Engine Agent"
    domain: str = "biometric_data_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_biometric_data_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BiometricDataRightsEntity] = field(default_factory=list)


def run_biometric_data_rights_engine() -> BiometricDataRightsEngineResult:
    entities = [
        BiometricDataRightsEntity(
            entity_id="BDR-001",
            name="Chine — SCS 700M visages, Système Crédit Social biométrique, minorités Ouïghours",
            country="Chine",
            mass_biometric_collection_score=97.0,
            facial_recognition_misuse_score=96.0,
            biometric_database_leak_score=94.0,
            consent_framework_gap_score=95.0,
            primary_pattern="mass_biometric_collection",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-002",
            name="Russie — 200 000 caméras Moscou reconnaissance faciale, SORM identifications dissidents",
            country="Russie",
            mass_biometric_collection_score=90.0,
            facial_recognition_misuse_score=92.0,
            biometric_database_leak_score=88.0,
            consent_framework_gap_score=89.0,
            primary_pattern="facial_recognition_misuse",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-003",
            name="Inde — Aadhaar 1.4Md biométriques, fuites 2023 (815M dossiers), UIDAI sans contrôle",
            country="Inde",
            mass_biometric_collection_score=85.0,
            facial_recognition_misuse_score=83.0,
            biometric_database_leak_score=88.0,
            consent_framework_gap_score=82.0,
            primary_pattern="biometric_database_leak",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-004",
            name="USA — Clearview AI 30Md images scrapées, ICE déploiement sans cadre légal",
            country="USA",
            mass_biometric_collection_score=76.0,
            facial_recognition_misuse_score=78.0,
            biometric_database_leak_score=74.0,
            consent_framework_gap_score=72.0,
            primary_pattern="facial_recognition_misuse",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-005",
            name="Israël — West Bank biométrique palestiniens sans consentement, Blue Wolf app",
            country="Israël",
            mass_biometric_collection_score=54.0,
            facial_recognition_misuse_score=58.0,
            biometric_database_leak_score=52.0,
            consent_framework_gap_score=56.0,
            primary_pattern="consent_framework_gap",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-006",
            name="Émirats Arabes — Abu Dhabi biométrie aéroports sans opt-out, données partagées",
            country="Émirats Arabes",
            mass_biometric_collection_score=46.0,
            facial_recognition_misuse_score=48.0,
            biometric_database_leak_score=44.0,
            consent_framework_gap_score=50.0,
            primary_pattern="consent_framework_gap",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-007",
            name="UK — King&apos;s Cross FRT retiré 2019, LFR déployé Metropolitan Police, GDPR partiel",
            country="UK",
            mass_biometric_collection_score=28.0,
            facial_recognition_misuse_score=30.0,
            biometric_database_leak_score=26.0,
            consent_framework_gap_score=24.0,
            primary_pattern="facial_recognition_misuse",
        ),
        BiometricDataRightsEntity(
            entity_id="BDR-008",
            name="UE — AI Act 2024 interdit FRT espace public, GDPR biométrique article 9, modèle mondial",
            country="UE",
            mass_biometric_collection_score=7.0,
            facial_recognition_misuse_score=6.0,
            biometric_database_leak_score=8.0,
            consent_framework_gap_score=5.0,
            primary_pattern="mass_biometric_collection",
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

    return BiometricDataRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_biometric_data_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "ai_now_institute_biometric_surveillance_2024",
            "access_now_digital_rights_biometrics_report",
            "hrw_facial_recognition_rights_violations",
            "edri_biometric_mass_surveillance_eu_2024",
            "article_19_biometric_data_rights_global",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_biometric_data_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
