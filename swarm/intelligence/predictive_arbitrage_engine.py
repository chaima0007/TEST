"""Module 259 — Predictive Analytics & Algorithmic Arbitrage Engine

Monitors predictive signal quality and algorithmic arbitrage opportunities
across portfolios, scoring each signal for alpha capture potential,
execution efficiency, and model resilience.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ArbitrageInput:
    signal_id: str
    signal_type: str  # price_momentum/volatility_spread/sentiment_divergence/macro_signal/cross_asset_correlation/mean_reversion/liquidity_gap/regime_shift
    region: str
    signal_accuracy_score: float
    model_confidence: float
    backtesting_sharpe_ratio: float
    alpha_generation_potential: float
    drawdown_risk: float
    execution_latency_score: float
    market_impact_cost: float
    signal_decay_rate: float
    feature_engineering_score: float
    ensemble_model_diversity: float
    data_quality_score: float
    regime_adaptability: float
    overfitting_risk: float
    transaction_cost_efficiency: float
    real_time_processing_capability: float
    risk_adjusted_return_estimate: float
    portfolio_diversification_benefit: float


class ArbitrageResult:
    def __init__(
        self,
        signal_id: str,
        signal_type: str,
        region: str,
        signal_quality_score: float,
        alpha_capture_score: float,
        execution_score: float,
        resilience_score: float,
        arbitrage_composite: float,
        arbitrage_risk: str,
        arbitrage_pattern: str,
        arbitrage_severity: str,
        recommended_action: str,
        arbitrage_signal: str,
        avg_estimated_alpha_decay_index: float,
        has_active_alert: bool,
    ):
        self.signal_id = signal_id
        self.signal_type = signal_type
        self.region = region
        self.signal_quality_score = signal_quality_score
        self.alpha_capture_score = alpha_capture_score
        self.execution_score = execution_score
        self.resilience_score = resilience_score
        self.arbitrage_composite = arbitrage_composite
        self.arbitrage_risk = arbitrage_risk
        self.arbitrage_pattern = arbitrage_pattern
        self.arbitrage_severity = arbitrage_severity
        self.recommended_action = recommended_action
        self.arbitrage_signal = arbitrage_signal
        self.avg_estimated_alpha_decay_index = avg_estimated_alpha_decay_index
        self.has_active_alert = has_active_alert

    def to_dict(self) -> Dict[str, Any]:
        # exactly 15 keys
        return {
            "signal_id":                       self.signal_id,
            "signal_type":                     self.signal_type,
            "region":                          self.region,
            "signal_quality_score":            self.signal_quality_score,
            "alpha_capture_score":             self.alpha_capture_score,
            "execution_score":                 self.execution_score,
            "resilience_score":                self.resilience_score,
            "arbitrage_composite":             self.arbitrage_composite,
            "arbitrage_risk":                  self.arbitrage_risk,
            "arbitrage_pattern":               self.arbitrage_pattern,
            "arbitrage_severity":              self.arbitrage_severity,
            "recommended_action":              self.recommended_action,
            "arbitrage_signal":                self.arbitrage_signal,
            "avg_estimated_alpha_decay_index": self.avg_estimated_alpha_decay_index,
            "has_active_alert":                self.has_active_alert,
        }


# ─── Sub-score helpers ────────────────────────────────────────────────────────

def _signal_quality_score(a: ArbitrageInput) -> float:
    # signal_accuracy_score (inverted: low accuracy = high risk)
    # model_confidence (inverted), data_quality_score (inverted)
    raw = (
        (1.0 - a.signal_accuracy_score) * 100 * 0.40
        + (1.0 - a.model_confidence) * 100 * 0.35
        + (1.0 - a.data_quality_score) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _alpha_capture_score(a: ArbitrageInput) -> float:
    # alpha_generation_potential (inverted), backtesting_sharpe_ratio (inverted), risk_adjusted_return_estimate (inverted)
    raw = (
        (1.0 - a.alpha_generation_potential) * 100 * 0.40
        + (1.0 - a.backtesting_sharpe_ratio) * 100 * 0.35
        + (1.0 - a.risk_adjusted_return_estimate) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _execution_score(a: ArbitrageInput) -> float:
    # execution_latency_score (high latency = high risk, NOT inverted)
    # market_impact_cost (high cost = high risk, NOT inverted)
    # transaction_cost_efficiency (inverted: low efficiency = high risk)
    raw = (
        a.execution_latency_score * 100 * 0.40
        + a.market_impact_cost * 100 * 0.35
        + (1.0 - a.transaction_cost_efficiency) * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _resilience_score(a: ArbitrageInput) -> float:
    # regime_adaptability (inverted: low adaptability = high risk)
    # ensemble_model_diversity (inverted), overfitting_risk (NOT inverted: high overfitting = high risk)
    raw = (
        (1.0 - a.regime_adaptability) * 100 * 0.40
        + (1.0 - a.ensemble_model_diversity) * 100 * 0.35
        + a.overfitting_risk * 100 * 0.25
    )
    return min(round(raw, 2), 100.0)


def _composite(sq: float, ac: float, ex: float, res: float) -> float:
    return min(round(sq * 0.30 + ac * 0.25 + ex * 0.25 + res * 0.20, 2), 100.0)


def _risk(comp: float) -> str:
    if comp >= 60:
        return "critical"
    if comp >= 40:
        return "high"
    if comp >= 20:
        return "moderate"
    return "low"


def _pattern(a: ArbitrageInput) -> str:
    if a.signal_accuracy_score <= 0.30 and a.model_confidence <= 0.35:
        return "signal_degradation"
    if a.alpha_generation_potential <= 0.25 and a.backtesting_sharpe_ratio <= 0.30:
        return "alpha_erosion"
    if a.execution_latency_score >= 0.70 and a.market_impact_cost >= 0.65:
        return "execution_failure"
    if a.overfitting_risk >= 0.70 and a.ensemble_model_diversity <= 0.30:
        return "model_overfit"
    if a.regime_adaptability <= 0.25 and a.signal_decay_rate >= 0.65:
        return "regime_blindness"
    return "none"


def _severity(comp: float) -> str:
    if comp >= 60:
        return "collapsing"
    if comp >= 40:
        return "degrading"
    if comp >= 20:
        return "stable"
    return "optimal"


def _action(risk: str, pattern: str) -> str:
    if risk == "critical":
        if pattern == "signal_degradation":
            return "model_rebuild"
        if pattern == "execution_failure":
            return "execution_overhaul"
        return "alpha_crisis"
    if risk == "high":
        if pattern == "signal_degradation":
            return "signal_recalibration"
        if pattern == "model_overfit":
            return "ensemble_retrain"
        return "risk_deleverage"
    if risk == "moderate":
        return "performance_monitoring"
    return "no_action"


def _signal_text(a: ArbitrageInput, pattern: str, comp: float) -> str:
    if comp < 20:
        return (
            "Signal prédictif optimal — qualité élevée, alpha stable, "
            "exécution efficiente, modèle robuste"
        )
    pat_labels: Dict[str, str] = {
        "signal_degradation": "Dégradation du signal",
        "alpha_erosion":      "Érosion de l'alpha",
        "execution_failure":  "Défaillance d'exécution",
        "model_overfit":      "Surapprentissage modèle",
        "regime_blindness":   "Cécité de régime",
    }
    label = pat_labels.get(pattern, pattern.replace("_", " "))
    return (
        f"{label} — précision signal {a.signal_accuracy_score:.2f} "
        f"— alpha potentiel {a.alpha_generation_potential:.2f} "
        f"— latence exécution {a.execution_latency_score:.2f} "
        f"— composite {round(comp)}"
    )


def _alpha_decay_index(comp: float, signal_accuracy: float) -> float:
    return round(min(comp / 100 * (1 - signal_accuracy + 0.01) * 10, 10.0), 2)


# ─── Engine ───────────────────────────────────────────────────────────────────

class PredictiveArbitrageEngine:

    def assess_batch(self, inputs: List[ArbitrageInput]) -> List[ArbitrageResult]:
        results = []
        for a in inputs:
            sq  = _signal_quality_score(a)
            ac  = _alpha_capture_score(a)
            ex  = _execution_score(a)
            res = _resilience_score(a)
            comp    = _composite(sq, ac, ex, res)
            risk    = _risk(comp)
            pat     = _pattern(a)
            sev     = _severity(comp)
            act     = _action(risk, pat)
            sig     = _signal_text(a, pat, comp)
            adi     = _alpha_decay_index(comp, a.signal_accuracy_score)
            alert   = comp >= 40 or a.signal_accuracy_score <= 0.40 or a.overfitting_risk >= 0.60
            results.append(ArbitrageResult(
                signal_id=signal_id_val(a),
                signal_type=a.signal_type,
                region=a.region,
                signal_quality_score=sq,
                alpha_capture_score=ac,
                execution_score=ex,
                resilience_score=res,
                arbitrage_composite=comp,
                arbitrage_risk=risk,
                arbitrage_pattern=pat,
                arbitrage_severity=sev,
                recommended_action=act,
                arbitrage_signal=sig,
                avg_estimated_alpha_decay_index=adi,
                has_active_alert=alert,
            ))
        return results

    def summary(self, results: List[ArbitrageResult]) -> Dict[str, Any]:
        # exactly 13 keys
        n = len(results) or 1
        risk_counts:     Dict[str, int] = {}
        pattern_counts:  Dict[str, int] = {}
        severity_counts: Dict[str, int] = {}
        action_counts:   Dict[str, int] = {}
        t_sq = t_ac = t_ex = t_res = t_comp = t_adi = 0.0
        alert_count = 0
        transform_count = 0
        for r in results:
            risk_counts[r.arbitrage_risk]         = risk_counts.get(r.arbitrage_risk, 0) + 1
            pattern_counts[r.arbitrage_pattern]   = pattern_counts.get(r.arbitrage_pattern, 0) + 1
            severity_counts[r.arbitrage_severity] = severity_counts.get(r.arbitrage_severity, 0) + 1
            action_counts[r.recommended_action]   = action_counts.get(r.recommended_action, 0) + 1
            t_sq   += r.signal_quality_score
            t_ac   += r.alpha_capture_score
            t_ex   += r.execution_score
            t_res  += r.resilience_score
            t_comp += r.arbitrage_composite
            t_adi  += r.avg_estimated_alpha_decay_index
            if r.has_active_alert:
                alert_count += 1
            if r.recommended_action not in ("no_action", "performance_monitoring"):
                transform_count += 1
        return {
            "total":                            len(results),
            "risk_counts":                      risk_counts,
            "pattern_counts":                   pattern_counts,
            "severity_counts":                  severity_counts,
            "action_counts":                    action_counts,
            "avg_arbitrage_composite":          round(t_comp / n, 1),
            "alert_count":                      alert_count,
            "transformation_required_count":    transform_count,
            "avg_signal_quality_score":         round(t_sq / n, 1),
            "avg_alpha_capture_score":          round(t_ac / n, 1),
            "avg_execution_score":              round(t_ex / n, 1),
            "avg_resilience_score":             round(t_res / n, 1),
            "avg_estimated_alpha_decay_index":  round(t_adi / n, 2),
        }


def signal_id_val(a: ArbitrageInput) -> str:
    return a.signal_id


if __name__ == "__main__":
    from swarm.intelligence.predictive_arbitrage_engine import (
        ArbitrageInput, PredictiveArbitrageEngine,
    )
    MOCK = [
        ArbitrageInput(signal_id="ARB-001", signal_type="price_momentum", region="EMEA",
            signal_accuracy_score=0.18, model_confidence=0.22, backtesting_sharpe_ratio=0.15,
            alpha_generation_potential=0.20, drawdown_risk=0.80, execution_latency_score=0.25,
            market_impact_cost=0.30, signal_decay_rate=0.75, feature_engineering_score=0.20,
            ensemble_model_diversity=0.18, data_quality_score=0.22, regime_adaptability=0.20,
            overfitting_risk=0.72, transaction_cost_efficiency=0.20, real_time_processing_capability=0.22,
            risk_adjusted_return_estimate=0.18, portfolio_diversification_benefit=0.20),
    ]
    engine = PredictiveArbitrageEngine()
    results = engine.assess_batch(MOCK)
    for r in results:
        d = r.to_dict()
        assert len(d) == 15, f"Expected 15 keys, got {len(d)}"
        print(f"{r.signal_id} | {r.arbitrage_risk:8s} | composite={r.arbitrage_composite}")
    s = engine.summary(results)
    assert len(s) == 13, f"Expected 13 keys, got {len(s)}"
    print("Summary:", s)
