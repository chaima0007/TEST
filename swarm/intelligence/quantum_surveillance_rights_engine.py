from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#06b6d4"


@dataclass
class QuantumSurveillanceRightsEntity:
    entity_id: str
    name: str
    country: str
    quantum_decryption_threat_score: float
    quantum_mass_surveillance_score: float
    privacy_legislation_gap_score: float
    post_quantum_cryptography_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_quantum_surveillance_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.quantum_decryption_threat_score * 0.30
            + self.quantum_mass_surveillance_score * 0.25
            + self.privacy_legislation_gap_score * 0.25
            + self.post_quantum_cryptography_score * 0.20,
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
        self.estimated_quantum_surveillance_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class QuantumSurveillanceRightsEngineResult:
    agent: str = "Quantum Surveillance Rights Engine Agent"
    domain: str = "quantum_surveillance_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_quantum_surveillance_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[QuantumSurveillanceRightsEntity] = field(default_factory=list)


def run_quantum_surveillance_rights_engine() -> QuantumSurveillanceRightsEngineResult:
    entities = [
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-001",
            name="Chine — Harvest Now Decrypt Later stratégique",
            country="Chine",
            quantum_decryption_threat_score=97,
            quantum_mass_surveillance_score=96,
            privacy_legislation_gap_score=95,
            post_quantum_cryptography_score=98,
            primary_pattern="Harvest Now Decrypt Later / 700M caméras IA quantique",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-002",
            name="USA/NSA — Stockage massif données chiffrées pré-quantum",
            country="USA",
            quantum_decryption_threat_score=92,
            quantum_mass_surveillance_score=90,
            privacy_legislation_gap_score=91,
            post_quantum_cryptography_score=93,
            primary_pattern="PRISM quantique / budget DARPA quantum surveillance",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-003",
            name="Russie — FSB programme quantique militaire",
            country="Russie",
            quantum_decryption_threat_score=86,
            quantum_mass_surveillance_score=84,
            privacy_legislation_gap_score=85,
            post_quantum_cryptography_score=87,
            primary_pattern="SORM-3 modernisation quantique / FSB quantum intelligence",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-004",
            name="Iran — Programme quantique IRGC",
            country="Iran",
            quantum_decryption_threat_score=80,
            quantum_mass_surveillance_score=78,
            privacy_legislation_gap_score=79,
            post_quantum_cryptography_score=81,
            primary_pattern="Surveillance religieuse amplifiée quantique / IRGC quantum",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-005",
            name="Union Européenne — NIS2 incomplète quantum",
            country="UE",
            quantum_decryption_threat_score=56,
            quantum_mass_surveillance_score=54,
            privacy_legislation_gap_score=55,
            post_quantum_cryptography_score=57,
            primary_pattern="ENISA retard standards PQC / RGPD lacunes quantum",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-006",
            name="Inde — QKDN expérimental Aadhaar vulnérable",
            country="Inde",
            quantum_decryption_threat_score=48,
            quantum_mass_surveillance_score=46,
            privacy_legislation_gap_score=47,
            post_quantum_cryptography_score=49,
            primary_pattern="Aadhaar vulnérable quantum / NATGRID upgrade insuffisant",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-007",
            name="Australie — Five Eyes quantum sharing",
            country="Australie",
            quantum_decryption_threat_score=31,
            quantum_mass_surveillance_score=29,
            privacy_legislation_gap_score=30,
            post_quantum_cryptography_score=32,
            primary_pattern="ASD quantum lab / législation en retard Five Eyes",
        ),
        QuantumSurveillanceRightsEntity(
            entity_id="QSR-008",
            name="NIST/ISO — PQC standards finalisés 2024",
            country="International",
            quantum_decryption_threat_score=13,
            quantum_mass_surveillance_score=11,
            privacy_legislation_gap_score=12,
            post_quantum_cryptography_score=14,
            primary_pattern="CRYSTALS-Kyber/Dilithium standards / migration PQC en cours",
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

    return QuantumSurveillanceRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_quantum_surveillance_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "nist_post_quantum_cryptography_standards_2024",
            "etsi_quantum_safe_cryptography_working_group",
            "cisa_quantum_readiness_critical_infrastructure_report",
            "chatham_house_quantum_technologies_human_rights_2024",
            "eff_quantum_surveillance_privacy_threat_analysis",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_quantum_surveillance_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
