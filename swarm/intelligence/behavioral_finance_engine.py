"""Behavioral Finance & Wealth Psychology Intelligence Engine — Module 332.

Detects cognitive, emotional, narrative, and systemic behavioral biases in financial markets
to anticipate behavioral crashes, speculative manias, and collective delusion dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BehavioralFinanceInput:
    entity_id: str
    market_segment: str
    region: str
    # 17 float fields (0-1)
    herd_behavior_intensity: float
    loss_aversion_amplification: float
    overconfidence_bias_level: float
    recency_bias_dominance: float
    anchoring_distortion_index: float
    narrative_economy_susceptibility: float
    FOMO_cascade_vulnerability: float
    panic_selling_propensity: float
    cognitive_dissonance_in_portfolio: float
    mental_accounting_fragmentation: float
    framing_effect_exploitation: float
    sunk_cost_trap_prevalence: float
    availability_heuristic_distortion: float
    status_quo_bias_resistance: float
    wealth_identity_fusion: float
    speculative_bubble_formation_risk: float
    collective_delusion_index: float


def _cognitive_score(inp: BehavioralFinanceInput) -> float:
    """Weight 0.30 — herd*0.4 + overconfidence*0.35 + anchoring*0.25, scaled x100."""
    return round(
        (
            inp.herd_behavior_intensity * 0.4
            + inp.overconfidence_bias_level * 0.35
            + inp.anchoring_distortion_index * 0.25
        )
        * 100,
        2,
    )


def _emotional_score(inp: BehavioralFinanceInput) -> float:
    """Weight 0.25 — loss_aversion*0.4 + panic_selling*0.35 + FOMO*0.25, scaled x100."""
    return round(
        (
            inp.loss_aversion_amplification * 0.4
            + inp.panic_selling_propensity * 0.35
            + inp.FOMO_cascade_vulnerability * 0.25
        )
        * 100,
        2,
    )


def _narrative_score(inp: BehavioralFinanceInput) -> float:
    """Weight 0.25 — narrative_susceptibility*0.4 + collective_delusion*0.35 + speculative_bubble*0.25, x100."""
    return round(
        (
            inp.narrative_economy_susceptibility * 0.4
            + inp.collective_delusion_index * 0.35
            + inp.speculative_bubble_formation_risk * 0.25
        )
        * 100,
        2,
    )


def _systemic_score(inp: BehavioralFinanceInput) -> float:
    """Weight 0.20 — cognitive_dissonance*0.4 + mental_accounting*0.35 + wealth_identity*0.25, x100."""
    return round(
        (
            inp.cognitive_dissonance_in_portfolio * 0.4
            + inp.mental_accounting_fragmentation * 0.35
            + inp.wealth_identity_fusion * 0.25
        )
        * 100,
        2,
    )


def _composite(cog: float, emo: float, nar: float, sys: float) -> float:
    return round(cog * 0.30 + emo * 0.25 + nar * 0.25 + sys * 0.20, 2)


def _risk_level(composite: float) -> str:
    if composite >= 60:
        return "critical"
    if composite >= 40:
        return "high"
    if composite >= 20:
        return "moderate"
    return "low"


def _behavioral_pattern(inp: BehavioralFinanceInput) -> str:
    """Checked in order; first match wins."""
    if inp.herd_behavior_intensity >= 0.70 and inp.panic_selling_propensity >= 0.65:
        return "mass_hysteria_crash"
    if inp.speculative_bubble_formation_risk >= 0.70 and inp.collective_delusion_index >= 0.65:
        return "speculative_mania"
    if inp.narrative_economy_susceptibility >= 0.70 and inp.cognitive_dissonance_in_portfolio >= 0.65:
        return "narrative_collapse"
    if inp.FOMO_cascade_vulnerability >= 0.70 and inp.overconfidence_bias_level >= 0.65:
        return "FOMO_spiral"
    if inp.loss_aversion_amplification >= 0.70 and inp.sunk_cost_trap_prevalence >= 0.65:
        return "cognitive_trap_cascade"
    return "none"


def _severity(risk_level: str) -> str:
    mapping = {
        "critical": "krach_comportemental_systemique",
        "high":     "instabilite_comportementale_majeure",
        "moderate": "biais_structurels_actifs",
        "low":      "comportement_rationnel_relatif",
    }
    return mapping[risk_level]


def _recommended_action(risk_level: str) -> str:
    mapping = {
        "critical": "circuit_breaker_comportemental_urgent",
        "high":     "debiaisage_systemique_active",
        "moderate": "surveillance_comportementale_renforcee",
        "low":      "monitoring_biais_continu",
    }
    return mapping[risk_level]


def _signal(risk_level: str) -> str:
    mapping = {
        "critical": "Krach comportemental imminent — biais systemiques critiques",
        "high":     "Instabilite comportementale majeure detectee",
        "moderate": "Biais actifs — surveillance requise",
        "low":      "Comportement financier relativement rationnel",
    }
    return mapping[risk_level]


# ── Mock entities ─────────────────────────────────────────────────────────────

_MOCK_ENTITIES: list[BehavioralFinanceInput] = [
    # BFE-001 critical + mass_hysteria_crash (herd>=0.70, panic_selling>=0.65)
    BehavioralFinanceInput(
        "BFE-001", "retail", "EMEA",
        herd_behavior_intensity=0.85,
        loss_aversion_amplification=0.80,
        overconfidence_bias_level=0.80,
        recency_bias_dominance=0.75,
        anchoring_distortion_index=0.75,
        narrative_economy_susceptibility=0.78,
        FOMO_cascade_vulnerability=0.78,
        panic_selling_propensity=0.75,
        cognitive_dissonance_in_portfolio=0.78,
        mental_accounting_fragmentation=0.72,
        framing_effect_exploitation=0.70,
        sunk_cost_trap_prevalence=0.68,
        availability_heuristic_distortion=0.70,
        status_quo_bias_resistance=0.65,
        wealth_identity_fusion=0.72,
        speculative_bubble_formation_risk=0.78,
        collective_delusion_index=0.75,
    ),
    # BFE-002 low risk no pattern
    BehavioralFinanceInput(
        "BFE-002", "institutional", "NAMER",
        herd_behavior_intensity=0.12,
        loss_aversion_amplification=0.10,
        overconfidence_bias_level=0.15,
        recency_bias_dominance=0.10,
        anchoring_distortion_index=0.12,
        narrative_economy_susceptibility=0.10,
        FOMO_cascade_vulnerability=0.08,
        panic_selling_propensity=0.10,
        cognitive_dissonance_in_portfolio=0.12,
        mental_accounting_fragmentation=0.10,
        framing_effect_exploitation=0.08,
        sunk_cost_trap_prevalence=0.10,
        availability_heuristic_distortion=0.12,
        status_quo_bias_resistance=0.10,
        wealth_identity_fusion=0.08,
        speculative_bubble_formation_risk=0.10,
        collective_delusion_index=0.08,
    ),
    # BFE-003 high risk + speculative_mania (speculative_bubble>=0.70, collective_delusion>=0.65)
    BehavioralFinanceInput(
        "BFE-003", "retail", "APAC",
        herd_behavior_intensity=0.58,
        loss_aversion_amplification=0.52,
        overconfidence_bias_level=0.60,
        recency_bias_dominance=0.55,
        anchoring_distortion_index=0.50,
        narrative_economy_susceptibility=0.65,
        FOMO_cascade_vulnerability=0.60,
        panic_selling_propensity=0.50,
        cognitive_dissonance_in_portfolio=0.55,
        mental_accounting_fragmentation=0.52,
        framing_effect_exploitation=0.48,
        sunk_cost_trap_prevalence=0.50,
        availability_heuristic_distortion=0.55,
        status_quo_bias_resistance=0.50,
        wealth_identity_fusion=0.52,
        speculative_bubble_formation_risk=0.75,
        collective_delusion_index=0.70,
    ),
    # BFE-004 low risk no pattern
    BehavioralFinanceInput(
        "BFE-004", "b2b", "MEA",
        herd_behavior_intensity=0.18,
        loss_aversion_amplification=0.15,
        overconfidence_bias_level=0.20,
        recency_bias_dominance=0.15,
        anchoring_distortion_index=0.18,
        narrative_economy_susceptibility=0.15,
        FOMO_cascade_vulnerability=0.12,
        panic_selling_propensity=0.14,
        cognitive_dissonance_in_portfolio=0.16,
        mental_accounting_fragmentation=0.14,
        framing_effect_exploitation=0.12,
        sunk_cost_trap_prevalence=0.15,
        availability_heuristic_distortion=0.18,
        status_quo_bias_resistance=0.12,
        wealth_identity_fusion=0.14,
        speculative_bubble_formation_risk=0.15,
        collective_delusion_index=0.12,
    ),
    # BFE-005 critical + FOMO_spiral (FOMO>=0.70, overconfidence>=0.65)
    # spec_bubble<0.70, coll_del<0.65, narrative_s<0.70 to avoid earlier pattern triggers
    BehavioralFinanceInput(
        "BFE-005", "b2c", "LATAM",
        herd_behavior_intensity=0.60,
        loss_aversion_amplification=0.75,
        overconfidence_bias_level=0.80,
        recency_bias_dominance=0.70,
        anchoring_distortion_index=0.68,
        narrative_economy_susceptibility=0.65,
        FOMO_cascade_vulnerability=0.85,
        panic_selling_propensity=0.58,
        cognitive_dissonance_in_portfolio=0.68,
        mental_accounting_fragmentation=0.65,
        framing_effect_exploitation=0.62,
        sunk_cost_trap_prevalence=0.55,
        availability_heuristic_distortion=0.65,
        status_quo_bias_resistance=0.60,
        wealth_identity_fusion=0.70,
        speculative_bubble_formation_risk=0.65,
        collective_delusion_index=0.60,
    ),
    # BFE-006 moderate risk no pattern (composite ~26-35)
    BehavioralFinanceInput(
        "BFE-006", "partner", "EMEA",
        herd_behavior_intensity=0.28,
        loss_aversion_amplification=0.26,
        overconfidence_bias_level=0.30,
        recency_bias_dominance=0.28,
        anchoring_distortion_index=0.28,
        narrative_economy_susceptibility=0.26,
        FOMO_cascade_vulnerability=0.24,
        panic_selling_propensity=0.26,
        cognitive_dissonance_in_portfolio=0.28,
        mental_accounting_fragmentation=0.26,
        framing_effect_exploitation=0.22,
        sunk_cost_trap_prevalence=0.25,
        availability_heuristic_distortion=0.28,
        status_quo_bias_resistance=0.22,
        wealth_identity_fusion=0.26,
        speculative_bubble_formation_risk=0.26,
        collective_delusion_index=0.24,
    ),
    # BFE-007 high risk + narrative_collapse (narrative_suscep>=0.70, cognitive_dissonance>=0.65)
    BehavioralFinanceInput(
        "BFE-007", "institutional", "APAC",
        herd_behavior_intensity=0.52,
        loss_aversion_amplification=0.55,
        overconfidence_bias_level=0.55,
        recency_bias_dominance=0.52,
        anchoring_distortion_index=0.50,
        narrative_economy_susceptibility=0.78,
        FOMO_cascade_vulnerability=0.55,
        panic_selling_propensity=0.52,
        cognitive_dissonance_in_portfolio=0.72,
        mental_accounting_fragmentation=0.60,
        framing_effect_exploitation=0.55,
        sunk_cost_trap_prevalence=0.52,
        availability_heuristic_distortion=0.52,
        status_quo_bias_resistance=0.50,
        wealth_identity_fusion=0.55,
        speculative_bubble_formation_risk=0.55,
        collective_delusion_index=0.52,
    ),
    # BFE-008 critical + cognitive_trap_cascade (loss_aversion>=0.70, sunk_cost>=0.65)
    # herd<0.70 OR panic<0.65 to avoid mass_hysteria, spec_bubble<0.70 for no speculative_mania,
    # narrative_s<0.70 to avoid narrative_collapse, fomo<0.70 to avoid FOMO_spiral
    BehavioralFinanceInput(
        "BFE-008", "retail", "NAMER",
        herd_behavior_intensity=0.68,
        loss_aversion_amplification=0.85,
        overconfidence_bias_level=0.72,
        recency_bias_dominance=0.78,
        anchoring_distortion_index=0.70,
        narrative_economy_susceptibility=0.65,
        FOMO_cascade_vulnerability=0.68,
        panic_selling_propensity=0.62,
        cognitive_dissonance_in_portfolio=0.78,
        mental_accounting_fragmentation=0.75,
        framing_effect_exploitation=0.68,
        sunk_cost_trap_prevalence=0.80,
        availability_heuristic_distortion=0.70,
        status_quo_bias_resistance=0.65,
        wealth_identity_fusion=0.72,
        speculative_bubble_formation_risk=0.65,
        collective_delusion_index=0.65,
    ),
]


class BehavioralFinanceEngine:
    """Module 332 — Detects behavioral finance biases and wealth psychology dynamics."""

    def __init__(self) -> None:
        self._results: list[dict[str, Any]] = []

    def analyze(self, inp: BehavioralFinanceInput) -> dict[str, Any]:
        cog = _cognitive_score(inp)
        emo = _emotional_score(inp)
        nar = _narrative_score(inp)
        sys = _systemic_score(inp)
        comp = _composite(cog, emo, nar, sys)

        risk = _risk_level(comp)
        pattern = _behavioral_pattern(inp)
        sev = _severity(risk)
        action = _recommended_action(risk)
        sig = _signal(risk)

        result = _to_dict(inp, cog, emo, nar, sys, comp, risk, pattern, sev, action, sig)
        self._results.append(result)
        return result

    def analyze_batch(self, inputs: list[BehavioralFinanceInput]) -> list[dict[str, Any]]:
        for inp in inputs:
            self.analyze(inp)
        self._results.sort(key=lambda r: r["composite_score"], reverse=True)
        return self._results

    def load_mock_entities(self) -> list[dict[str, Any]]:
        self._results.clear()
        return self.analyze_batch(_MOCK_ENTITIES)

    def reset(self) -> None:
        self._results.clear()

    @staticmethod
    def summary(results: list[dict[str, Any]]) -> dict[str, Any]:
        """Returns exactly 13 keys."""
        n = len(results)
        if n == 0:
            return {
                "module_id":                           332,
                "module_name":                         "Behavioral Finance & Wealth Psychology Intelligence Engine",
                "total_entities":                      0,
                "critical_count":                      0,
                "high_count":                          0,
                "moderate_count":                      0,
                "low_count":                           0,
                "avg_composite":                       0.0,
                "pattern_distribution":                {},
                "risk_distribution":                   {},
                "severity_distribution":               {},
                "action_distribution":                 {},
                "avg_estimated_behavioral_risk_index": 0.0,
            }

        critical_count = sum(1 for r in results if r["risk_level"] == "critical")
        high_count     = sum(1 for r in results if r["risk_level"] == "high")
        moderate_count = sum(1 for r in results if r["risk_level"] == "moderate")
        low_count      = sum(1 for r in results if r["risk_level"] == "low")
        avg_composite  = round(sum(r["composite_score"] for r in results) / n, 2)

        pattern_dist:  dict[str, int] = {}
        risk_dist:     dict[str, int] = {}
        severity_dist: dict[str, int] = {}
        action_dist:   dict[str, int] = {}

        for r in results:
            pattern_dist[r["behavioral_pattern"]] = pattern_dist.get(r["behavioral_pattern"], 0) + 1
            risk_dist[r["risk_level"]]            = risk_dist.get(r["risk_level"], 0) + 1
            severity_dist[r["severity"]]          = severity_dist.get(r["severity"], 0) + 1
            action_dist[r["recommended_action"]]  = action_dist.get(r["recommended_action"], 0) + 1

        return {
            "module_id":                           332,
            "module_name":                         "Behavioral Finance & Wealth Psychology Intelligence Engine",
            "total_entities":                      n,
            "critical_count":                      critical_count,
            "high_count":                          high_count,
            "moderate_count":                      moderate_count,
            "low_count":                           low_count,
            "avg_composite":                       avg_composite,
            "pattern_distribution":                pattern_dist,
            "risk_distribution":                   risk_dist,
            "severity_distribution":               severity_dist,
            "action_distribution":                 action_dist,
            "avg_estimated_behavioral_risk_index": round(avg_composite / 100 * 10, 2),
        }


def _to_dict(
    inp: BehavioralFinanceInput,
    cog: float,
    emo: float,
    nar: float,
    sys: float,
    comp: float,
    risk: str,
    pattern: str,
    sev: str,
    action: str,
    sig: str,
) -> dict[str, Any]:
    """Returns exactly 15 keys."""
    return {
        "entity_id":                        inp.entity_id,
        "market_segment":                   inp.market_segment,
        "region":                           inp.region,
        "cognitive_score":                  cog,
        "emotional_score":                  emo,
        "narrative_score":                  nar,
        "systemic_score":                   sys,
        "composite_score":                  comp,
        "risk_level":                       risk,
        "behavioral_pattern":               pattern,
        "severity":                         sev,
        "recommended_action":               action,
        "signal":                           sig,
        "speculative_bubble_formation_risk": inp.speculative_bubble_formation_risk,
        "collective_delusion_index":        inp.collective_delusion_index,
    }
