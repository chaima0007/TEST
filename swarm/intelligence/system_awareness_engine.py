"""
Module 316 — System Awareness & Feedback Loop Intelligence Engine
Monitors reinforcing/balancing loops, delay dynamics, emergent behaviour,
and systemic blind-spots across complex adaptive systems.

Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SystemAwarenessInput:
    entity_id: str
    system_category: str
    region: str
    # 17 float fields (0.0–1.0)
    reinforcing_loop_dominance: float          # 0-1
    balancing_loop_weakness: float             # 0-1
    delay_accumulation_risk: float             # 0-1
    stock_flow_misalignment: float             # 0-1
    emergence_unpredictability: float          # 0-1
    systemic_leverage_blindness: float         # 0-1
    feedback_signal_noise_ratio: float         # 0-1, inverse: high=good
    archetype_trap_exposure: float             # 0-1
    policy_resistance_index: float             # 0-1
    complexity_escalation_rate: float          # 0-1
    nonlinear_response_risk: float             # 0-1
    tipping_point_proximity: float             # 0-1
    intervention_side_effect_risk: float       # 0-1
    systemic_inertia_index: float              # 0-1
    oscillation_instability: float             # 0-1
    goal_seeking_drift: float                  # 0-1
    system_boundary_permeability: float        # 0-1


@dataclass
class SystemAwarenessResult:
    entity_id: str
    region: str
    system_category: str
    awareness_risk: str
    awareness_pattern: str
    awareness_severity: str
    recommended_action: str
    loop_score: float
    delay_score: float
    emergence_score: float
    blindspot_score: float
    awareness_composite: float
    is_system_crisis: bool
    requires_system_intervention: bool
    system_signal: str

    def to_dict(self) -> Dict:
        return {
            "entity_id":                      self.entity_id,
            "region":                         self.region,
            "system_category":                self.system_category,
            "awareness_risk":                 self.awareness_risk,
            "awareness_pattern":              self.awareness_pattern,
            "awareness_severity":             self.awareness_severity,
            "recommended_action":             self.recommended_action,
            "loop_score":                     self.loop_score,
            "delay_score":                    self.delay_score,
            "emergence_score":                self.emergence_score,
            "blindspot_score":                self.blindspot_score,
            "awareness_composite":            self.awareness_composite,
            "is_system_crisis":               self.is_system_crisis,
            "requires_system_intervention":   self.requires_system_intervention,
            "system_signal":                  self.system_signal,
        }


class SystemAwarenessEngine:
    """
    Module 316 — System Awareness & Feedback Loop Intelligence Engine
    Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
    """

    # ------------------------------------------------------------------ #
    #  Sub-scores (0–100)                                                  #
    # ------------------------------------------------------------------ #

    def _loop_score(self, i: SystemAwarenessInput) -> float:
        return round(
            (
                i.reinforcing_loop_dominance * 0.4
                + i.balancing_loop_weakness * 0.35
                + i.oscillation_instability * 0.25
            ) * 100,
            2,
        )

    def _delay_score(self, i: SystemAwarenessInput) -> float:
        return round(
            (
                i.delay_accumulation_risk * 0.4
                + (1 - i.feedback_signal_noise_ratio) * 0.35
                + i.policy_resistance_index * 0.25
            ) * 100,
            2,
        )

    def _emergence_score(self, i: SystemAwarenessInput) -> float:
        return round(
            (
                i.emergence_unpredictability * 0.4
                + i.nonlinear_response_risk * 0.35
                + i.tipping_point_proximity * 0.25
            ) * 100,
            2,
        )

    def _blindspot_score(self, i: SystemAwarenessInput) -> float:
        return round(
            (
                i.systemic_leverage_blindness * 0.4
                + i.archetype_trap_exposure * 0.35
                + i.intervention_side_effect_risk * 0.25
            ) * 100,
            2,
        )

    def _composite(
        self,
        loop: float,
        delay: float,
        emergence: float,
        blindspot: float,
    ) -> float:
        return round(
            loop * 0.30
            + delay * 0.25
            + emergence * 0.25
            + blindspot * 0.20,
            2,
        )

    # ------------------------------------------------------------------ #
    #  Risk classification                                                 #
    # ------------------------------------------------------------------ #

    def _risk(self, composite: float) -> str:
        if composite >= 60:
            return "critical"
        if composite >= 40:
            return "high"
        if composite >= 20:
            return "moderate"
        return "low"

    # ------------------------------------------------------------------ #
    #  Pattern detection (first match wins)                                #
    # ------------------------------------------------------------------ #

    def _pattern(self, i: SystemAwarenessInput) -> str:
        if i.reinforcing_loop_dominance >= 0.70 and i.balancing_loop_weakness >= 0.65:
            return "runaway_reinforcing_loop"
        if i.delay_accumulation_risk >= 0.70 and i.policy_resistance_index >= 0.65:
            return "delay_catastrophe"
        if i.tipping_point_proximity >= 0.70 and i.nonlinear_response_risk >= 0.65:
            return "tipping_point_cascade"
        if i.archetype_trap_exposure >= 0.70 and i.systemic_leverage_blindness >= 0.65:
            return "archetype_trap"
        if i.oscillation_instability >= 0.70 and i.goal_seeking_drift >= 0.65:
            return "oscillation_death_spiral"
        return "none"

    # ------------------------------------------------------------------ #
    #  Severity                                                            #
    # ------------------------------------------------------------------ #

    def _severity(self, composite: float) -> str:
        if composite >= 75:
            return "system_chaos"
        if composite >= 50:
            return "high_systemic_risk"
        if composite >= 25:
            return "systemic_instability"
        return "system_balanced"

    # ------------------------------------------------------------------ #
    #  Action selection                                                    #
    # ------------------------------------------------------------------ #

    def _action(self, risk: str, pattern: str) -> str:
        if risk == "critical":
            return "systemic_emergency_redesign"
        if risk == "high":
            if pattern == "runaway_reinforcing_loop":
                return "loop_dampening"
            return "leverage_point_intervention"
        if risk == "moderate":
            return "system_monitoring"
        return "no_action"

    # ------------------------------------------------------------------ #
    #  French signal                                                       #
    # ------------------------------------------------------------------ #

    def _signal(
        self,
        i: SystemAwarenessInput,
        pattern: str,
        composite: float,
    ) -> str:
        if composite < 20:
            return (
                "Système équilibré — boucles de rétroaction stables, "
                "dynamiques de délai maîtrisées, aucun comportement émergent critique détecté"
            )
        if composite >= 60:
            pattern_labels: Dict[str, str] = {
                "runaway_reinforcing_loop": "Boucle de renforcement incontrôlée",
                "delay_catastrophe":        "Catastrophe par accumulation de délais",
                "tipping_point_cascade":    "Cascade vers point de basculement",
                "archetype_trap":           "Piège d'archétype systémique",
                "oscillation_death_spiral": "Spirale d'oscillation fatale",
                "none":                     "Défaillance systémique composite",
            }
            label = pattern_labels.get(pattern, pattern.replace("_", " ").title())
            return (
                f"Crise systémique critique — {label}"
                f" — boucles renforçantes {i.reinforcing_loop_dominance:.2f}"
                f" — proximité basculement {i.tipping_point_proximity:.2f}"
                f" — composite {composite:.0f}"
            )
        if composite >= 40:
            pattern_labels_high: Dict[str, str] = {
                "runaway_reinforcing_loop": "Boucle de renforcement en fuite",
                "delay_catastrophe":        "Accumulation critique de délais",
                "tipping_point_cascade":    "Risque de basculement non-linéaire",
                "archetype_trap":           "Exposition aux archétypes pathologiques",
                "oscillation_death_spiral": "Instabilité oscillatoire croissante",
                "none":                     "Déséquilibre systémique",
            }
            label = pattern_labels_high.get(pattern, pattern.replace("_", " ").title())
            return (
                f"Risque systémique élevé — {label}"
                f" — résistance politique {i.policy_resistance_index:.2f}"
                f" — imprévisibilité émergente {i.emergence_unpredictability:.2f}"
                f" — composite {composite:.0f}"
            )
        return (
            f"Instabilité systémique modérée — tensions observées"
            f" — inertie systémique {i.systemic_inertia_index:.2f}"
            f" — perméabilité frontières {i.system_boundary_permeability:.2f}"
            f" — composite {composite:.0f}"
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def _analyze_one(self, i: SystemAwarenessInput) -> SystemAwarenessResult:
        loop       = self._loop_score(i)
        delay      = self._delay_score(i)
        emergence  = self._emergence_score(i)
        blindspot  = self._blindspot_score(i)
        composite  = self._composite(loop, delay, emergence, blindspot)
        risk       = self._risk(composite)
        pattern    = self._pattern(i)
        severity   = self._severity(composite)
        action     = self._action(risk, pattern)
        signal     = self._signal(i, pattern, composite)

        return SystemAwarenessResult(
            entity_id=i.entity_id,
            region=i.region,
            system_category=i.system_category,
            awareness_risk=risk,
            awareness_pattern=pattern,
            awareness_severity=severity,
            recommended_action=action,
            loop_score=loop,
            delay_score=delay,
            emergence_score=emergence,
            blindspot_score=blindspot,
            awareness_composite=composite,
            is_system_crisis=composite >= 60,
            requires_system_intervention=composite >= 40,
            system_signal=signal,
        )

    def analyze(self, entities: List[SystemAwarenessInput]) -> Dict:
        results = [self._analyze_one(i) for i in entities]

        if not results:
            return {
                "total_entities_analyzed":         0,
                "critical_count":                  0,
                "high_count":                      0,
                "moderate_count":                  0,
                "low_count":                       0,
                "crisis_count":                    0,
                "intervention_required_count":     0,
                "avg_loop_score":                  0.0,
                "avg_delay_score":                 0.0,
                "avg_emergence_score":             0.0,
                "avg_blindspot_score":             0.0,
                "avg_awareness_composite":         0.0,
                "avg_estimated_system_risk_index": 0.0,
            }

        n = len(results)

        critical_count  = sum(1 for r in results if r.awareness_risk == "critical")
        high_count      = sum(1 for r in results if r.awareness_risk == "high")
        moderate_count  = sum(1 for r in results if r.awareness_risk == "moderate")
        low_count       = sum(1 for r in results if r.awareness_risk == "low")
        crisis_count    = sum(1 for r in results if r.is_system_crisis)
        intervention_required_count = sum(1 for r in results if r.requires_system_intervention)

        avg_loop       = round(sum(r.loop_score      for r in results) / n, 2)
        avg_delay      = round(sum(r.delay_score     for r in results) / n, 2)
        avg_emergence  = round(sum(r.emergence_score for r in results) / n, 2)
        avg_blindspot  = round(sum(r.blindspot_score for r in results) / n, 2)
        avg_composite  = round(sum(r.awareness_composite for r in results) / n, 2)

        return {
            "total_entities_analyzed":         n,
            "critical_count":                  critical_count,
            "high_count":                      high_count,
            "moderate_count":                  moderate_count,
            "low_count":                       low_count,
            "crisis_count":                    crisis_count,
            "intervention_required_count":     intervention_required_count,
            "avg_loop_score":                  avg_loop,
            "avg_delay_score":                 avg_delay,
            "avg_emergence_score":             avg_emergence,
            "avg_blindspot_score":             avg_blindspot,
            "avg_awareness_composite":         avg_composite,
            "avg_estimated_system_risk_index": round(avg_composite / 100 * 10, 2),
        }
