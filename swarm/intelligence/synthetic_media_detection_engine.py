"""
Module 294 — Synthetic Media & Deepfake Detection Intelligence Engine
Caelum Partners Swarm Intelligence — Detecting and assessing risk from synthetic media:
deepfakes, AI-generated content, voice cloning, identity fraud.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SyntheticMediaInput:
    entity_id: str
    media_domain: str
    region: str
    deepfake_prevalence: float
    ai_content_saturation: float
    detection_capability: float
    authentication_gap: float
    voice_clone_exposure: float
    face_swap_sophistication: float
    provenance_verification_rate: float
    synthetic_identity_fraud_rate: float
    content_authenticity_infrastructure: float
    adversarial_evolution_speed: float
    forensic_detection_lag: float
    platform_content_moderation: float
    public_trust_erosion: float
    legal_framework_readiness: float
    biometric_spoofing_risk: float
    media_literacy_level: float
    watermarking_adoption: float


@dataclass
class SyntheticMediaResult:
    entity_id: str
    region: str
    media_domain: str
    synthetic_risk: str
    synthetic_pattern: str
    synthetic_severity: str
    recommended_action: str
    detection_score: float
    authenticity_score: float
    trust_score: float
    governance_score: float
    synthetic_composite: float
    is_in_synthetic_crisis: bool
    requires_synthetic_intervention: bool
    synthetic_signal: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "region": self.region,
            "media_domain": self.media_domain,
            "synthetic_risk": self.synthetic_risk,
            "synthetic_pattern": self.synthetic_pattern,
            "synthetic_severity": self.synthetic_severity,
            "recommended_action": self.recommended_action,
            "detection_score": self.detection_score,
            "authenticity_score": self.authenticity_score,
            "trust_score": self.trust_score,
            "governance_score": self.governance_score,
            "synthetic_composite": self.synthetic_composite,
            "is_in_synthetic_crisis": self.is_in_synthetic_crisis,
            "requires_synthetic_intervention": self.requires_synthetic_intervention,
            "synthetic_signal": self.synthetic_signal,
        }


def _detection_score(inp: SyntheticMediaInput) -> float:
    return round(
        ((1 - inp.detection_capability) * 0.4
         + inp.forensic_detection_lag * 0.35
         + inp.adversarial_evolution_speed * 0.25) * 100,
        2,
    )


def _authenticity_score(inp: SyntheticMediaInput) -> float:
    return round(
        (inp.deepfake_prevalence * 0.4
         + inp.authentication_gap * 0.35
         + (1 - inp.provenance_verification_rate) * 0.25) * 100,
        2,
    )


def _trust_score(inp: SyntheticMediaInput) -> float:
    return round(
        (inp.public_trust_erosion * 0.4
         + inp.synthetic_identity_fraud_rate * 0.35
         + (1 - inp.media_literacy_level) * 0.25) * 100,
        2,
    )


def _governance_score(inp: SyntheticMediaInput) -> float:
    return round(
        ((1 - inp.platform_content_moderation) * 0.4
         + (1 - inp.legal_framework_readiness) * 0.35
         + (1 - inp.watermarking_adoption) * 0.25) * 100,
        2,
    )


def _composite(det: float, auth: float, trust: float, gov: float) -> float:
    return round(det * 0.30 + auth * 0.25 + trust * 0.25 + gov * 0.20, 2)


def _synthetic_risk(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _synthetic_pattern(inp: SyntheticMediaInput) -> str:
    if inp.deepfake_prevalence >= 0.65 and (1 - inp.detection_capability) >= 0.55:
        return "deepfake_epidemic"
    if inp.synthetic_identity_fraud_rate >= 0.65 and inp.authentication_gap >= 0.55:
        return "identity_fraud_cascade"
    if inp.public_trust_erosion >= 0.70 and (1 - inp.media_literacy_level) >= 0.60:
        return "trust_collapse"
    if (1 - inp.legal_framework_readiness) >= 0.70 and (1 - inp.platform_content_moderation) >= 0.60:
        return "governance_vacuum"
    if inp.adversarial_evolution_speed >= 0.70 and inp.forensic_detection_lag >= 0.60:
        return "adversarial_arms_race"
    return "none"


def _synthetic_severity(composite: float) -> str:
    if composite >= 75:
        return "synthetic_reality_crisis"
    if composite >= 50:
        return "high_synthetic_threat"
    if composite >= 25:
        return "developing_threat"
    return "authentic_environment"


def _recommended_action(risk: str, pattern: str) -> str:
    if risk == "critical":
        return "synthetic_media_emergency"
    if risk == "high" and pattern == "trust_collapse":
        return "trust_restoration_protocol"
    if risk == "high":
        return "detection_infrastructure"
    if risk == "moderate":
        return "synthetic_monitoring"
    return "no_action"


def _synthetic_signal(
    inp: SyntheticMediaInput,
    risk: str,
    composite: float,
) -> str:
    dp_pct = int(inp.deepfake_prevalence * 100)
    pt_pct = int(inp.public_trust_erosion * 100)
    sif_pct = int(inp.synthetic_identity_fraud_rate * 100)
    dc_pct = int(inp.detection_capability * 100)
    acs_pct = int(inp.ai_content_saturation * 100)
    comp_int = int(composite)

    if risk == "critical":
        return (
            f"Critique — prévalence deepfakes {dp_pct}% — "
            f"érosion confiance {pt_pct}% — composite {comp_int}"
        )
    if risk == "high":
        return (
            f"Élevé — fraude identité synthétique {sif_pct}% — "
            f"capacité détection {dc_pct}% — composite {comp_int}"
        )
    if risk == "moderate":
        return (
            f"Modéré — saturation contenu IA {acs_pct}% — composite {comp_int}"
        )
    return "Environnement média authentique — détection robuste, confiance publique maintenue"


def analyse(inp: SyntheticMediaInput) -> SyntheticMediaResult:
    det = _detection_score(inp)
    auth = _authenticity_score(inp)
    trust = _trust_score(inp)
    gov = _governance_score(inp)
    comp = _composite(det, auth, trust, gov)

    risk = _synthetic_risk(comp)
    pattern = _synthetic_pattern(inp)
    severity = _synthetic_severity(comp)
    action = _recommended_action(risk, pattern)
    signal = _synthetic_signal(inp, risk, comp)

    return SyntheticMediaResult(
        entity_id=inp.entity_id,
        region=inp.region,
        media_domain=inp.media_domain,
        synthetic_risk=risk,
        synthetic_pattern=pattern,
        synthetic_severity=severity,
        recommended_action=action,
        detection_score=det,
        authenticity_score=auth,
        trust_score=trust,
        governance_score=gov,
        synthetic_composite=comp,
        is_in_synthetic_crisis=comp >= 60,
        requires_synthetic_intervention=comp >= 40,
        synthetic_signal=signal,
    )


class SyntheticMediaDetectionEngine:
    """
    Aggregate multiple SyntheticMediaInput entities and produce a summary
    with 13 keys as required by Module 294 spec.
    """

    def run(self, inputs: List[SyntheticMediaInput]) -> Dict[str, Any]:
        results = [analyse(inp) for inp in inputs]

        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}

        total_det = 0.0
        total_auth = 0.0
        total_trust = 0.0
        total_gov = 0.0
        total_comp = 0.0
        crisis_count = 0
        intervention_count = 0

        for r in results:
            risk_counts[r.synthetic_risk] = risk_counts.get(r.synthetic_risk, 0) + 1
            pattern_counts[r.synthetic_pattern] = pattern_counts.get(r.synthetic_pattern, 0) + 1
            severity_counts[r.synthetic_severity] = severity_counts.get(r.synthetic_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            total_det += r.detection_score
            total_auth += r.authenticity_score
            total_trust += r.trust_score
            total_gov += r.governance_score
            total_comp += r.synthetic_composite
            if r.is_in_synthetic_crisis:
                crisis_count += 1
            if r.requires_synthetic_intervention:
                intervention_count += 1

        n = len(results)
        avg_comp = total_comp / n if n else 0.0

        return {
            "total": n,
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_synthetic_composite": round(avg_comp * 10) / 10,
            "synthetic_crisis_count": crisis_count,
            "synthetic_intervention_count": intervention_count,
            "avg_detection_score": round(total_det / n * 10) / 10 if n else 0.0,
            "avg_authenticity_score": round(total_auth / n * 10) / 10 if n else 0.0,
            "avg_trust_score": round(total_trust / n * 10) / 10 if n else 0.0,
            "avg_governance_score": round(total_gov / n * 10) / 10 if n else 0.0,
            "avg_estimated_synthetic_threat_index": round(avg_comp / 100 * 10, 2),
        }
