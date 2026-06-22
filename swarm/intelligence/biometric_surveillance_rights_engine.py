#!/usr/bin/env python3
"""Biometric Surveillance Rights Engine — CaelumSwarm™ Wave 202 | CSDDD Art.8-13"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

DOMAIN_CODE = "BSR"
ACCENT_COLOR = "#581c87"


@dataclass
class BiometricSurveillanceRightsEntity:
    entity_id: str
    name: str
    country: str
    facial_recognition_mass_deployment_rights_violation_score: float
    biometric_data_collection_consent_gap_score: float
    discriminatory_algorithmic_bias_racial_profiling_score: float
    legal_framework_gdpr_compliance_accountability_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_bsr_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.facial_recognition_mass_deployment_rights_violation_score * 0.30
            + self.biometric_data_collection_consent_gap_score * 0.25
            + self.discriminatory_algorithmic_bias_racial_profiling_score * 0.25
            + self.legal_framework_gdpr_compliance_accountability_score * 0.20,
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
        self.estimated_bsr_index = round(self.composite_score / 100 * 10, 2)


@dataclass
class BiometricSurveillanceRightsEngineResult:
    agent: str = "Biometric Surveillance Rights Engine Agent"
    domain: str = "biometric_surveillance_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_bsr_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[BiometricSurveillanceRightsEntity] = field(default_factory=list)


def run_biometric_surveillance_rights_engine() -> BiometricSurveillanceRightsEngineResult:
    entities = [
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-001",
            name="Clearview AI — Base 30 Milliards Photos Scraped Sans Consentement, Ventes Police Monde Entier & Violation RGPD/BIPA Condamnations",
            country="USA",
            facial_recognition_mass_deployment_rights_violation_score=95.0,
            biometric_data_collection_consent_gap_score=93.0,
            discriminatory_algorithmic_bias_racial_profiling_score=92.0,
            legal_framework_gdpr_compliance_accountability_score=91.0,
            primary_pattern="facial_recognition_mass_deployment_rights_violation",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-002",
            name="SenseTime — Reconnaissance Faciale Surveillance Ouïghours Xinjiang, Contrats Gouvernement Chinois Répression & Blacklist USA OFAC",
            country="Chine",
            facial_recognition_mass_deployment_rights_violation_score=91.0,
            biometric_data_collection_consent_gap_score=89.0,
            discriminatory_algorithmic_bias_racial_profiling_score=88.0,
            legal_framework_gdpr_compliance_accountability_score=87.0,
            primary_pattern="discriminatory_algorithmic_bias_racial_profiling",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-003",
            name="Dahua Technology — Caméras Surveillance Biométrique Xinjiang Camps Détention, Export Régimes Autoritaires & Infrastructure Contrôle Masse",
            country="Chine",
            facial_recognition_mass_deployment_rights_violation_score=87.0,
            biometric_data_collection_consent_gap_score=85.0,
            discriminatory_algorithmic_bias_racial_profiling_score=84.0,
            legal_framework_gdpr_compliance_accountability_score=83.0,
            primary_pattern="facial_recognition_mass_deployment_rights_violation",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-004",
            name="Hikvision — Plus Grand Fabricant Caméras Surveillance Monde, Xinjiang Camps Intégration Biométrique & Export Sans Due Diligence Droits Humains",
            country="Chine",
            facial_recognition_mass_deployment_rights_violation_score=83.0,
            biometric_data_collection_consent_gap_score=81.0,
            discriminatory_algorithmic_bias_racial_profiling_score=80.0,
            legal_framework_gdpr_compliance_accountability_score=79.0,
            primary_pattern="biometric_data_collection_consent_gap",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-005",
            name="NEC Corporation — Déploiement Reconnaissance Faciale Aéroports/Frontières, Biais Algorithmiques Documentés & Contrats Gouvernements Opacité",
            country="Japon",
            facial_recognition_mass_deployment_rights_violation_score=57.0,
            biometric_data_collection_consent_gap_score=55.0,
            discriminatory_algorithmic_bias_racial_profiling_score=54.0,
            legal_framework_gdpr_compliance_accountability_score=53.0,
            primary_pattern="facial_recognition_mass_deployment_rights_violation",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-006",
            name="Thales Group — Systèmes Biométriques Contrôle Frontières/Passeports, Contrats Pays Surveillance Citoyens & Déficits Transparence Algorithmes",
            country="France",
            facial_recognition_mass_deployment_rights_violation_score=53.0,
            biometric_data_collection_consent_gap_score=51.0,
            discriminatory_algorithmic_bias_racial_profiling_score=50.0,
            legal_framework_gdpr_compliance_accountability_score=49.0,
            primary_pattern="legal_framework_gdpr_compliance_accountability",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-007",
            name="Microsoft Azure Face API — Reconnaissance Faciale Commerciale Biais Racial NIST, Moratoire Partiel Imposé & Restrictions Usage Police Annoncées",
            country="USA",
            facial_recognition_mass_deployment_rights_violation_score=27.0,
            biometric_data_collection_consent_gap_score=26.0,
            discriminatory_algorithmic_bias_racial_profiling_score=25.0,
            legal_framework_gdpr_compliance_accountability_score=25.0,
            primary_pattern="discriminatory_algorithmic_bias_racial_profiling",
        ),
        BiometricSurveillanceRightsEntity(
            entity_id="BSR-008",
            name="ACLU Digital Rights — Campagnes Contre Surveillance Biométrique, Litiges Clearview/Illinois BIPA & Lobbying Moratoire Reconnaissance Faciale",
            country="USA",
            facial_recognition_mass_deployment_rights_violation_score=5.0,
            biometric_data_collection_consent_gap_score=4.0,
            discriminatory_algorithmic_bias_racial_profiling_score=4.0,
            legal_framework_gdpr_compliance_accountability_score=4.0,
            primary_pattern="biometric_data_collection_consent_gap",
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

    return BiometricSurveillanceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_bsr_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "algorithmic_justice_league_facial_recognition_bias_audit",
            "ai_now_institute_surveillance_accountability_report",
            "amnesty_international_ban_facial_recognition_campaign",
            "nist_frvt_face_recognition_accuracy_demographic_bias_study",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_biometric_surveillance_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_bsr_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
