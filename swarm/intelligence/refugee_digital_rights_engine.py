from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

@dataclass
class RefugeeDigitalRightsEntity:
    entity_id: str
    name: str
    country: str
    biometric_data_coercion_scale_score: float
    digital_exclusion_service_denial_severity_score: float
    surveillance_control_refugee_population_score: float
    data_sharing_persecution_risk_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_refugee_digital_rights_index: float = field(init=False)
    last_updated: str = "2026-06-21"

    def __post_init__(self):
        self.composite_score = round(
            self.biometric_data_coercion_scale_score * 0.30
            + self.digital_exclusion_service_denial_severity_score * 0.25
            + self.surveillance_control_refugee_population_score * 0.25
            + self.data_sharing_persecution_risk_gap_score * 0.20,
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
        self.estimated_refugee_digital_rights_index = round(self.composite_score / 100 * 10, 2)

@dataclass
class RefugeeDigitalRightsEngineResult:
    agent: str = "Refugee Digital Rights Engine Agent"
    domain: str = "refugee_digital_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.84
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-21"
    engine_version: str = "1.0.0"
    avg_estimated_refugee_digital_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[RefugeeDigitalRightsEntity] = field(default_factory=list)

def run_refugee_digital_rights_engine() -> RefugeeDigitalRightsEngineResult:
    entities = [
        RefugeeDigitalRightsEntity(
            entity_id="RDR-001",
            name="Bangladesh/Rohingyas — UNHCR Biométrie Forcée, Données Partagées Myanmar & Camp Numérique",
            country="Asie du Sud",
            biometric_data_coercion_scale_score=95.0,
            digital_exclusion_service_denial_severity_score=88.0,
            surveillance_control_refugee_population_score=92.0,
            data_sharing_persecution_risk_gap_score=95.0,
            primary_pattern="data_sharing_persecution_risk_gap",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-002",
            name="Jordanie/Liban — 1,5M Syriens, SIM Biométrique Obligatoire & Surveillance Téléphonie",
            country="Moyen-Orient",
            biometric_data_coercion_scale_score=92.0,
            digital_exclusion_service_denial_severity_score=90.0,
            surveillance_control_refugee_population_score=92.0,
            data_sharing_persecution_risk_gap_score=88.0,
            primary_pattern="surveillance_control_refugee_population",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-003",
            name="Kenya/Dadaab — Biométrie UNHCR, Couverture Internet 3%, Services Numériques Bloqués Réfugiés",
            country="Afrique de l'Est",
            biometric_data_coercion_scale_score=88.0,
            digital_exclusion_service_denial_severity_score=92.0,
            surveillance_control_refugee_population_score=85.0,
            data_sharing_persecution_risk_gap_score=88.0,
            primary_pattern="digital_exclusion_service_denial_severity",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-004",
            name="UE/Eurodac — Empreintes Digitales Demandeurs Asile, Interopérabilité Bases Police & Leaks",
            country="Europe",
            biometric_data_coercion_scale_score=88.0,
            digital_exclusion_service_denial_severity_score=82.0,
            surveillance_control_refugee_population_score=88.0,
            data_sharing_persecution_risk_gap_score=88.0,
            primary_pattern="biometric_data_coercion_scale",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-005",
            name="Turquie — 3,6M Syriens, Surveillance Apps, Expulsions Via Données Téléphoniques",
            country="Europe/Asie",
            biometric_data_coercion_scale_score=55.0,
            digital_exclusion_service_denial_severity_score=52.0,
            surveillance_control_refugee_population_score=55.0,
            data_sharing_persecution_risk_gap_score=52.0,
            primary_pattern="biometric_data_coercion_scale",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-006",
            name="Australie — Offshore Processing Numérique, Surveillance Manus/Nauru & IMSI Catchers Camps",
            country="Océanie",
            biometric_data_coercion_scale_score=52.0,
            digital_exclusion_service_denial_severity_score=55.0,
            surveillance_control_refugee_population_score=52.0,
            data_sharing_persecution_risk_gap_score=50.0,
            primary_pattern="digital_exclusion_service_denial_severity",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-007",
            name="Privacy International/UNHCR — Data Protection Réfugiés, Biométrie Éthique & Do No Harm",
            country="Global",
            biometric_data_coercion_scale_score=22.0,
            digital_exclusion_service_denial_severity_score=28.0,
            surveillance_control_refugee_population_score=25.0,
            data_sharing_persecution_risk_gap_score=30.0,
            primary_pattern="data_sharing_persecution_risk_gap",
        ),
        RefugeeDigitalRightsEntity(
            entity_id="RDR-008",
            name="ONU/HCR — Convention Réfugiés 1951, SDG 16 Identité Légale & RGPD Personnes Déplacées",
            country="Global",
            biometric_data_coercion_scale_score=4.0,
            digital_exclusion_service_denial_severity_score=5.0,
            surveillance_control_refugee_population_score=3.0,
            data_sharing_persecution_risk_gap_score=6.0,
            primary_pattern="surveillance_control_refugee_population",
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

    return RefugeeDigitalRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_refugee_digital_rights_index=round(avg_composite / 100 * 10, 2),
        data_sources=[
            "privacy_international_unhcr_biometric_data_refugee_rights_report",
            "human_rights_watch_digital_id_surveillance_refugees_global_review",
            "alan_turing_institute_data_protection_displaced_populations_study",
        ],
        entities=entities,
    )

if __name__ == "__main__":
    result = run_refugee_digital_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Total entities: {result.total_entities}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Avg index: {result.avg_estimated_refugee_digital_rights_index}")
    print(f"Risk distribution: {result.risk_distribution}")
    print(f"Pattern distribution: {result.pattern_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
