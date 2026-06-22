import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_SIGNALS = [
  // ARB-001 price_momentum EMEA — critical, signal_degradation
  { signal_id:"ARB-001", signal_type:"price_momentum",          region:"EMEA",  signal_accuracy_score:0.18, model_confidence:0.22, backtesting_sharpe_ratio:0.15, alpha_generation_potential:0.20, drawdown_risk:0.80, execution_latency_score:0.25, market_impact_cost:0.30, signal_decay_rate:0.75, feature_engineering_score:0.20, ensemble_model_diversity:0.18, data_quality_score:0.22, regime_adaptability:0.20, overfitting_risk:0.72, transaction_cost_efficiency:0.20, real_time_processing_capability:0.22, risk_adjusted_return_estimate:0.18, portfolio_diversification_benefit:0.20 },
  // ARB-002 volatility_spread NAMER — low, optimal
  { signal_id:"ARB-002", signal_type:"volatility_spread",       region:"NAMER", signal_accuracy_score:0.88, model_confidence:0.90, backtesting_sharpe_ratio:0.85, alpha_generation_potential:0.85, drawdown_risk:0.12, execution_latency_score:0.10, market_impact_cost:0.08, signal_decay_rate:0.12, feature_engineering_score:0.88, ensemble_model_diversity:0.85, data_quality_score:0.92, regime_adaptability:0.88, overfitting_risk:0.10, transaction_cost_efficiency:0.90, real_time_processing_capability:0.88, risk_adjusted_return_estimate:0.85, portfolio_diversification_benefit:0.88 },
  // ARB-003 sentiment_divergence APAC — high, alpha_erosion
  { signal_id:"ARB-003", signal_type:"sentiment_divergence",    region:"APAC",  signal_accuracy_score:0.52, model_confidence:0.55, backtesting_sharpe_ratio:0.22, alpha_generation_potential:0.18, drawdown_risk:0.58, execution_latency_score:0.45, market_impact_cost:0.42, signal_decay_rate:0.62, feature_engineering_score:0.50, ensemble_model_diversity:0.48, data_quality_score:0.55, regime_adaptability:0.50, overfitting_risk:0.48, transaction_cost_efficiency:0.52, real_time_processing_capability:0.50, risk_adjusted_return_estimate:0.20, portfolio_diversification_benefit:0.48 },
  // ARB-004 macro_signal LATAM — low, stable
  { signal_id:"ARB-004", signal_type:"macro_signal",            region:"LATAM", signal_accuracy_score:0.82, model_confidence:0.80, backtesting_sharpe_ratio:0.78, alpha_generation_potential:0.80, drawdown_risk:0.18, execution_latency_score:0.12, market_impact_cost:0.15, signal_decay_rate:0.18, feature_engineering_score:0.80, ensemble_model_diversity:0.78, data_quality_score:0.85, regime_adaptability:0.80, overfitting_risk:0.15, transaction_cost_efficiency:0.82, real_time_processing_capability:0.80, risk_adjusted_return_estimate:0.78, portfolio_diversification_benefit:0.80 },
  // ARB-005 cross_asset_correlation EMEA — critical, execution_failure
  { signal_id:"ARB-005", signal_type:"cross_asset_correlation", region:"EMEA",  signal_accuracy_score:0.55, model_confidence:0.52, backtesting_sharpe_ratio:0.48, alpha_generation_potential:0.50, drawdown_risk:0.75, execution_latency_score:0.85, market_impact_cost:0.80, signal_decay_rate:0.60, feature_engineering_score:0.48, ensemble_model_diversity:0.50, data_quality_score:0.55, regime_adaptability:0.45, overfitting_risk:0.55, transaction_cost_efficiency:0.20, real_time_processing_capability:0.18, risk_adjusted_return_estimate:0.48, portfolio_diversification_benefit:0.45 },
  // ARB-006 mean_reversion MEA — moderate, none
  { signal_id:"ARB-006", signal_type:"mean_reversion",          region:"MEA",   signal_accuracy_score:0.65, model_confidence:0.62, backtesting_sharpe_ratio:0.60, alpha_generation_potential:0.62, drawdown_risk:0.38, execution_latency_score:0.35, market_impact_cost:0.38, signal_decay_rate:0.40, feature_engineering_score:0.62, ensemble_model_diversity:0.60, data_quality_score:0.65, regime_adaptability:0.62, overfitting_risk:0.35, transaction_cost_efficiency:0.65, real_time_processing_capability:0.62, risk_adjusted_return_estimate:0.60, portfolio_diversification_benefit:0.62 },
  // ARB-007 liquidity_gap NAMER — high, regime_blindness
  { signal_id:"ARB-007", signal_type:"liquidity_gap",           region:"NAMER", signal_accuracy_score:0.48, model_confidence:0.50, backtesting_sharpe_ratio:0.45, alpha_generation_potential:0.48, drawdown_risk:0.55, execution_latency_score:0.48, market_impact_cost:0.45, signal_decay_rate:0.72, feature_engineering_score:0.45, ensemble_model_diversity:0.48, data_quality_score:0.50, regime_adaptability:0.20, overfitting_risk:0.52, transaction_cost_efficiency:0.48, real_time_processing_capability:0.45, risk_adjusted_return_estimate:0.45, portfolio_diversification_benefit:0.48 },
  // ARB-008 regime_shift APAC — critical, model_overfit
  { signal_id:"ARB-008", signal_type:"regime_shift",            region:"APAC",  signal_accuracy_score:0.28, model_confidence:0.30, backtesting_sharpe_ratio:0.25, alpha_generation_potential:0.28, drawdown_risk:0.82, execution_latency_score:0.35, market_impact_cost:0.30, signal_decay_rate:0.78, feature_engineering_score:0.22, ensemble_model_diversity:0.18, data_quality_score:0.28, regime_adaptability:0.25, overfitting_risk:0.82, transaction_cost_efficiency:0.25, real_time_processing_capability:0.22, risk_adjusted_return_estimate:0.22, portfolio_diversification_benefit:0.20 },
];

