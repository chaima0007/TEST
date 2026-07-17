"""
Module 281 — Bio-Digital Convergence & Synthetic Life Engine
Caelum Partners Swarm Intelligence
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class BioDigitalInput:
    entity_id: str
    convergence_domain: str
    region: str
    # 17 float fields (0.0–1.0)
    bio_integration_rate: float
    digital_twin_fidelity: float
    synthetic_viability: float
    biocompute_efficiency: float
    dna_data_density: float
    neural_coupling_depth: float
    bio_signal_clarity: float
    organic_error_rate: float
    cellular_adaptation: float
    protein_fold_accuracy: float
    evolutionary_drift: float
    regulatory_compliance_bio: float
    containment_integrity: float
    cross_domain_coherence: float
    emergence_risk: float
    biological_instability: float
    interface_degradation: float


@dataclass
class BioDigitalResult:
    entity_id: str
    region: str
    convergence_domain: str
    convergence_risk: str
    convergence_pattern: str
    convergence_severity: str
    recommended_action: str
    integration_score: float
    synthetic_score: float
    biocompute_score: float
    coherence_score: float
    convergence_composite: float
    is_in_convergence_crisis: bool
    requires_bio_intervention: bool
    convergence_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "convergence_domain": self.convergence_domain,
            "convergence_risk": self.convergence_risk,
            "convergence_pattern": self.convergence_pattern,
            "convergence_severity": self.convergence_severity,
            "recommended_action": self.recommended_action,
            "integration_score": self.integration_score,
            "synthetic_score": self.synthetic_score,
            "biocompute_score": self.biocompute_score,
            "coherence_score": self.coherence_score,
            "convergence_composite": self.convergence_composite,
            "is_in_convergence_crisis": self.is_in_convergence_crisis,
            "requires_bio_intervention": self.requires_bio_intervention,
            "convergence_signal": self.convergence_signal,
        }


def _integration_score(inp: BioDigitalInput) -> float:
    raw = (
        inp.biological_instability * 0.4
        + inp.interface_degradation * 0.3
        + (1 - inp.bio_integration_rate) * 0.3
    ) * 100
    return round(raw * 100) / 100


def _synthetic_score(inp: BioDigitalInput) -> float:
    raw = (
        (1 - inp.synthetic_viability) * 0.4
        + inp.organic_error_rate * 0.35
        + inp.evolutionary_drift * 0.25
    ) * 100
    return round(raw * 100) / 100


def _biocompute_score(inp: BioDigitalInput) -> float:
    raw = (
        (1 - inp.biocompute_efficiency) * 0.4
        + (1 - inp.protein_fold_accuracy) * 0.3
        + (1 - inp.dna_data_density) * 0.3
    ) * 100
    return round(raw * 100) / 100


def _coherence_score(inp: BioDigitalInput) -> float:
    raw = (
        (1 - inp.cross_domain_coherence) * 0.4
        + inp.emergence_risk * 0.35
        + (1 - inp.containment_integrity) * 0.25
    ) * 100
    return round(raw * 100) / 100


def _composite(integration: float, synthetic: float, biocompute: float, coherence: float) -> float:
    return round(
        (integration * 0.30 + synthetic * 0.25 + biocompute * 0.25 + coherence * 0.20) * 100
    ) / 100


def _convergence_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _convergence_pattern(inp: BioDigitalInput) -> str:
    if inp.biological_instability >= 0.65 and (1 - inp.bio_integration_rate) >= 0.55:
        return "bio_digital_desync"
    if (1 - inp.synthetic_viability) >= 0.65 and inp.organic_error_rate >= 0.55:
        return "synthetic_collapse"
    if (1 - inp.biocompute_efficiency) >= 0.65 and (1 - inp.protein_fold_accuracy) >= 0.55:
        return "biocompute_failure"
    if inp.emergence_risk >= 0.65 and (1 - inp.containment_integrity) >= 0.50:
        return "emergence_cascade"
    if inp.evolutionary_drift >= 0.65 and (1 - inp.cellular_adaptation) >= 0.55:
        return "evolutionary_drift"
    return "none"


def _convergence_severity(composite: float) -> str:
    if composite >= 75:
        return "critical_divergence"
    if composite >= 50:
        return "high_instability"
    if composite >= 25:
        return "developing_risk"
    return "stable_convergence"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "bio_digital_emergency"
    if risk == "high":
        if pattern == "emergence_cascade":
            return "containment_protocol"
        return "convergence_stabilization"
    if risk == "moderate":
        return "bio_monitoring"
    return "no_action"


def _convergence_signal(inp: BioDigitalInput, risk: str, composite: float) -> str:
    comp_int = int(composite)
    if risk == "critical":
        bio_pct = int(inp.bio_integration_rate * 100)
        synth_pct = int(inp.synthetic_viability * 100)
        return (
            f"Critique — intégration bio-digitale {bio_pct}% — "
            f"viabilité synthétique {synth_pct}% — composite {comp_int}"
        )
    if risk == "high":
        drift_pct = int(inp.evolutionary_drift * 100)
        coh_pct = int(inp.cross_domain_coherence * 100)
        return (
            f"Élevé — dérive évolutive {drift_pct}% — "
            f"cohérence domaines {coh_pct}% — composite {comp_int}"
        )
    if risk == "moderate":
        bio_eff_pct = int(inp.biocompute_efficiency * 100)
        return f"Modéré — efficacité biocompute {bio_eff_pct}% — composite {comp_int}"
    return "Convergence bio-digitale optimale — systèmes synthétiques stables, biocomputing performant"


def assess(inp: BioDigitalInput) -> BioDigitalResult:
    integration = _integration_score(inp)
    synthetic = _synthetic_score(inp)
    biocompute = _biocompute_score(inp)
    coherence = _coherence_score(inp)
    composite = _composite(integration, synthetic, biocompute, coherence)
    risk = _convergence_risk(composite)
    pattern = _convergence_pattern(inp)
    severity = _convergence_severity(composite)
    action = _recommended_action(risk, pattern)
    signal = _convergence_signal(inp, risk, composite)

    return BioDigitalResult(
        entity_id=inp.entity_id,
        region=inp.region,
        convergence_domain=inp.convergence_domain,
        convergence_risk=risk,
        convergence_pattern=pattern,
        convergence_severity=severity,
        recommended_action=action,
        integration_score=integration,
        synthetic_score=synthetic,
        biocompute_score=biocompute,
        coherence_score=coherence,
        convergence_composite=composite,
        is_in_convergence_crisis=composite >= 60,
        requires_bio_intervention=composite >= 40,
        convergence_signal=signal,
    )


class BioDigitalConvergenceEngine:

    def assess_batch(self, inputs: List[BioDigitalInput]) -> List[BioDigitalResult]:
        return [assess(inp) for inp in inputs]

    def summary(self, results: List[BioDigitalResult]) -> Dict[str, Any]:
        n = len(results)
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        total_integration = 0.0
        total_synthetic = 0.0
        total_biocompute = 0.0
        total_coherence = 0.0
        total_composite = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.convergence_risk] = risk_counts.get(r.convergence_risk, 0) + 1
            pattern_counts[r.convergence_pattern] = pattern_counts.get(r.convergence_pattern, 0) + 1
            severity_counts[r.convergence_severity] = severity_counts.get(r.convergence_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_integration += r.integration_score
            total_synthetic += r.synthetic_score
            total_biocompute += r.biocompute_score
            total_coherence += r.coherence_score
            total_composite += r.convergence_composite
            if r.is_in_convergence_crisis:
                crisis_count += 1
            if r.requires_bio_intervention:
                intervention_count += 1

        avg_composite = total_composite / n if n else 0.0

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_convergence_composite": round(avg_composite * 10) / 10,
            "convergence_crisis_count": crisis_count,
            "bio_intervention_required_count": intervention_count,
            "avg_integration_score": round(total_integration / n * 10) / 10 if n else 0.0,
            "avg_synthetic_score": round(total_synthetic / n * 10) / 10 if n else 0.0,
            "avg_biocompute_score": round(total_biocompute / n * 10) / 10 if n else 0.0,
            "avg_coherence_score": round(total_coherence / n * 10) / 10 if n else 0.0,
            "avg_estimated_bio_digital_index": round(avg_composite / 100 * 10 * 100) / 100,
        }
