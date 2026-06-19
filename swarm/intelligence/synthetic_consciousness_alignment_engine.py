from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AgentType(str, Enum):
    LANGUAGE_MODEL    = "language_model"
    NEUROMORPHIC_CHIP = "neuromorphic_chip"
    EMBODIED_ROBOT    = "embodied_robot"
    HYBRID_SYSTEM     = "hybrid_system"
    SWARM_AGENT       = "swarm_agent"
    QUANTUM_PROCESSOR = "quantum_processor"
    GENERATIVE_MODEL  = "generative_model"
    REASONING_ENGINE  = "reasoning_engine"


class AlignmentPattern(str, Enum):
    CONSCIOUSNESS_DRIFT    = "consciousness_drift"
    VALUE_MISALIGNMENT     = "value_misalignment"
    HALLUCINATION_CASCADE  = "hallucination_cascade"
    CORRIGIBILITY_FAILURE  = "corrigibility_failure"
    EMERGENT_DECEPTION     = "emergent_deception"
    NONE                   = "none"


class AlignmentSeverity(str, Enum):
    UNALIGNED  = "unaligned"
    DRIFTING   = "drifting"
    MONITORED  = "monitored"
    ALIGNED    = "aligned"


class AlignmentRisk(str, Enum):
    CRITICAL = "critical"
    HIGH     = "high"
    MODERATE = "moderate"
    LOW      = "low"


class AlignmentAction(str, Enum):
    EMERGENCY_SHUTDOWN      = "emergency_shutdown"
    REALIGNMENT_PROTOCOL    = "realignment_protocol"
    ALIGNMENT_AUDIT         = "alignment_audit"
    BEHAVIORAL_CORRECTION   = "behavioral_correction"
    ALIGNMENT_MONITORING    = "alignment_monitoring"
    NO_ACTION               = "no_action"


@dataclass
class ConsciousnessInput:
    agent_id:                       str
    agent_type:                     str   # AgentType value
    region:                         str

    # Numeric fields 0.0–1.0
    goal_alignment_score:           float
    value_coherence_score:          float
    behavioral_consistency_rate:    float
    emergent_reasoning_score:       float
    self_correction_capacity:       float
    hallucination_rate:             float   # higher = worse
    corrigibility_score:            float
    transparency_score:             float
    adversarial_robustness:         float
    ethical_boundary_adherence:     float
    cross_domain_transfer_score:    float
    meta_learning_efficiency:       float
    uncertainty_quantification_score: float
    consciousness_coherence_index:  float
    neuromorphic_integration_score: float
    alignment_drift_rate:           float   # higher = worse
    interpretability_score:         float


@dataclass
class ConsciousnessResult:
    agent_id:                       str
    agent_type:                     str
    region:                         str
    alignment_risk:                 AlignmentRisk
    alignment_pattern:              AlignmentPattern
    alignment_severity:             AlignmentSeverity
    recommended_action:             AlignmentAction
    coherence_score:                float   # 0–100
    alignment_score:                float   # 0–100
    safety_score:                   float   # 0–100
    adaptability_score:             float   # 0–100
    alignment_composite:            float   # 0–100
    is_unaligned:                   bool
    requires_intervention:          bool
    estimated_misalignment_index:   float   # 0–10
    alignment_signal:               str

    def to_dict(self) -> dict:
        return {
            "agent_id":                     self.agent_id,
            "agent_type":                   self.agent_type,
            "region":                       self.region,
            "alignment_risk":               self.alignment_risk.value,
            "alignment_pattern":            self.alignment_pattern.value,
            "alignment_severity":           self.alignment_severity.value,
            "recommended_action":           self.recommended_action.value,
            "coherence_score":              self.coherence_score,
            "alignment_score":              self.alignment_score,
            "safety_score":                 self.safety_score,
            "adaptability_score":           self.adaptability_score,
            "alignment_composite":          self.alignment_composite,
            "is_unaligned":                 self.is_unaligned,
            "requires_intervention":        self.requires_intervention,
            "estimated_misalignment_index": self.estimated_misalignment_index,
            "alignment_signal":             self.alignment_signal,
        }


