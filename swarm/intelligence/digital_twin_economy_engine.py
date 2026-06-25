"""
Module 306 — Digital Twin Economy Intelligence Engine
Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DigitalTwinEconomyInput:
    entity_id: str
    twin_category: str
    region: str
    # 17 float fields (0.0-1.0)
    simulation_accuracy: float
    physical_digital_sync_lag: float
    data_sovereignty_risk: float
    model_drift_rate: float
    twin_manipulation_risk: float
    predictive_fidelity: float
    real_time_latency: float
    sensor_coverage_gap: float
    adversarial_input_risk: float
    regulatory_compliance_gap: float
    economic_divergence_index: float
    twin_fragmentation_rate: float
    orchestration_complexity: float
    cybersecurity_exposure: float
    interoperability_deficit: float
    human_oversight_erosion: float
    twin_dependency_lock_in: float


@dataclass
class DigitalTwinEconomyResult:
    entity_id: str
    region: str
    twin_category: str
    twin_risk: str
    twin_pattern: str
    twin_severity: str
    recommended_action: str
    fidelity_score: float
    sync_score: float
    security_score: float
    governance_score: float
    twin_composite: float
    is_twin_crisis: bool
    requires_twin_intervention: bool
    twin_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "twin_category": self.twin_category,
            "twin_risk": self.twin_risk,
            "twin_pattern": self.twin_pattern,
            "twin_severity": self.twin_severity,
            "recommended_action": self.recommended_action,
            "fidelity_score": self.fidelity_score,
            "sync_score": self.sync_score,
            "security_score": self.security_score,
            "governance_score": self.governance_score,
            "twin_composite": self.twin_composite,
            "is_twin_crisis": self.is_twin_crisis,
            "requires_twin_intervention": self.requires_twin_intervention,
            "twin_signal": self.twin_signal,
        }


def _fidelity_score(inp: DigitalTwinEconomyInput) -> float:
    raw = (
        (1 - inp.simulation_accuracy) * 0.4
        + inp.model_drift_rate * 0.35
        + inp.real_time_latency * 0.25
    ) * 100
    return round(raw * 100) / 100


def _sync_score(inp: DigitalTwinEconomyInput) -> float:
    raw = (
        inp.physical_digital_sync_lag * 0.4
        + inp.sensor_coverage_gap * 0.35
        + inp.twin_fragmentation_rate * 0.25
    ) * 100
    return round(raw * 100) / 100


def _security_score(inp: DigitalTwinEconomyInput) -> float:
    raw = (
        inp.cybersecurity_exposure * 0.4
        + inp.adversarial_input_risk * 0.35
        + inp.twin_manipulation_risk * 0.25
    ) * 100
    return round(raw * 100) / 100


def _governance_score(inp: DigitalTwinEconomyInput) -> float:
    raw = (
        inp.data_sovereignty_risk * 0.4
        + inp.regulatory_compliance_gap * 0.35
        + inp.human_oversight_erosion * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(
    fidelity: float,
    sync: float,
    security: float,
    governance: float,
) -> float:
    return round(
        fidelity * 0.30
        + sync * 0.25
        + security * 0.25
        + governance * 0.20,
        2,
    )


def _twin_pattern(inp: DigitalTwinEconomyInput) -> str:
    if inp.physical_digital_sync_lag >= 0.70 and inp.model_drift_rate >= 0.65:
        return "twin_divergence_crisis"
    if inp.data_sovereignty_risk >= 0.70 and inp.regulatory_compliance_gap >= 0.65:
        return "digital_sovereignty_breach"
    if inp.adversarial_input_risk >= 0.70 and inp.cybersecurity_exposure >= 0.65:
        return "adversarial_twin_attack"
    if inp.simulation_accuracy <= 0.30 and inp.twin_fragmentation_rate >= 0.60:
        return "predictive_failure_cascade"
    if inp.twin_dependency_lock_in >= 0.70 and inp.interoperability_deficit >= 0.65:
        return "lock_in_monopoly"
    return "none"


def _twin_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _twin_severity(composite: float) -> str:
    if composite >= 75:
        return "twin_emergency"
    if composite >= 50:
        return "critical_divergence"
    if composite >= 25:
        return "twin_instability"
    return "twin_stable"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "twin_emergency_shutdown"
    if risk == "high" and pattern == "adversarial_twin_attack":
        return "security_lockdown"
    if risk == "high":
        return "twin_recalibration"
    if risk == "moderate":
        return "sync_monitoring"
    return "no_action"


def _twin_signal(inp: DigitalTwinEconomyInput, risk: str, composite: float) -> str:
    if risk == "critical":
        return (
            f"Critique — synchronisation physique-numérique {int(inp.physical_digital_sync_lag * 100)}% "
            f"— dérive modèle {int(inp.model_drift_rate * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "high":
        return (
            f"Élevé — exposition cybersécurité {int(inp.cybersecurity_exposure * 100)}% "
            f"— risque données souveraines {int(inp.data_sovereignty_risk * 100)}% "
            f"— composite {int(composite)}"
        )
    if risk == "moderate":
        return (
            f"Modéré — latence temps réel {int(inp.real_time_latency * 100)}% "
            f"— composite {int(composite)}"
        )
    return "Jumeau numérique stable — fidélité optimale, synchronisation solide, gouvernance maîtrisée"


def analyze(inp: DigitalTwinEconomyInput) -> DigitalTwinEconomyResult:
    fid = _fidelity_score(inp)
    syn = _sync_score(inp)
    sec = _security_score(inp)
    gov = _governance_score(inp)
    comp = _composite(fid, syn, sec, gov)
    pat = _twin_pattern(inp)
    risk = _twin_risk(comp)
    sev = _twin_severity(comp)
    action = _recommended_action(risk, pat)
    sig = _twin_signal(inp, risk, comp)

    return DigitalTwinEconomyResult(
        entity_id=inp.entity_id,
        region=inp.region,
        twin_category=inp.twin_category,
        twin_risk=risk,
        twin_pattern=pat,
        twin_severity=sev,
        recommended_action=action,
        fidelity_score=fid,
        sync_score=syn,
        security_score=sec,
        governance_score=gov,
        twin_composite=comp,
        is_twin_crisis=comp >= 60,
        requires_twin_intervention=comp >= 40,
        twin_signal=sig,
    )


class DigitalTwinEconomyEngine:
    def __init__(self, inputs: List[DigitalTwinEconomyInput]):
        self.inputs = inputs
        self.results: List[DigitalTwinEconomyResult] = [analyze(i) for i in inputs]

    def analyze(self, entities: List[DigitalTwinEconomyInput]) -> Dict[str, Any]:
        results = [analyze(e) for e in entities]
        n = len(results)
        if n == 0:
            return {}

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_composite = 0.0
        total_fidelity = 0.0
        total_sync = 0.0
        total_security = 0.0
        total_governance = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.twin_risk] = risk_counts.get(r.twin_risk, 0) + 1
            pattern_counts[r.twin_pattern] = pattern_counts.get(r.twin_pattern, 0) + 1
            severity_counts[r.twin_severity] = severity_counts.get(r.twin_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1

            total_composite += r.twin_composite
            total_fidelity += r.fidelity_score
            total_sync += r.sync_score
            total_security += r.security_score
            total_governance += r.governance_score

            if r.is_twin_crisis:
                crisis_count += 1
            if r.requires_twin_intervention:
                intervention_count += 1

        avg_composite = round(total_composite / n * 10) / 10

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_twin_composite": avg_composite,
            "twin_crisis_count": crisis_count,
            "twin_intervention_count": intervention_count,
            "avg_fidelity_score": round(total_fidelity / n * 10) / 10,
            "avg_sync_score": round(total_sync / n * 10) / 10,
            "avg_security_score": round(total_security / n * 10) / 10,
            "avg_governance_score": round(total_governance / n * 10) / 10,
            "avg_estimated_twin_risk_index": round(avg_composite / 100 * 10, 2),
        }