type Signal = typeof MOCK_SIGNALS[0];

function signalQualityScore(s: Signal): number {
  const raw =
    (1.0 - s.signal_accuracy_score) * 100 * 0.40 +
    (1.0 - s.model_confidence)       * 100 * 0.35 +
    (1.0 - s.data_quality_score)     * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function alphaCaptureScore(s: Signal): number {
  const raw =
    (1.0 - s.alpha_generation_potential)    * 100 * 0.40 +
    (1.0 - s.backtesting_sharpe_ratio)      * 100 * 0.35 +
    (1.0 - s.risk_adjusted_return_estimate) * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function executionScore(s: Signal): number {
  const raw =
    s.execution_latency_score              * 100 * 0.40 +
    s.market_impact_cost                   * 100 * 0.35 +
    (1.0 - s.transaction_cost_efficiency)  * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function resilienceScore(s: Signal): number {
  const raw =
    (1.0 - s.regime_adaptability)     * 100 * 0.40 +
    (1.0 - s.ensemble_model_diversity) * 100 * 0.35 +
    s.overfitting_risk                 * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}

function composite(sq: number, ac: number, ex: number, res: number): number {
  return Math.min(Math.round((sq * 0.30 + ac * 0.25 + ex * 0.25 + res * 0.20) * 100) / 100, 100);
}

function arbitragePattern(s: Signal): string {
  if (s.signal_accuracy_score <= 0.30 && s.model_confidence <= 0.35)          return "signal_degradation";
  if (s.alpha_generation_potential <= 0.25 && s.backtesting_sharpe_ratio <= 0.30) return "alpha_erosion";
  if (s.execution_latency_score >= 0.70 && s.market_impact_cost >= 0.65)      return "execution_failure";
  if (s.overfitting_risk >= 0.70 && s.ensemble_model_diversity <= 0.30)       return "model_overfit";
  if (s.regime_adaptability <= 0.25 && s.signal_decay_rate >= 0.65)           return "regime_blindness";
  return "none";
}

function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsing"; if (c >= 40) return "degrading"; if (c >= 20) return "stable"; return "optimal"; }

function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "signal_degradation") return "model_rebuild";
    if (p === "execution_failure")  return "execution_overhaul";
    return "alpha_crisis";
  }
  if (r === "high") {
    if (p === "signal_degradation") return "signal_recalibration";
    if (p === "model_overfit")      return "ensemble_retrain";
    return "risk_deleverage";
  }
  if (r === "moderate") return "performance_monitoring";
  return "no_action";
}