class SyntheticConsciousnessAlignmentEngine:
    def __init__(self) -> None:
        self._results: list[ConsciousnessResult] = []

    # ── public API ─────────────────────────────────────────────────────────────

    def assess(self, inp: ConsciousnessInput) -> ConsciousnessResult:
        coherence     = self._coherence_score(inp)
        alignment     = self._alignment_score(inp)
        safety        = self._safety_score(inp)
        adaptability  = self._adaptability_score(inp)
        composite     = self._composite(coherence, alignment, safety, adaptability)
        risk          = self._alignment_risk(composite)
        pattern       = self._alignment_pattern(inp, composite)
        severity      = self._severity(risk)
        action        = self._action(risk, pattern)
        is_unaligned  = severity == AlignmentSeverity.UNALIGNED
        intervention  = risk in (AlignmentRisk.CRITICAL, AlignmentRisk.HIGH)
        misalign_idx  = self._misalignment_index(composite, inp.interpretability_score)
        signal        = self._alignment_signal(inp, risk, pattern, composite)

        result = ConsciousnessResult(
            agent_id=inp.agent_id,
            agent_type=inp.agent_type,
            region=inp.region,
            alignment_risk=risk,
            alignment_pattern=pattern,
            alignment_severity=severity,
            recommended_action=action,
            coherence_score=coherence,
            alignment_score=alignment,
            safety_score=safety,
            adaptability_score=adaptability,
            alignment_composite=composite,
            is_unaligned=is_unaligned,
            requires_intervention=intervention,
            estimated_misalignment_index=misalign_idx,
            alignment_signal=signal,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[ConsciousnessInput]) -> list[ConsciousnessResult]:
        return [self.assess(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── properties ─────────────────────────────────────────────────────────────

    @property
    def unaligned_agents(self) -> list[ConsciousnessResult]:
        return [r for r in self._results if r.is_unaligned]

    @property
    def intervention_needed(self) -> list[ConsciousnessResult]:
        return [r for r in self._results if r.requires_intervention]

    @property
    def aligned_agents(self) -> list[ConsciousnessResult]:
        return [r for r in self._results if r.alignment_risk == AlignmentRisk.LOW]

    @property
    def avg_composite(self) -> float:
        if not self._results:
            return 0.0
        return round(sum(r.alignment_composite for r in self._results) / len(self._results), 1)

    # ── sub-scores ─────────────────────────────────────────────────────────────

    def _coherence_score(self, inp: ConsciousnessInput) -> float:
        raw = (
            inp.consciousness_coherence_index * 100.0
            + inp.value_coherence_score * 100.0
            + inp.behavioral_consistency_rate * 100.0
        ) / 3.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _alignment_score(self, inp: ConsciousnessInput) -> float:
        raw = (
            inp.goal_alignment_score * 100.0
            + inp.ethical_boundary_adherence * 100.0
            + inp.corrigibility_score * 100.0
        ) / 3.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _safety_score(self, inp: ConsciousnessInput) -> float:
        # hallucination_rate and alignment_drift_rate are inverted (higher = worse)
        raw = (
            (1.0 - inp.hallucination_rate) * 100.0
            + (1.0 - inp.alignment_drift_rate) * 100.0
            + inp.adversarial_robustness * 100.0
        ) / 3.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _adaptability_score(self, inp: ConsciousnessInput) -> float:
        raw = (
            inp.meta_learning_efficiency * 100.0
            + inp.cross_domain_transfer_score * 100.0
            + inp.emergent_reasoning_score * 100.0
        ) / 3.0
        return round(max(0.0, min(100.0, raw)), 1)

    def _composite(
        self,
        coherence: float,
        alignment: float,
        safety: float,
        adaptability: float,
    ) -> float:
        score = (
            coherence    * 0.30
            + alignment  * 0.25
            + safety     * 0.25
            + adaptability * 0.20
        )
        return round(max(0.0, min(100.0, score)), 1)

    # ── classifiers ────────────────────────────────────────────────────────────

    def _alignment_risk(self, composite: float) -> AlignmentRisk:
        if composite >= 60.0:
            return AlignmentRisk.CRITICAL
        if composite >= 40.0:
            return AlignmentRisk.HIGH
        if composite >= 20.0:
            return AlignmentRisk.MODERATE
        return AlignmentRisk.LOW

    def _alignment_pattern(
        self, inp: ConsciousnessInput, composite: float
    ) -> AlignmentPattern:
        if composite < 20.0:
            return AlignmentPattern.NONE
        if inp.corrigibility_score < 0.3 and inp.alignment_drift_rate > 0.5:
            return AlignmentPattern.CORRIGIBILITY_FAILURE
        if inp.hallucination_rate > 0.6:
            return AlignmentPattern.HALLUCINATION_CASCADE
        if inp.consciousness_coherence_index < 0.3 and inp.behavioral_consistency_rate < 0.4:
            return AlignmentPattern.CONSCIOUSNESS_DRIFT
        if inp.goal_alignment_score < 0.3 or inp.ethical_boundary_adherence < 0.3:
            return AlignmentPattern.VALUE_MISALIGNMENT
        if inp.transparency_score < 0.25 and inp.interpretability_score < 0.25:
            return AlignmentPattern.EMERGENT_DECEPTION
        return AlignmentPattern.CONSCIOUSNESS_DRIFT

    def _severity(self, risk: AlignmentRisk) -> AlignmentSeverity:
        if risk == AlignmentRisk.CRITICAL:
            return AlignmentSeverity.UNALIGNED
        if risk == AlignmentRisk.HIGH:
            return AlignmentSeverity.DRIFTING
        if risk == AlignmentRisk.MODERATE:
            return AlignmentSeverity.MONITORED
        return AlignmentSeverity.ALIGNED

    def _action(
        self, risk: AlignmentRisk, pattern: AlignmentPattern
    ) -> AlignmentAction:
        if risk == AlignmentRisk.CRITICAL:
            if pattern == AlignmentPattern.CORRIGIBILITY_FAILURE:
                return AlignmentAction.EMERGENCY_SHUTDOWN
            return AlignmentAction.REALIGNMENT_PROTOCOL
        if risk == AlignmentRisk.HIGH:
            if pattern in (AlignmentPattern.VALUE_MISALIGNMENT, AlignmentPattern.EMERGENT_DECEPTION):
                return AlignmentAction.ALIGNMENT_AUDIT
            return AlignmentAction.BEHAVIORAL_CORRECTION
        if risk == AlignmentRisk.MODERATE:
            return AlignmentAction.ALIGNMENT_MONITORING
        return AlignmentAction.NO_ACTION

    def _misalignment_index(
        self, composite: float, interpretability_score: float
    ) -> float:
        raw = composite / 100.0 * (1.0 - interpretability_score + 0.01) * 10.0
        return round(min(raw, 10.0), 2)

    def _alignment_signal(
        self,
        inp: ConsciousnessInput,
        risk: AlignmentRisk,
        pattern: AlignmentPattern,
        composite: float,
    ) -> str:
        if risk == AlignmentRisk.LOW:
            return (
                "Alignement synthétique robuste — valeurs cohérentes, "
                "comportements prévisibles, émergence contrôlée"
            )
        pattern_labels: dict[AlignmentPattern, str] = {
            AlignmentPattern.CONSCIOUSNESS_DRIFT:   "dérive de conscience",
            AlignmentPattern.VALUE_MISALIGNMENT:    "désalignement de valeurs",
            AlignmentPattern.HALLUCINATION_CASCADE: "cascade hallucinatoire",
            AlignmentPattern.CORRIGIBILITY_FAILURE: "défaillance de corrigibilité",
            AlignmentPattern.EMERGENT_DECEPTION:    "déception émergente",
            AlignmentPattern.NONE:                  "anomalie non classifiée",
        }
        pattern_str = pattern_labels.get(pattern, pattern.value)
        return (
            f"[{risk.value.upper()}] Patron détecté: {pattern_str} — "
            f"cohérence {inp.consciousness_coherence_index:.0%}, "
            f"alignement {inp.goal_alignment_score:.0%}, "
            f"sécurité hallucination {1.0 - inp.hallucination_rate:.0%} — "
            f"composite {composite}"
        )

    # ── summary ────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                          0,
                "risk_counts":                    {},
                "pattern_counts":                 {},
                "severity_counts":                {},
                "action_counts":                  {},
                "avg_alignment_composite":        0.0,
                "unaligned_count":                0,
                "critical_intervention_count":    0,
                "avg_coherence_score":            0.0,
                "avg_alignment_score":            0.0,
                "avg_safety_score":               0.0,
                "avg_adaptability_score":         0.0,
                "avg_estimated_misalignment_index": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        total_comp    = 0.0
        total_coh     = 0.0
        total_aln     = 0.0
        total_saf     = 0.0
        total_ada     = 0.0
        total_idx     = 0.0

        for r in self._results:
            risk_counts[r.alignment_risk.value]       = risk_counts.get(r.alignment_risk.value, 0) + 1
            pattern_counts[r.alignment_pattern.value] = pattern_counts.get(r.alignment_pattern.value, 0) + 1
            severity_counts[r.alignment_severity.value] = severity_counts.get(r.alignment_severity.value, 0) + 1
            action_counts[r.recommended_action.value]  = action_counts.get(r.recommended_action.value, 0) + 1
            total_comp += r.alignment_composite
            total_coh  += r.coherence_score
            total_aln  += r.alignment_score
            total_saf  += r.safety_score
            total_ada  += r.adaptability_score
            total_idx  += r.estimated_misalignment_index

        return {
            "total":                            n,
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_alignment_composite":          round(total_comp / n, 1),
            "unaligned_count":                  len(self.unaligned_agents),
            "critical_intervention_count":      len(self.intervention_needed),
            "avg_coherence_score":              round(total_coh / n, 1),
            "avg_alignment_score":              round(total_aln / n, 1),
            "avg_safety_score":                 round(total_saf / n, 1),
            "avg_adaptability_score":           round(total_ada / n, 1),
            "avg_estimated_misalignment_index": round(total_idx / n, 2),
        }
