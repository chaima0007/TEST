"""
Module 274 — Augmented Reality Engineering & Neural Interface Engine
Caelum Partners Swarm Intelligence Platform
Monitors AR/XR deployment quality, neural interface latency,
brain-computer integration safety, and immersive experience engineering.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ARNeuralInput:
    interface_id: str
    interface_type: str  # retinal_projection | holographic_overlay | haptic_neural |
                         # brain_computer_interface | spatial_computing | mixed_reality_mesh |
                         # neural_feedback_loop | embodied_ai_avatar
    region: str

    # Risk fields (higher = worse)
    neural_latency_risk: float              # ms delay in neural signal processing
    biometric_privacy_exposure: float      # higher = more exposure risk
    motion_sickness_risk: float            # higher = more sickness risk
    neural_fatigue_accumulation: float     # higher = more fatigue
    data_sovereignty_of_neural_data: float # higher = MORE risk
    immersive_addiction_risk: float        # higher = more addiction risk

    # Performance / quality fields (higher = better, will be inverted where needed)
    spatial_accuracy_score: float
    cognitive_immersion_depth: float
    neural_signal_integrity: float
    sensory_coherence_score: float
    eye_tracking_precision: float
    haptic_fidelity_score: float
    reality_anchoring_stability: float
    bci_safety_compliance: float
    cross_platform_interoperability: float
    environmental_mapping_accuracy: float
    neural_adaptation_speed: float


class ARNeuralInterfaceEngine:
    """
    Assesses AR/XR neural interface deployments for risk, immersion quality,
    biometric safety, and signal integrity.
    """

    def _neural_risk_score(self, inp: ARNeuralInput) -> float:
        """0.30 weight — latency risk, fatigue, BCI safety (inverted)."""
        return (
            inp.neural_latency_risk * 0.333
            + inp.neural_fatigue_accumulation * 0.333
            + (1.0 - inp.bci_safety_compliance) * 0.334
        )

    def _immersion_score(self, inp: ARNeuralInput) -> float:
        """0.25 weight — immersion depth (inv), coherence (inv), anchoring (inv)."""
        return (
            (1.0 - inp.cognitive_immersion_depth) * 0.333
            + (1.0 - inp.sensory_coherence_score) * 0.333
            + (1.0 - inp.reality_anchoring_stability) * 0.334
        )

    def _safety_score(self, inp: ARNeuralInput) -> float:
        """0.25 weight — biometric exposure, motion sickness, addiction risk."""
        return (
            inp.biometric_privacy_exposure * 0.333
            + inp.motion_sickness_risk * 0.333
            + inp.immersive_addiction_risk * 0.334
        )

    def _integrity_score(self, inp: ARNeuralInput) -> float:
        """0.20 weight — signal integrity (inv), data sovereignty, spatial accuracy (inv)."""
        return (
            (1.0 - inp.neural_signal_integrity) * 0.333
            + inp.data_sovereignty_of_neural_data * 0.333
            + (1.0 - inp.spatial_accuracy_score) * 0.334
        )

    def _composite(self, nr: float, im: float, sa: float, ig: float) -> float:
        return round(
            nr * 0.30 + im * 0.25 + sa * 0.25 + ig * 0.20,
            4,
        )

    def _neural_pattern(self, inp: ARNeuralInput) -> str:
        if inp.neural_latency_risk >= 0.75 and inp.neural_fatigue_accumulation >= 0.70:
            return "neural_overload"
        if inp.reality_anchoring_stability <= 0.25 or inp.sensory_coherence_score <= 0.25:
            return "reality_dissociation"
        if inp.biometric_privacy_exposure >= 0.75 or inp.data_sovereignty_of_neural_data >= 0.75:
            return "biometric_breach"
        if inp.bci_safety_compliance <= 0.25 or inp.neural_signal_integrity <= 0.25:
            return "bci_failure"
        if inp.sensory_coherence_score <= 0.35 and inp.haptic_fidelity_score <= 0.35:
            return "sensory_collapse"
        return "none"

    def _risk_level(self, comp: float) -> str:
        if comp >= 0.60:
            return "critical"
        if comp >= 0.40:
            return "high"
        if comp >= 0.20:
            return "moderate"
        return "low"

    def _severity(self, comp: float) -> str:
        if comp >= 0.60:
            return "critical_neural"
        if comp >= 0.40:
            return "unstable"
        if comp >= 0.20:
            return "calibrating"
        return "immersive"

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            if pattern in ("neural_overload", "bci_failure"):
                return "neural_emergency_disconnect"
            return "bci_safety_lockdown"
        if risk == "high":
            if pattern in ("reality_dissociation", "sensory_collapse"):
                return "immersion_recalibration"
            return "privacy_shield"
        if risk == "moderate":
            return "neural_monitoring"
        return "no_action"

    def _signal(self, inp: ARNeuralInput, pattern: str, comp: float) -> str:
        latency_ms = round(inp.neural_latency_risk * 500, 1)
        immersion_pct = round(inp.cognitive_immersion_depth * 100, 1)
        integrity_pct = round(inp.neural_signal_integrity * 100, 1)

        if comp < 0.20:
            return (
                f"Interface neuronale stable — latence {latency_ms}ms"
                f" — immersion {immersion_pct}%"
                f" — intégrité signal {integrity_pct}%"
            )

        labels: Dict[str, str] = {
            "neural_overload":     "Surcharge neuronale",
            "reality_dissociation":"Dissociation réalité",
            "biometric_breach":    "Violation biométrique",
            "bci_failure":         "Défaillance BCI",
            "sensory_collapse":    "Effondrement sensoriel",
            "none":                "Aucun pattern critique",
        }
        label = labels.get(pattern, pattern.replace("_", " "))
        return (
            f"{label} — latence {latency_ms}ms"
            f" — immersion {immersion_pct}%"
            f" — intégrité signal {integrity_pct}%"
            f" — risque composite {round(comp * 100, 1)}%"
        )

    def _assess_one(self, inp: ARNeuralInput) -> Dict[str, Any]:
        nr = self._neural_risk_score(inp)
        im = self._immersion_score(inp)
        sa = self._safety_score(inp)
        ig = self._integrity_score(inp)
        comp = self._composite(nr, im, sa, ig)
        pattern = self._neural_pattern(inp)
        risk = self._risk_level(comp)
        sev = self._severity(comp)
        act = self._action(risk, pattern)
        sig = self._signal(inp, pattern, comp)

        return {
            "interface_id": inp.interface_id,
            "interface_type": inp.interface_type,
            "region": inp.region,
            "neural_risk_score": round(nr * 100, 2),
            "immersion_score": round(im * 100, 2),
            "safety_score": round(sa * 100, 2),
            "integrity_score": round(ig * 100, 2),
            "neural_risk_composite": round(comp * 100, 2),
            "neural_pattern": pattern,
            "neural_risk": risk,
            "neural_severity": sev,
            "recommended_action": act,
            "has_critical_signal": comp >= 0.40 or inp.neural_latency_risk >= 0.70 or inp.bci_safety_compliance <= 0.30,
            "requires_disconnect": comp >= 0.25 or inp.neural_fatigue_accumulation >= 0.65 or inp.biometric_privacy_exposure >= 0.70,
            "estimated_neural_risk_index": round(min(comp / 1.0 * (1 - inp.neural_signal_integrity + 0.01) * 10, 10.0), 2),
            "neural_signal": sig,
        }

    def assess_batch(self, inputs: List[ARNeuralInput]) -> List[Dict[str, Any]]:
        return [self._assess_one(inp) for inp in inputs]

    def summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Returns exactly 13 keys."""
        rc: Dict[str, int] = {}
        pc: Dict[str, int] = {}
        sc: Dict[str, int] = {}
        ac: Dict[str, int] = {}
        t_nr = t_im = t_sa = t_ig = t_comp = t_idx = 0.0
        crit_c = disc_c = 0

        for r in results:
            rc[r["neural_risk"]] = rc.get(r["neural_risk"], 0) + 1
            pc[r["neural_pattern"]] = pc.get(r["neural_pattern"], 0) + 1
            sc[r["neural_severity"]] = sc.get(r["neural_severity"], 0) + 1
            ac[r["recommended_action"]] = ac.get(r["recommended_action"], 0) + 1
            t_nr += r["neural_risk_score"]
            t_im += r["immersion_score"]
            t_sa += r["safety_score"]
            t_ig += r["integrity_score"]
            t_comp += r["neural_risk_composite"]
            t_idx += r["estimated_neural_risk_index"]
            if r["has_critical_signal"]:
                crit_c += 1
            if r["requires_disconnect"]:
                disc_c += 1

        n = len(results) or 1
        return {
            "total": len(results),
            "risk_counts": rc,
            "pattern_counts": pc,
            "severity_counts": sc,
            "action_counts": ac,
            "avg_neural_risk_composite": round(t_comp / n, 1),
            "critical_signal_count": crit_c,
            "disconnect_required_count": disc_c,
            "avg_neural_risk_score": round(t_nr / n, 1),
            "avg_immersion_score": round(t_im / n, 1),
            "avg_safety_score": round(t_sa / n, 1),
            "avg_integrity_score": round(t_ig / n, 1),
            "avg_estimated_neural_risk_index": round(t_idx / n, 2),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Returns exactly 15 keys describing this engine instance."""
        return {
            "module_id": "274",
            "module_name": "Augmented Reality Engineering & Neural Interface Engine",
            "platform": "Caelum Partners Swarm Intelligence",
            "version": "1.0.0",
            "interface_types": [
                "retinal_projection",
                "holographic_overlay",
                "haptic_neural",
                "brain_computer_interface",
                "spatial_computing",
                "mixed_reality_mesh",
                "neural_feedback_loop",
                "embodied_ai_avatar",
            ],
            "patterns": ["neural_overload", "reality_dissociation", "biometric_breach", "bci_failure", "sensory_collapse", "none"],
            "severities": ["critical_neural", "unstable", "calibrating", "immersive"],
            "risk_levels": ["critical", "high", "moderate", "low"],
            "actions": ["neural_emergency_disconnect", "bci_safety_lockdown", "immersion_recalibration", "privacy_shield", "neural_monitoring", "no_action"],
            "sub_score_weights": {"neural_risk_score": 0.30, "immersion_score": 0.25, "safety_score": 0.25, "integrity_score": 0.20},
            "numeric_fields_count": 17,
            "summary_keys_count": 13,
            "output_keys_count": 15,
            "language": "fr/en bilingual signals",
            "author": "Caelum Partners — Chaima Mhadbi",
        }