function arbitrageSignal(s: Signal, pat: string, comp: number): string {
  if (comp < 20) return "Signal prédictif optimal — qualité élevée, alpha stable, exécution efficiente, modèle robuste";
  const labels: Record<string,string> = {
    signal_degradation: "Dégradation du signal",
    alpha_erosion:      "Érosion de l'alpha",
    execution_failure:  "Défaillance d'exécution",
    model_overfit:      "Surapprentissage modèle",
    regime_blindness:   "Cécité de régime",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — précision signal ${s.signal_accuracy_score.toFixed(2)} — alpha potentiel ${s.alpha_generation_potential.toFixed(2)} — latence exécution ${s.execution_latency_score.toFixed(2)} — composite ${Math.round(comp)}`;
}

function alphaDecayIndex(comp: number, signalAccuracy: number): number {
  return Math.round(Math.min(comp / 100 * (1 - signalAccuracy + 0.01) * 10, 10.0) * 100) / 100;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[predictive-arbitrage-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tsq=0, tac=0, tex=0, tres=0, tcomp=0, tadi=0, alertC=0, transfC=0;
    for (const sig of signals) {
      rc[sig.arbitrage_risk]      = (rc[sig.arbitrage_risk]     || 0) + 1;
      pc[sig.arbitrage_pattern]   = (pc[sig.arbitrage_pattern]  || 0) + 1;
      sc[sig.arbitrage_severity]  = (sc[sig.arbitrage_severity] || 0) + 1;
      ac[sig.recommended_action]  = (ac[sig.recommended_action] || 0) + 1;
      tsq   += sig.signal_quality_score;
      tac   += sig.alpha_capture_score;
      tex   += sig.execution_score;
      tres  += sig.resilience_score;
      tcomp += sig.arbitrage_composite;
      tadi  += sig.avg_estimated_alpha_decay_index;
      if (sig.has_active_alert) alertC++;
      if (sig.recommended_action !== "no_action" && sig.recommended_action !== "performance_monitoring") transfC++;
    }
    const n = signals.length;
    return sealResponse(NextResponse.json(sealResponse({ signals, summary: {
      total:                            n,
      risk_counts:                      rc,
      pattern_counts:                   pc,
      severity_counts:                  sc,
      action_counts:                    ac,
      avg_arbitrage_composite:          Math.round(tcomp / n * 10) / 10,
      alert_count:                      alertC,
      transformation_required_count:    transfC,
      avg_signal_quality_score:         Math.round(tsq  / n * 10) / 10,
      avg_alpha_capture_score:          Math.round(tac  / n * 10) / 10,
      avg_execution_score:              Math.round(tex  / n * 10) / 10,
      avg_resilience_score:             Math.round(tres / n * 10) / 10,
      avg_estimated_alpha_decay_index:  Math.round(tadi / n * 100) / 100,
    } as Record<string, unknown>}, "predictive-arbitrage-engine") as Parameters<typeof NextResponse.json>[0]));
  }
  return sealResponse(NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/predictive-arbitrage-engine`, { next: { revalidate: 30 } })).json(), "predictive-arbitrage-engine") as Parameters<typeof NextResponse.json>[0]));
}
