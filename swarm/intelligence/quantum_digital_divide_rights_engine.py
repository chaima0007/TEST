from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import statistics

ACCENT_COLOR = "#f59e0b"


@dataclass
class QuantumDigitalDivideRightsEntity:
    entity_id: str
    name: str
    country: str
    quantum_access_inequality_score: float
    technology_sovereignty_gap_score: float
    quantum_workforce_exclusion_score: float
    economic_quantum_disruption_score: float
    composite_score: float = field(init=False)
    risk_level: str = field(init=False)
    primary_pattern: str = ""
    estimated_quantum_digital_divide_rights_index: float = field(init=False)
    last_updated: str = "2026-06-22"

    def __post_init__(self):
        self.composite_score = round(
            self.quantum_access_inequality_score * 0.30
            + self.technology_sovereignty_gap_score * 0.25
            + self.quantum_workforce_exclusion_score * 0.25
            + self.economic_quantum_disruption_score * 0.20,
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
        self.estimated_quantum_digital_divide_rights_index = round(
            self.composite_score / 100 * 10, 2
        )


@dataclass
class QuantumDigitalDivideRightsEngineResult:
    agent: str = "Quantum Digital Divide Rights Engine Agent"
    domain: str = "quantum_digital_divide_rights"
    total_entities: int = 0
    avg_composite: float = 0.0
    confidence_score: float = 0.85
    risk_distribution: dict = field(default_factory=dict)
    pattern_distribution: dict = field(default_factory=dict)
    top_risk_entities: List[str] = field(default_factory=list)
    critical_alerts: List[str] = field(default_factory=list)
    last_analysis: str = "2026-06-22"
    engine_version: str = "1.0.0"
    avg_estimated_quantum_digital_divide_rights_index: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    entities: List[QuantumDigitalDivideRightsEntity] = field(default_factory=list)


def run_quantum_digital_divide_rights_engine() -> QuantumDigitalDivideRightsEngineResult:
    entities = [
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-001",
            name="Afrique Sub-Saharienne — Zéro infrastructure quantum 54 pays dépendants",
            country="Afrique Sub-Saharienne",
            quantum_access_inequality_score=96,
            technology_sovereignty_gap_score=95,
            quantum_workforce_exclusion_score=94,
            economic_quantum_disruption_score=97,
            primary_pattern="Zéro infrastructure quantum / dépendance totale fournisseurs US/CN",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-002",
            name="Bangladesh/Pakistan — Économies vulnérables disruption quantum",
            country="Bangladesh/Pakistan",
            quantum_access_inequality_score=89,
            technology_sovereignty_gap_score=88,
            quantum_workforce_exclusion_score=90,
            economic_quantum_disruption_score=91,
            primary_pattern="Chiffrement bancaire dépassé / vulnérabilité disruption quantum",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-003",
            name="Brésil/Amérique Latine — Quantum gap vs USA/UE formation insuffisante",
            country="Brésil/Amérique Latine",
            quantum_access_inequality_score=83,
            technology_sovereignty_gap_score=82,
            quantum_workforce_exclusion_score=84,
            economic_quantum_disruption_score=85,
            primary_pattern="Quantum gap régional / Petrobras vulnérable PQC",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-004",
            name="Inde — Quantum Mission ₹6000Cr insuffisant 1.4Md sans protection PQC",
            country="Inde",
            quantum_access_inequality_score=77,
            technology_sovereignty_gap_score=76,
            quantum_workforce_exclusion_score=78,
            economic_quantum_disruption_score=79,
            primary_pattern="Quantum Mission insuffisant / 1.4Md personnes sans protection PQC banques",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-005",
            name="Union Européenne — EuroQCI en développement retard vs USA/Chine",
            country="UE",
            quantum_access_inequality_score=55,
            technology_sovereignty_gap_score=54,
            quantum_workforce_exclusion_score=56,
            economic_quantum_disruption_score=57,
            primary_pattern="EuroQCI retard / gap 50k ingénieurs quantiques",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-006",
            name="Russie — Sanctions limitant accès matériel quantique dépendance Chine",
            country="Russie",
            quantum_access_inequality_score=46,
            technology_sovereignty_gap_score=45,
            quantum_workforce_exclusion_score=47,
            economic_quantum_disruption_score=48,
            primary_pattern="Sanctions matériel quantique / dépendance Chine croissante",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-007",
            name="Canada/Australie — Programmes quantum nationaux Five Eyes accès",
            country="Canada/Australie",
            quantum_access_inequality_score=30,
            technology_sovereignty_gap_score=29,
            quantum_workforce_exclusion_score=31,
            economic_quantum_disruption_score=32,
            primary_pattern="Five Eyes quantum sharing / programmes nationaux investissements",
        ),
        QuantumDigitalDivideRightsEntity(
            entity_id="QDD-008",
            name="USA/IBM/Google — Quantum supremacy Stargate standards exportation PQC",
            country="USA",
            quantum_access_inequality_score=12,
            technology_sovereignty_gap_score=11,
            quantum_workforce_exclusion_score=13,
            economic_quantum_disruption_score=14,
            primary_pattern="Quantum supremacy / standards exportation PQC globaux",
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

    return QuantumDigitalDivideRightsEngineResult(
        total_entities=len(entities),
        avg_composite=avg_composite,
        risk_distribution=risk_dist,
        pattern_distribution=pattern_dist,
        top_risk_entities=top_risk,
        critical_alerts=alerts,
        avg_estimated_quantum_digital_divide_rights_index=round(
            avg_composite / 100 * 10, 2
        ),
        data_sources=[
            "mckinsey_quantum_technology_global_state_2024",
            "world_economic_forum_quantum_equity_access_2024",
            "itu_quantum_digital_divide_developing_countries",
            "quantum_economic_development_consortium_workforce",
            "un_unctad_quantum_technology_developing_nations_2024",
        ],
        entities=entities,
    )


if __name__ == "__main__":
    result = run_quantum_digital_divide_rights_engine()
    print(f"Agent: {result.agent}")
    print(f"Avg composite: {result.avg_composite}")
    print(f"Risk distribution: {result.risk_distribution}")
    for e in result.entities:
        print(f"  {e.entity_id}: {e.composite_score} [{e.risk_level}]")
