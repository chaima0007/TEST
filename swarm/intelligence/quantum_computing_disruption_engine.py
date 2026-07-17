"""
Module 307 — Quantum Computing Disruption Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class QuantumDisruptionInput:
    entity_id: str
    sector: str
    region: str
    # 17 float fields (0.0–1.0)
    cryptographic_vulnerability: float
    quantum_readiness_gap: float
    post_quantum_adoption_rate: float          # inverse: high = good
    qubit_error_rate: float
    decoherence_susceptibility: float
    quantum_supremacy_exposure: float
    harvest_now_decrypt_later_risk: float
    quantum_key_distribution_adoption: float  # inverse: high = good
    nist_pqc_compliance_gap: float
    supply_chain_quantum_risk: float
    financial_system_exposure: float
    critical_infrastructure_vulnerability: float
    quantum_arms_race_intensity: float
    talent_shortage_index: float
    standardization_lag: float
    adversarial_quantum_capability: float
    quantum_economic_disruption_index: float


@dataclass
class QuantumDisruptionResult:
    entity_id: str
    region: str
    sector: str
    quantum_risk: str
    quantum_pattern: str
    quantum_severity: str
    recommended_action: str
    cryptographic_score: float
    readiness_score: float
    infrastructure_score: float
    geopolitical_score: float
    quantum_composite: float
    is_quantum_crisis: bool
    requires_quantum_intervention: bool
    quantum_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "sector": self.sector,
            "quantum_risk": self.quantum_risk,
            "quantum_pattern": self.quantum_pattern,
            "quantum_severity": self.quantum_severity,
            "recommended_action": self.recommended_action,
            "cryptographic_score": self.cryptographic_score,
            "readiness_score": self.readiness_score,
            "infrastructure_score": self.infrastructure_score,
            "geopolitical_score": self.geopolitical_score,
            "quantum_composite": self.quantum_composite,
            "is_quantum_crisis": self.is_quantum_crisis,
            "requires_quantum_intervention": self.requires_quantum_intervention,
            "quantum_signal": self.quantum_signal,
        }


def _cryptographic_score(e: QuantumDisruptionInput) -> float:
    raw = (
        e.cryptographic_vulnerability * 0.4
        + e.harvest_now_decrypt_later_risk * 0.35
        + e.nist_pqc_compliance_gap * 0.25
    ) * 100
    return round(raw * 100) / 100


def _readiness_score(e: QuantumDisruptionInput) -> float:
    raw = (
        e.quantum_readiness_gap * 0.4
        + (1 - e.post_quantum_adoption_rate) * 0.35
        + e.standardization_lag * 0.25
    ) * 100
    return round(raw * 100) / 100


def _infrastructure_score(e: QuantumDisruptionInput) -> float:
    raw = (
        e.critical_infrastructure_vulnerability * 0.4
        + e.financial_system_exposure * 0.35
        + e.supply_chain_quantum_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _geopolitical_score(e: QuantumDisruptionInput) -> float:
    raw = (
        e.adversarial_quantum_capability * 0.4
        + e.quantum_arms_race_intensity * 0.35
        + e.talent_shortage_index * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    crypto: float,
    readiness: float,
    infra: float,
    geo: float,
) -> float:
    return round(
        crypto * 0.30
        + readiness * 0.25
        + infra * 0.25
        + geo * 0.20,
        2,
    )


def _quantum_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _quantum_pattern(e: QuantumDisruptionInput) -> str:
    if e.cryptographic_vulnerability >= 0.70 and e.harvest_now_decrypt_later_risk >= 0.65:
        return "cryptographic_apocalypse"
    if e.adversarial_quantum_capability >= 0.70 and e.cryptographic_vulnerability >= 0.60:
        return "quantum_surprise_attack"
    if e.critical_infrastructure_vulnerability >= 0.70 and e.quantum_readiness_gap >= 0.65:
        return "infrastructure_quantum_shock"
    if e.financial_system_exposure >= 0.70 and e.nist_pqc_compliance_gap >= 0.65:
        return "financial_system_collapse"
    if e.talent_shortage_index >= 0.70 and e.quantum_readiness_gap >= 0.65:
        return "talent_capability_gap"
    return "none"


def _quantum_severity(composite: float) -> str:
    if composite >= 75:
        return "quantum_emergency"
    if composite >= 50:
        return "high_quantum_risk"
    if composite >= 25:
        return "quantum_preparing"
    return "quantum_secure"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "quantum_emergency_migration"
    if risk == "high" and pattern == "cryptographic_apocalypse":
        return "immediate_pqc_deployment"
    if risk == "high":
        return "quantum_transition_plan"
    if risk == "moderate":
        return "quantum_monitoring"
    return "no_action"


def _quantum_signal(e: QuantumDisruptionInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        return (
            f"Critique — vulnérabilité cryptographique {int(e.cryptographic_vulnerability * 100)}% "
            f"— risque HNDL {int(e.harvest_now_decrypt_later_risk * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — capacité adversaire quantique {int(e.adversarial_quantum_capability * 100)}% "
            f"— écart préparation {int(e.quantum_readiness_gap * 100)}% "
            f"— composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — retard standardisation {int(e.standardization_lag * 100)}% "
            f"— composite {comp_int}"
        )
    return "Infrastructure quantique sécurisée — conformité PQC NIST assurée, résilience cryptographique préservée"


def _analyze(e: QuantumDisruptionInput) -> QuantumDisruptionResult:
    crypto = _cryptographic_score(e)
    readiness = _readiness_score(e)
    infra = _infrastructure_score(e)
    geo = _geopolitical_score(e)
    comp = _composite(crypto, readiness, infra, geo)
    risk = _quantum_risk(comp)
    pattern = _quantum_pattern(e)
    severity = _quantum_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _quantum_signal(e, risk, comp)

    return QuantumDisruptionResult(
        entity_id=e.entity_id,
        region=e.region,
        sector=e.sector,
        quantum_risk=risk,
        quantum_pattern=pattern,
        quantum_severity=severity,
        recommended_action=action,
        cryptographic_score=crypto,
        readiness_score=readiness,
        infrastructure_score=infra,
        geopolitical_score=geo,
        quantum_composite=comp,
        is_quantum_crisis=comp >= 60,
        requires_quantum_intervention=comp >= 40,
        quantum_signal=signal,
    )


class QuantumComputingDisruptionEngine:
    def analyze(self, entities: List[QuantumDisruptionInput]) -> Dict[str, Any]:
        results = [_analyze(e) for e in entities]
        entity_dicts = [r.to_dict() for r in results]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_crypto = 0.0
        total_readiness = 0.0
        total_infra = 0.0
        total_geo = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.quantum_risk] = risk_counts.get(r.quantum_risk, 0) + 1
            pattern_counts[r.quantum_pattern] = pattern_counts.get(r.quantum_pattern, 0) + 1
            severity_counts[r.quantum_severity] = severity_counts.get(r.quantum_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_composite += r.quantum_composite
            total_crypto += r.cryptographic_score
            total_readiness += r.readiness_score
            total_infra += r.infrastructure_score
            total_geo += r.geopolitical_score
            if r.is_quantum_crisis:
                crisis_count += 1
            if r.requires_quantum_intervention:
                intervention_count += 1

        n = len(results)
        avg_composite = round(total_composite / n * 10) / 10 if n else 0.0

        summary = {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_quantum_composite": avg_composite,
            "quantum_crisis_count": crisis_count,
            "quantum_intervention_count": intervention_count,
            "avg_cryptographic_score": round(total_crypto / n * 10) / 10 if n else 0.0,
            "avg_readiness_score": round(total_readiness / n * 10) / 10 if n else 0.0,
            "avg_infrastructure_score": round(total_infra / n * 10) / 10 if n else 0.0,
            "avg_geopolitical_score": round(total_geo / n * 10) / 10 if n else 0.0,
            "avg_estimated_quantum_disruption_index": round(avg_composite / 100 * 10, 2),
        }

        return {"entities": entity_dicts, "summary": summary}
