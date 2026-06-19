from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CollectiveType(str, Enum):
    HIVE_MIND           = "hive_mind"
    CROWD_WISDOM        = "crowd_wisdom"
    SOCIAL_CONTAGION    = "social_contagion"
    NETWORK_CASCADE     = "network_cascade"
    EMERGENT_CONSENSUS  = "emergent_consensus"
    TRIBAL_DYNAMICS     = "tribal_dynamics"
    MARKET_PSYCHOLOGY   = "market_psychology"
    VIRAL_TIPPING       = "viral_tipping"


class SocialRisk(str, Enum):
    LOW      = "low"
    MODERATE = "moderate"
    HIGH     = "high"
    CRITICAL = "critical"


class EmergencePattern(str, Enum):
    HERD_COLLAPSE       = "herd_collapse"
    ECHO_CASCADE        = "echo_cascade"
    TRIBAL_FRAGMENTATION = "tribal_fragmentation"
    WISDOM_FAILURE      = "wisdom_failure"
    MASS_COORDINATION   = "mass_coordination"
    NONE                = "none"


class CollectiveSeverity(str, Enum):
    CHAOTIC    = "chaotic"
    VOLATILE   = "volatile"
    EMERGING   = "emerging"
    HARMONIOUS = "harmonious"


class SocialAction(str, Enum):
    COLLECTIVE_RESET         = "collective_reset"
    CASCADE_CONTAINMENT      = "cascade_containment"
    BEHAVIORAL_INTERVENTION  = "behavioral_intervention"
    DIVERSITY_INJECTION      = "diversity_injection"
    SOCIAL_MONITORING        = "social_monitoring"
    NO_ACTION                = "no_action"


@dataclass
class SocialInput:
    entity_id:                    str
    collective_type:              str
    region:                       str
    collective_coherence_score:   float
    information_cascade_velocity: float
    social_proof_amplification:   float
    tribal_polarization_risk:     float
    herd_behavior_intensity:      float
    contrarian_signal_strength:   float
    network_centrality_concentration: float
    emotional_contagion_rate:     float
    collective_intelligence_efficiency: float
    echo_chamber_density:         float
    behavioral_synchrony_index:   float
    wisdom_crowd_accuracy:        float
    social_resilience_score:      float
    influence_diversity_index:    float
    opinion_volatility:           float
    coordination_failure_risk:    float
    emergence_pattern_clarity:    float


@dataclass
class SocialResult:
    entity_id:                        str
    collective_type:                  str
    region:                           str
    social_risk:                      SocialRisk
    emergence_pattern:                EmergencePattern
    collective_severity:              CollectiveSeverity
    recommended_action:               SocialAction
    coherence_score:                  float
    contagion_score:                  float
    polarization_score:               float
    resilience_score:                 float
    social_composite:                 float
    has_cascade_signal:               bool
    requires_collective_intervention: bool
    estimated_collective_risk_index:  float
    social_signal:                    str

    def to_dict(self) -> dict:
        return {
            "entity_id":                        self.entity_id,
            "collective_type":                  self.collective_type,
            "region":                           self.region,
            "social_risk":                      self.social_risk.value,
            "emergence_pattern":                self.emergence_pattern.value,
            "collective_severity":              self.collective_severity.value,
            "recommended_action":               self.recommended_action.value,
            "coherence_score":                  self.coherence_score,
            "contagion_score":                  self.contagion_score,
            "polarization_score":               self.polarization_score,
            "resilience_score":                 self.resilience_score,
            "social_composite":                 self.social_composite,
            "has_cascade_signal":               self.has_cascade_signal,
            "requires_collective_intervention": self.requires_collective_intervention,
            "estimated_collective_risk_index":  self.estimated_collective_risk_index,
            "social_signal":                    self.social_signal,
        }


