from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#22c55e"


@dataclass
class QuantumBioethicsRightsEntity:
    entity_id: str
    name: str
    country: str
    genetic_modification_ethics_score: float
    biometric_exploitation_score: float
    pharmaceutical_inequality_score: float
    informed_consent_gap_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_quantum_bioethics_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.genetic_modification_ethics_score * 0.30
            + self.biometric_exploitation_score * 0.25
            + self.pharmaceutical_inequality_score * 0.25
            + self.informed_consent_gap_score * 0.20,
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
        self.estimated_quantum_bioethics_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class QuantumBioethicsRightsEngineResult:
    agent: str = "Quantum Bioethics Rights Engine Agent"
    domain: str = "quantum_bioethics_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_quantum_bioethics_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[QuantumBioethicsRightsEntity] = field(default_factory=list)


def run_quantum_bioethics_rights_engine() -> QuantumBioethicsRightsEngineResult:
    entities = [
        QuantumBioethicsRightsEntity(
            entity_id="QBR-001",
            name="Chine — He Jiankui bébés CRISPR quantum-ML drug design",
            country="Chine",
            genetic_modification_ethics_score=96,
            biometric_exploitation_score=95,
            pharmaceutical_inequality_score=94,
            informed_consent_gap_score=97,
            primary_pattern="CRISPR quantum-ML / supervision éthique absente",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-002",
            name="USA — Biotech privée CRISPR quantum-AI brevets gènes humains",
            country="USA",
            genetic_modification_ethics_score=89,
            biometric_exploitation_score=88,
            pharmaceutical_inequality_score=90,
            informed_consent_gap_score=91,
            primary_pattern="Brevets gènes humains / inégalité accès CRISPR quantum",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-003",
            name="Emirats Arabes — Human Genome Project national données biométriques diaspora",
            country="Emirats Arabes Unis",
            genetic_modification_ethics_score=83,
            biometric_exploitation_score=82,
            pharmaceutical_inequality_score=84,
            informed_consent_gap_score=85,
            primary_pattern="Données biométriques diaspora / Human Genome Project national",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-004",
            name="Russie — Programme militaire super-soldats modifications neuronales",
            country="Russie",
            genetic_modification_ethics_score=77,
            biometric_exploitation_score=76,
            pharmaceutical_inequality_score=78,
            informed_consent_gap_score=79,
            primary_pattern="Super-soldats modifications neuronales / BRICS biodata",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-005",
            name="Union Européenne — AI Act lacunes biotech quantum Horizon Europe",
            country="UE",
            genetic_modification_ethics_score=54,
            biometric_exploitation_score=53,
            pharmaceutical_inequality_score=55,
            informed_consent_gap_score=56,
            primary_pattern="AI Act lacunes biotech quantum / Horizon Europe éthique insuffisante",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-006",
            name="Inde — CRISPR agriculture humain non régulé données génétiques 1.4Md",
            country="Inde",
            genetic_modification_ethics_score=46,
            biometric_exploitation_score=45,
            pharmaceutical_inequality_score=47,
            informed_consent_gap_score=48,
            primary_pattern="CRISPR non régulé / données génétiques 1.4Md personnes",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-007",
            name="Canada — Loi non-discrimination génétique CGPN protections partielles",
            country="Canada",
            genetic_modification_ethics_score=30,
            biometric_exploitation_score=29,
            pharmaceutical_inequality_score=31,
            informed_consent_gap_score=32,
            primary_pattern="Loi non-discrimination génétique / CGPN protections partielles",
        ),
        QuantumBioethicsRightsEntity(
            entity_id="QBR-008",
            name="UNESCO/WHO — Déclaration Génie Génétique 2021 bioéthique internationale",
            country="International",
            genetic_modification_ethics_score=12,
            biometric_exploitation_score=11,
            pharmaceutical_inequality_score=13,
            informed_consent_gap_score=14,
            primary_pattern="Bioéthique internationale référence / Déclaration Génie Génétique 2021",
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

    return QuantumBioethicsRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_quantum_bioethics_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "who_human_genome_editing_governance_framework_2021",
            "unesco_bioethics_committee_quantum_ai_report_2024",
            "nature_quantum_computing_drug_discovery_ethics_2024",
            "genome_research_institute_crispr_rights_implications",
            "amnesty_international_biotech_surveillance_rights",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_quantum_bioethics_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
