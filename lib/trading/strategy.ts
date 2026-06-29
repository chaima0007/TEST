// Stratégie de day trading « Momentum VWAP / EMA ».
//
// Logique (intraday, sans position overnight) :
//   • Tendance      : EMA rapide vs EMA lente (croisement).
//   • Confirmation  : prix au-dessus/en-dessous du VWAP de la séance.
//   • Momentum      : RSI dans une zone saine (ni surachat ni survente extrême).
//   • Risque        : stop-loss et take-profit dérivés de l'ATR (volatilité).
//
// La stratégie est volontairement simple et transparente : chaque condition est
// explicable. Elle sert de base pédagogique, à backtester avant tout usage réel.

import type { Candle, Signal, StrategyParams } from "./types";
import { ema, rsi, atr, vwap } from "./indicators";

export const DEFAULT_PARAMS: StrategyParams = {
  emaFast: 9,
  emaSlow: 21,
  rsiPeriod: 14,
  atrPeriod: 14,
  rsiLongMin: 50,
  rsiLongMax: 72,
  rsiShortMax: 48,
  atrStopMult: 1.5,
  atrTargetMult: 2.5,
};

/** Série complète des indicateurs (utile pour le backtest et les graphiques). */
export interface IndicatorSeries {
  emaFast: number[];
  emaSlow: number[];
  rsi: number[];
  atr: number[];
  vwap: number[];
}

export function computeIndicators(
  candles: Candle[],
  params: StrategyParams = DEFAULT_PARAMS,
): IndicatorSeries {
  const close = candles.map((c) => c.close);
  return {
    emaFast: ema(close, params.emaFast),
    emaSlow: ema(close, params.emaSlow),
    rsi: rsi(close, params.rsiPeriod),
    atr: atr(candles, params.atrPeriod),
    vwap: vwap(candles),
  };
}

/**
 * Évalue les conditions de la stratégie à l'indice `i` et renvoie la position
 * souhaitée (`long` / `short` / `flat`) accompagnée d'un score de confiance.
 * Exporté pour être réutilisé par le moteur de backtest.
 */
export function evaluateAt(
  ind: IndicatorSeries,
  candles: Candle[],
  i: number,
  params: StrategyParams = DEFAULT_PARAMS,
): { side: "long" | "short" | "flat"; confidence: number; reason: string } {
  if (i < 1) return { side: "flat", confidence: 0, reason: "Données insuffisantes" };

  const price = candles[i].close;
  const fast = ind.emaFast[i];
  const slow = ind.emaSlow[i];
  const fastPrev = ind.emaFast[i - 1];
  const slowPrev = ind.emaSlow[i - 1];
  const r = ind.rsi[i];
  const vw = ind.vwap[i];

  if ([fast, slow, fastPrev, slowPrev, r, vw].some((v) => Number.isNaN(v))) {
    return { side: "flat", confidence: 0, reason: "Indicateurs en chauffe" };
  }

  const crossUp = fastPrev <= slowPrev && fast > slow;
  const crossDown = fastPrev >= slowPrev && fast < slow;
  const trendUp = fast > slow;
  const trendDown = fast < slow;
  const aboveVwap = price > vw;
  const belowVwap = price < vw;

  // ── Conditions LONG ──
  if (trendUp && aboveVwap && r >= params.rsiLongMin && r <= params.rsiLongMax) {
    let conf = 0.5;
    if (crossUp) conf += 0.25; // croisement frais = signal plus fort
    if (r >= 55 && r <= 65) conf += 0.15; // momentum idéal
    conf += Math.min(0.1, (price - vw) / vw); // distance au VWAP
    return {
      side: "long",
      confidence: Math.min(1, conf),
      reason: `EMA${params.emaFast}>EMA${params.emaSlow}, prix>VWAP, RSI ${r.toFixed(0)}${crossUp ? " (croisement haussier)" : ""}`,
    };
  }

  // ── Conditions SHORT ──
  if (trendDown && belowVwap && r <= params.rsiShortMax) {
    let conf = 0.5;
    if (crossDown) conf += 0.25;
    if (r >= 30 && r <= 45) conf += 0.15;
    conf += Math.min(0.1, (vw - price) / vw);
    return {
      side: "short",
      confidence: Math.min(1, conf),
      reason: `EMA${params.emaFast}<EMA${params.emaSlow}, prix<VWAP, RSI ${r.toFixed(0)}${crossDown ? " (croisement baissier)" : ""}`,
    };
  }

  return {
    side: "flat",
    confidence: 0,
    reason: "Aucune confluence (tendance / VWAP / RSI non alignés)",
  };
}

/**
 * Produit le signal courant à partir des bougies les plus récentes.
 * C'est le point d'entrée appelé par l'API et le bot.
 */
export function generateSignal(
  symbol: string,
  candles: Candle[],
  params: StrategyParams = DEFAULT_PARAMS,
): Signal {
  const ind = computeIndicators(candles, params);
  const i = candles.length - 1;
  const last = candles[i];
  const { side, confidence, reason } = evaluateAt(ind, candles, i, params);

  const atrVal = ind.atr[i];
  let stopLoss: number | null = null;
  let takeProfit: number | null = null;
  if (!Number.isNaN(atrVal)) {
    if (side === "long") {
      stopLoss = last.close - params.atrStopMult * atrVal;
      takeProfit = last.close + params.atrTargetMult * atrVal;
    } else if (side === "short") {
      stopLoss = last.close + params.atrStopMult * atrVal;
      takeProfit = last.close - params.atrTargetMult * atrVal;
    }
  }

  const action = side === "long" ? "buy" : side === "short" ? "sell" : "hold";

  return {
    symbol,
    time: last.time,
    price: last.close,
    side,
    action,
    stopLoss,
    takeProfit,
    confidence,
    reason,
    indicators: {
      emaFast: round(ind.emaFast[i]),
      emaSlow: round(ind.emaSlow[i]),
      vwap: round(ind.vwap[i]),
      rsi: round(ind.rsi[i]),
      atr: round(ind.atr[i]),
    },
  };
}

/** Taille de position basée sur le risque : risque € / (entrée − stop). */
export function positionSize(
  capital: number,
  riskPerTradePct: number,
  entry: number,
  stopLoss: number,
): number {
  const riskPerShare = Math.abs(entry - stopLoss);
  if (riskPerShare <= 0) return 0;
  const riskBudget = capital * (riskPerTradePct / 100);
  return Math.max(0, Math.floor(riskBudget / riskPerShare));
}

function round(v: number): number {
  return Number.isNaN(v) ? NaN : Math.round(v * 1000) / 1000;
}
