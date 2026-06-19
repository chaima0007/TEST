from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class GameInput:
    game_id: str
    game_type: str  # pricing_war/merger_negotiation/market_entry/supply_chain_contract/regulatory_negotiation/alliance_formation/talent_competition/ip_licensing
    region: str
    nash_equilibrium_stability: float
    dominant_strategy_clarity: float
    cooperative_surplus_potential: float
    defection_temptation_index: float
    information_asymmetry_score: float
    commitment_credibility_score: float
    payoff_matrix_volatility: float
    iteration_learning_rate: float
    coalition_stability_score: float
    threat_credibility_score: float
    outside_option_strength: float
    time_pressure_index: float
    reputation_effect_weight: float
    zero_sum_intensity: float
    signaling_effectiveness: float
    punishment_mechanism_strength: float
    bargaining_power_score: float


class GameResult:
    def __init__(
        self,
        game_id: str,
        game_type: str,
        region: str,
        stability_score: float,
        strategy_score: float,
        cooperation_score: float,
        information_score: float,
        game_composite: float,
        game_risk: str,
        game_pattern: str,
        game_severity: str,
        recommended_action: str,
        recommended_action_secondary: str,
        game_signal: str,
        estimated_game_loss_index: float,
    ):
        self.game_id = game_id
        self.game_type = game_type
        self.region = region
        self.stability_score = stability_score
        self.strategy_score = strategy_score
        self.cooperation_score = cooperation_score
        self.information_score = information_score
        self.game_composite = game_composite
        self.game_risk = game_risk
        self.game_pattern = game_pattern
        self.game_severity = game_severity
        self.recommended_action = recommended_action
        self.recommended_action_secondary = recommended_action_secondary
        self.game_signal = game_signal
        self.estimated_game_loss_index = estimated_game_loss_index

    def to_dict(self) -> Dict[str, Any]:
        # exactly 15 keys
        return {
            "game_id": self.game_id,
            "game_type": self.game_type,
            "region": self.region,
            "stability_score": self.stability_score,
            "strategy_score": self.strategy_score,
            "cooperation_score": self.cooperation_score,
            "information_score": self.information_score,
            "game_composite": self.game_composite,
            "game_risk": self.game_risk,
            "game_pattern": self.game_pattern,
            "game_severity": self.game_severity,
            "recommended_action": self.recommended_action,
            "recommended_action_secondary": self.recommended_action_secondary,
            "game_signal": self.game_signal,
            "estimated_game_loss_index": self.estimated_game_loss_index,
        }