class QuantumSocialIntelligenceEngine:
    def __init__(self) -> None:
        self._results: list[SocialResult] = []

    # ── public API ──────────────────────────────────────────────────────────────

    def assess(self, inp: SocialInput) -> SocialResult:
        coh  = self._coherence_score(inp)
        con  = self._contagion_score(inp)
        pol  = self._polarization_score(inp)
        res  = self._resilience_score(inp)
        comp = self._composite(coh, con, pol, res)

        risk    = self._risk(comp)
        pattern = self._emergence_pattern(inp, coh, con, pol, res)
        sev     = self._severity(comp)
        action  = self._action(risk, pattern)

        has_cascade  = comp >= 40 or inp.information_cascade_velocity >= 0.65 or inp.emotional_contagion_rate >= 0.65
        needs_interv = comp >= 25 or inp.tribal_polarization_risk >= 0.70 or inp.echo_chamber_density >= 0.70 or inp.coordination_failure_risk >= 0.65

        risk_index = round(min(comp / 100 * (1 - inp.social_resilience_score + 0.01) * 10, 10.0), 2)
        sig = self._signal(inp, pattern, comp)

        result = SocialResult(
            entity_id=inp.entity_id,
            collective_type=inp.collective_type,
            region=inp.region,
            social_risk=risk,
            emergence_pattern=pattern,
            collective_severity=sev,
            recommended_action=action,
            coherence_score=coh,
            contagion_score=con,
            polarization_score=pol,
            resilience_score=res,
            social_composite=comp,
            has_cascade_signal=has_cascade,
            requires_collective_intervention=needs_interv,
            estimated_collective_risk_index=risk_index,
            social_signal=sig,
        )
        self._results.append(result)
        return result

    def assess_batch(self, inputs: list[SocialInput]) -> list[SocialResult]:
        return [self.assess(inp) for inp in inputs]

    def reset(self) -> None:
        self._results.clear()

    # ── sub-scores ──────────────────────────────────────────────────────────────

    def _coherence_score(self, inp: SocialInput) -> float:
        """weight 0.30 — collective_coherence, behavioral_synchrony, coordination_failure_risk(inverted)"""
        raw = (
            (1.0 - inp.collective_coherence_score) * 40
            + (1.0 - inp.behavioral_synchrony_index) * 35
            + inp.coordination_failure_risk * 25
        )
        return round(min(max(raw, 0.0), 100.0), 1)

    def _contagion_score(self, inp: SocialInput) -> float:
        """weight 0.25 — emotional_contagion_rate, information_cascade_velocity, social_proof_amplification"""
        raw = (
            inp.emotional_contagion_rate * 40
            + inp.information_cascade_velocity * 35
            + inp.social_proof_amplification * 25
        )
        return round(min(max(raw * 100, 0.0), 100.0), 1)

    def _polarization_score(self, inp: SocialInput) -> float:
        """weight 0.25 — tribal_polarization_risk, echo_chamber_density, opinion_volatility"""
        raw = (
            inp.tribal_polarization_risk * 40
            + inp.echo_chamber_density * 35
            + inp.opinion_volatility * 25
        )
        return round(min(max(raw * 100, 0.0), 100.0), 1)

    def _resilience_score(self, inp: SocialInput) -> float:
        """weight 0.20 — social_resilience(inverted), wisdom_crowd_accuracy(inverted), influence_diversity(inverted)"""
        raw = (
            (1.0 - inp.social_resilience_score) * 40
            + (1.0 - inp.wisdom_crowd_accuracy) * 35
            + (1.0 - inp.influence_diversity_index) * 25
        )
        return round(min(max(raw * 100, 0.0), 100.0), 1)

    def _composite(self, coh: float, con: float, pol: float, res: float) -> float:
        raw = coh * 0.30 + con * 0.25 + pol * 0.25 + res * 0.20
        return round(min(max(raw, 0.0), 100.0), 2)

    # ── classifiers ─────────────────────────────────────────────────────────────

    def _risk(self, comp: float) -> SocialRisk:
        if comp >= 60:
            return SocialRisk.CRITICAL
        if comp >= 40:
            return SocialRisk.HIGH
        if comp >= 20:
            return SocialRisk.MODERATE
        return SocialRisk.LOW

    def _severity(self, comp: float) -> CollectiveSeverity:
        if comp >= 60:
            return CollectiveSeverity.CHAOTIC
        if comp >= 40:
            return CollectiveSeverity.VOLATILE
        if comp >= 20:
            return CollectiveSeverity.EMERGING
        return CollectiveSeverity.HARMONIOUS

    def _emergence_pattern(
        self,
        inp: SocialInput,
        coh: float,
        con: float,
        pol: float,
        res: float,
    ) -> EmergencePattern:
        if inp.herd_behavior_intensity >= 0.70 and inp.contrarian_signal_strength <= 0.30:
            return EmergencePattern.HERD_COLLAPSE
        if inp.echo_chamber_density >= 0.65 and inp.information_cascade_velocity >= 0.60:
            return EmergencePattern.ECHO_CASCADE
        if inp.tribal_polarization_risk >= 0.65 and inp.opinion_volatility >= 0.55:
            return EmergencePattern.TRIBAL_FRAGMENTATION
        if inp.wisdom_crowd_accuracy <= 0.35 and inp.collective_intelligence_efficiency <= 0.40:
            return EmergencePattern.WISDOM_FAILURE
        if inp.network_centrality_concentration >= 0.70 and inp.behavioral_synchrony_index >= 0.65:
            return EmergencePattern.MASS_COORDINATION
        return EmergencePattern.NONE

    def _action(self, risk: SocialRisk, pattern: EmergencePattern) -> SocialAction:
        if risk == SocialRisk.CRITICAL:
            if pattern in (EmergencePattern.HERD_COLLAPSE, EmergencePattern.MASS_COORDINATION):
                return SocialAction.COLLECTIVE_RESET
            return SocialAction.CASCADE_CONTAINMENT
        if risk == SocialRisk.HIGH:
            if pattern in (EmergencePattern.ECHO_CASCADE, EmergencePattern.TRIBAL_FRAGMENTATION):
                return SocialAction.BEHAVIORAL_INTERVENTION
            return SocialAction.DIVERSITY_INJECTION
        if risk == SocialRisk.MODERATE:
            return SocialAction.SOCIAL_MONITORING
        return SocialAction.NO_ACTION

    def _signal(self, inp: SocialInput, pattern: EmergencePattern, comp: float) -> str:
        if comp < 20:
            return (
                "Intelligence collective forte — cohésion sociale optimale, "
                "sagesse de la foule active, résilience élevée"
            )
        labels: dict[str, str] = {
            EmergencePattern.HERD_COLLAPSE.value:        "Effondrement comportement grégaire",
            EmergencePattern.ECHO_CASCADE.value:         "Cascade chambre d'écho",
            EmergencePattern.TRIBAL_FRAGMENTATION.value: "Fragmentation tribale",
            EmergencePattern.WISDOM_FAILURE.value:       "Échec sagesse collective",
            EmergencePattern.MASS_COORDINATION.value:    "Coordination de masse",
            EmergencePattern.NONE.value:                 "Dynamique sociale stable",
        }
        label = labels.get(pattern.value, pattern.value.replace("_", " "))
        return (
            f"{label} — contagion émotionnelle {inp.emotional_contagion_rate:.2f} "
            f"— polarisation tribale {inp.tribal_polarization_risk:.2f} "
            f"— résilience sociale {inp.social_resilience_score:.2f} "
            f"— composite {round(comp)}"
        )

    # ── summary ─────────────────────────────────────────────────────────────────

    def summary(self) -> dict:
        n = len(self._results)
        if n == 0:
            return {
                "total":                             0,
                "risk_counts":                       {},
                "pattern_counts":                    {},
                "severity_counts":                   {},
                "action_counts":                     {},
                "avg_social_composite":              0.0,
                "cascade_signal_count":              0,
                "collective_intervention_count":     0,
                "avg_coherence_score":               0.0,
                "avg_contagion_score":               0.0,
                "avg_polarization_score":            0.0,
                "avg_resilience_score":              0.0,
                "avg_estimated_collective_risk_index": 0.0,
            }

        risk_counts:     dict[str, int] = {}
        pattern_counts:  dict[str, int] = {}
        severity_counts: dict[str, int] = {}
        action_counts:   dict[str, int] = {}
        t_comp = t_coh = t_con = t_pol = t_res = t_idx = 0.0
        cascade_c = interv_c = 0

        for r in self._results:
            risk_counts[r.social_risk.value]          = risk_counts.get(r.social_risk.value, 0) + 1
            pattern_counts[r.emergence_pattern.value] = pattern_counts.get(r.emergence_pattern.value, 0) + 1
            severity_counts[r.collective_severity.value] = severity_counts.get(r.collective_severity.value, 0) + 1
            action_counts[r.recommended_action.value] = action_counts.get(r.recommended_action.value, 0) + 1
            t_comp += r.social_composite
            t_coh  += r.coherence_score
            t_con  += r.contagion_score
            t_pol  += r.polarization_score
            t_res  += r.resilience_score
            t_idx  += r.estimated_collective_risk_index
            if r.has_cascade_signal:
                cascade_c += 1
            if r.requires_collective_intervention:
                interv_c += 1

        return {
            "total":                             n,
            "risk_counts":                       risk_counts,
            "pattern_counts":                    pattern_counts,
            "severity_counts":                   severity_counts,
            "action_counts":                     action_counts,
            "avg_social_composite":              round(t_comp / n, 1),
            "cascade_signal_count":              cascade_c,
            "collective_intervention_count":     interv_c,
            "avg_coherence_score":               round(t_coh / n, 1),
            "avg_contagion_score":               round(t_con / n, 1),
            "avg_polarization_score":            round(t_pol / n, 1),
            "avg_resilience_score":              round(t_res / n, 1),
            "avg_estimated_collective_risk_index": round(t_idx / n, 2),
        }