def _stability_score(g: GameInput) -> float:
    # nash_equilibrium_stability (inverted), payoff_matrix_volatility (inverted), commitment_credibility_score
    raw = (
        (1.0 - g.nash_equilibrium_stability) * 100 * 0.40
        + g.payoff_matrix_volatility * 100 * 0.35
        + (1.0 - g.commitment_credibility_score) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _strategy_score(g: GameInput) -> float:
    # dominant_strategy_clarity (inverted), threat_credibility_score (inverted), punishment_mechanism_strength (inverted)
    raw = (
        (1.0 - g.dominant_strategy_clarity) * 100 * 0.40
        + (1.0 - g.threat_credibility_score) * 100 * 0.35
        + (1.0 - g.punishment_mechanism_strength) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _cooperation_score(g: GameInput) -> float:
    # cooperative_surplus_potential (inverted), coalition_stability_score (inverted), reputation_effect_weight (inverted)
    raw = (
        (1.0 - g.cooperative_surplus_potential) * 100 * 0.40
        + (1.0 - g.coalition_stability_score) * 100 * 0.35
        + (1.0 - g.reputation_effect_weight) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _information_score(g: GameInput) -> float:
    # information_asymmetry_score (inverted means high asymmetry = high risk, so NOT inverted here)
    # signaling_effectiveness (inverted), iteration_learning_rate (inverted)
    raw = (
        g.information_asymmetry_score * 100 * 0.40
        + (1.0 - g.signaling_effectiveness) * 100 * 0.35
        + (1.0 - g.iteration_learning_rate) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _composite(stab: float, strat: float, coop: float, info: float) -> float:
    return min(round(stab * 0.30 + strat * 0.25 + coop * 0.25 + info * 0.20, 2), 100.0)


def _risk(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _pattern(g: GameInput) -> str:
    if g.zero_sum_intensity >= 0.75 and g.cooperative_surplus_potential <= 0.25:
        return "zero_sum_destruction"
    if g.nash_equilibrium_stability <= 0.25 and g.defection_temptation_index >= 0.70:
        return "prisoners_dilemma_trap"
    if g.nash_equilibrium_stability <= 0.30 and g.commitment_credibility_score <= 0.30:
        return "nash_deadlock"
    if g.defection_temptation_index >= 0.65 and g.coalition_stability_score <= 0.35:
        return "defection_cascade"
    if g.information_asymmetry_score >= 0.65 and g.signaling_effectiveness <= 0.35:
        return "information_warfare"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 60:
        return "destructive"
    if comp >= 40:
        return "unstable"
    if comp >= 20:
        return "negotiating"
    return "optimal"


def _actions(risk: str) -> tuple:
    if risk == "critical":
        return ("emergency_mediation", "game_reset")
    if risk == "high":
        return ("commitment_device", "coalition_building")
    if risk == "moderate":
        return ("strategy_monitoring", "strategy_monitoring")
    return ("no_action", "no_action")


def _signal(g: GameInput, pattern: str, comp: float) -> str:
    if comp < 20:
        return (
            "Équilibre de Nash optimal — stratégie dominante claire, "
            "coopération stable, information équilibrée"
        )
    pat_labels = {
        "prisoners_dilemma_trap": "Piège du dilemme du prisonnier",
        "nash_deadlock": "Blocage de Nash",
        "defection_cascade": "Cascade de défection",
        "information_warfare": "Guerre de l'information",
        "zero_sum_destruction": "Destruction somme nulle",
    }
    label = pat_labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — équilibre Nash {g.nash_equilibrium_stability:.2f} "
        f"— surplus coopératif {g.cooperative_surplus_potential:.2f} "
        f"— tentation défection {g.defection_temptation_index:.2f} "
        f"— composite {round(comp)}"
    )


def _game_loss_index(comp: float, nash_stability: float) -> float:
    return round(min(comp / 100 * (1 - nash_stability + 0.01) * 10, 10.0), 2)


MOCK_GAMES: List[GameInput] = [
    # GM-001 pricing_war EMEA — critical / zero_sum_destruction
    GameInput(
        game_id="GM-001", game_type="pricing_war", region="EMEA",
        nash_equilibrium_stability=0.08, dominant_strategy_clarity=0.72,
        cooperative_surplus_potential=0.10, defection_temptation_index=0.88,
        information_asymmetry_score=0.75, commitment_credibility_score=0.12,
        payoff_matrix_volatility=0.85, iteration_learning_rate=0.20,
        coalition_stability_score=0.10, threat_credibility_score=0.75,
        outside_option_strength=0.30, time_pressure_index=0.80,
        reputation_effect_weight=0.15, zero_sum_intensity=0.90,
        signaling_effectiveness=0.18, punishment_mechanism_strength=0.70,
        bargaining_power_score=0.55,
    ),
    # GM-002 merger_negotiation NAMER — low
    GameInput(
        game_id="GM-002", game_type="merger_negotiation", region="NAMER",
        nash_equilibrium_stability=0.88, dominant_strategy_clarity=0.82,
        cooperative_surplus_potential=0.85, defection_temptation_index=0.15,
        information_asymmetry_score=0.18, commitment_credibility_score=0.90,
        payoff_matrix_volatility=0.12, iteration_learning_rate=0.88,
        coalition_stability_score=0.85, threat_credibility_score=0.80,
        outside_option_strength=0.70, time_pressure_index=0.20,
        reputation_effect_weight=0.88, zero_sum_intensity=0.10,
        signaling_effectiveness=0.85, punishment_mechanism_strength=0.80,
        bargaining_power_score=0.75,
    ),
    # GM-003 market_entry APAC — high / prisoners_dilemma_trap
    GameInput(
        game_id="GM-003", game_type="market_entry", region="APAC",
        nash_equilibrium_stability=0.20, dominant_strategy_clarity=0.48,
        cooperative_surplus_potential=0.42, defection_temptation_index=0.72,
        information_asymmetry_score=0.60, commitment_credibility_score=0.35,
        payoff_matrix_volatility=0.62, iteration_learning_rate=0.45,
        coalition_stability_score=0.38, threat_credibility_score=0.52,
        outside_option_strength=0.55, time_pressure_index=0.58,
        reputation_effect_weight=0.40, zero_sum_intensity=0.55,
        signaling_effectiveness=0.40, punishment_mechanism_strength=0.48,
        bargaining_power_score=0.45,
    ),
    # GM-004 supply_chain_contract LATAM — low
    GameInput(
        game_id="GM-004", game_type="supply_chain_contract", region="LATAM",
        nash_equilibrium_stability=0.80, dominant_strategy_clarity=0.78,
        cooperative_surplus_potential=0.80, defection_temptation_index=0.18,
        information_asymmetry_score=0.20, commitment_credibility_score=0.85,
        payoff_matrix_volatility=0.15, iteration_learning_rate=0.82,
        coalition_stability_score=0.78, threat_credibility_score=0.75,
        outside_option_strength=0.65, time_pressure_index=0.22,
        reputation_effect_weight=0.82, zero_sum_intensity=0.12,
        signaling_effectiveness=0.80, punishment_mechanism_strength=0.78,
        bargaining_power_score=0.70,
    ),
    # GM-005 regulatory_negotiation EMEA — critical / nash_deadlock
    GameInput(
        game_id="GM-005", game_type="regulatory_negotiation", region="EMEA",
        nash_equilibrium_stability=0.12, dominant_strategy_clarity=0.35,
        cooperative_surplus_potential=0.28, defection_temptation_index=0.78,
        information_asymmetry_score=0.72, commitment_credibility_score=0.15,
        payoff_matrix_volatility=0.80, iteration_learning_rate=0.22,
        coalition_stability_score=0.20, threat_credibility_score=0.40,
        outside_option_strength=0.38, time_pressure_index=0.75,
        reputation_effect_weight=0.22, zero_sum_intensity=0.68,
        signaling_effectiveness=0.20, punishment_mechanism_strength=0.30,
        bargaining_power_score=0.42,
    ),
    # GM-006 alliance_formation MEA — moderate
    GameInput(
        game_id="GM-006", game_type="alliance_formation", region="MEA",
        nash_equilibrium_stability=0.55, dominant_strategy_clarity=0.58,
        cooperative_surplus_potential=0.60, defection_temptation_index=0.40,
        information_asymmetry_score=0.42, commitment_credibility_score=0.60,
        payoff_matrix_volatility=0.38, iteration_learning_rate=0.58,
        coalition_stability_score=0.55, threat_credibility_score=0.58,
        outside_option_strength=0.50, time_pressure_index=0.40,
        reputation_effect_weight=0.58, zero_sum_intensity=0.35,
        signaling_effectiveness=0.55, punishment_mechanism_strength=0.55,
        bargaining_power_score=0.52,
    ),
    # GM-007 talent_competition NAMER — high / defection_cascade
    GameInput(
        game_id="GM-007", game_type="talent_competition", region="NAMER",
        nash_equilibrium_stability=0.30, dominant_strategy_clarity=0.40,
        cooperative_surplus_potential=0.35, defection_temptation_index=0.70,
        information_asymmetry_score=0.55, commitment_credibility_score=0.30,
        payoff_matrix_volatility=0.60, iteration_learning_rate=0.40,
        coalition_stability_score=0.28, threat_credibility_score=0.45,
        outside_option_strength=0.62, time_pressure_index=0.65,
        reputation_effect_weight=0.35, zero_sum_intensity=0.58,
        signaling_effectiveness=0.38, punishment_mechanism_strength=0.40,
        bargaining_power_score=0.48,
    ),
    # GM-008 ip_licensing APAC — low
    GameInput(
        game_id="GM-008", game_type="ip_licensing", region="APAC",
        nash_equilibrium_stability=0.82, dominant_strategy_clarity=0.80,
        cooperative_surplus_potential=0.82, defection_temptation_index=0.12,
        information_asymmetry_score=0.15, commitment_credibility_score=0.88,
        payoff_matrix_volatility=0.10, iteration_learning_rate=0.85,
        coalition_stability_score=0.80, threat_credibility_score=0.78,
        outside_option_strength=0.72, time_pressure_index=0.18,
        reputation_effect_weight=0.85, zero_sum_intensity=0.08,
        signaling_effectiveness=0.82, punishment_mechanism_strength=0.80,
        bargaining_power_score=0.75,
    ),
]


class GameTheoryDecisionEngine:
    def assess_batch(self, inputs: List[GameInput]) -> List[GameResult]:
        results = []
        for g in inputs:
            stab = _stability_score(g)
            strat = _strategy_score(g)
            coop = _cooperation_score(g)
            info = _information_score(g)
            comp = _composite(stab, strat, coop, info)
            risk = _risk(comp)
            pat = _pattern(g)
            sev = _severity(comp)
            act_primary, act_secondary = _actions(risk)
            sig = _signal(g, pat, comp)
            gli = _game_loss_index(comp, g.nash_equilibrium_stability)
            results.append(GameResult(
                game_id=g.game_id,
                game_type=g.game_type,
                region=g.region,
                stability_score=stab,
                strategy_score=strat,
                cooperation_score=coop,
                information_score=info,
                game_composite=comp,
                game_risk=risk,
                game_pattern=pat,
                game_severity=sev,
                recommended_action=act_primary,
                recommended_action_secondary=act_secondary,
                game_signal=sig,
                estimated_game_loss_index=gli,
            ))
        return results

    def summary(self, results: List[GameResult]) -> Dict[str, Any]:
        # exactly 13 keys
        n = len(results) or 1
        risk_counts: Dict[str, int] = {}
        pattern_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts: Dict[str, int] = {}
        t_stab = t_strat = t_coop = t_info = t_comp = t_gli = 0.0
        destructive_count = 0
        mediation_required_count = 0
        for r in results:
            risk_counts[r.game_risk] = risk_counts.get(r.game_risk, 0) + 1
            pattern_counts[r.game_pattern] = pattern_counts.get(r.game_pattern, 0) + 1
            severity_counts[r.game_severity] = severity_counts.get(r.game_severity, 0) + 1
            action_counts[r.recommended_action] = action_counts.get(r.recommended_action, 0) + 1
            t_stab += r.stability_score
            t_strat += r.strategy_score
            t_coop += r.cooperation_score
            t_info += r.information_score
            t_comp += r.game_composite
            t_gli += r.estimated_game_loss_index
            if r.game_severity == "destructive":
                destructive_count += 1
            if r.recommended_action == "emergency_mediation":
                mediation_required_count += 1
        return {
            "total": len(results),
            "risk_counts": risk_counts,
            "pattern_counts": pattern_counts,
            "severity_counts": severity_counts,
            "action_counts": action_counts,
            "avg_game_composite": round(t_comp / n, 1),
            "destructive_count": destructive_count,
            "mediation_required_count": mediation_required_count,
            "avg_stability_score": round(t_stab / n, 1),
            "avg_strategy_score": round(t_strat / n, 1),
            "avg_cooperation_score": round(t_coop / n, 1),
            "avg_information_score": round(t_info / n, 1),
            "avg_estimated_game_loss_index": round(t_gli / n, 2),
        }


if __name__ == "__main__":
    engine = GameTheoryDecisionEngine()
    results = engine.assess_batch(MOCK_GAMES)
    for r in results:
        d = r.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}"
        print(f"{r.game_id} | {r.game_risk:8s} | {r.game_pattern:25s} | composite={r.game_composite}")
    s = engine.summary(results)
    assert len(s) == 13, f"Expected 13 keys, got {len(s)}"
    print("\nSummary:", s)
