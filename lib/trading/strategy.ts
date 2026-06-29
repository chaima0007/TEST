// Stratégie de day trading « Momentum multi-confluences ».
//
// Logique (intraday, sans position overnight) — on n'entre que lorsque plusieurs
// signaux indépendants s'alignent (confluence), et uniquement quand le marché a
// une vraie tendance (filtre ADX) :
//
//   Filtres durs (obligatoires) :
//     • Force de tendance  : ADX ≥ seuil (sinon marché en range → on s'abstient).
//     • Direction de fond  : prix du bon côté de l'EMA de tendance (EMA50).
//     • Tendance court term : EMA rapide vs EMA lente.
//     • VWAP               : prix du bon côté du VWAP de la séance.
//   Confirmations (score de confluence) :
//     • MACD               : histogramme du bon signe / croisement.
//     • RSI                : momentum dans une zone saine.
//     • +DI / -DI          : dominance directionnelle cohérente.
//     • Volume relatif     : participation supérieure à la moyenne.
//     • Stochastique       : pas en zone extrême opposée.
//
//   Risque : stop-loss et objectifs (TP1/TP2) dérivés de l'ATR. La gestion fine
//   de la position (break-even, stop suiveur, prises partielles) est dans
//   backtest.ts (simulation) et exposée via les niveaux du signal.

import type { Candle, Signal, StrategyParams, RiskParams } from "./types";
import { ema, rsi, atr, vwap, macd, bollinger, adx, stochastic, volumeRatio } from "./indicators";

export const DEFAULT_PARAMS: StrategyParams = {
  emaFast: 9,
  emaSlow: 21,
  emaTrend: 50,
  rsiPeriod: 14,
  atrPeriod: 14,
  rsiLongMin: 50,
  rsiLongMax: 72,
  rsiShortMax: 48,
  macdFast: 12,
  macdSlow: 26,
  macdSignal: 9,
  adxPeriod: 14,
  adxMin: 20,
  bbPeriod: 20,
  bbMult: 2,
  stochPeriod: 14,
  volPeriod: 20,
  volMinRatio: 1.0,
  minConfluences: 3,
  atrStopMult: 1.5,
  atrTargetMult: 3,
};

/** Gestion de position par défaut (money management). */
export const DEFAULT_RISK: RiskParams = {
  tp1RMultiple: 1,
  partialExitPct: 0.5,
  breakevenAtR: 1,
  trailActivateR: 1.5,
  trailAtrMult: 2.5,
  maxTradesPerDay: 4,
  dailyLossLimitR: 2,
  noEntryLastBars: 3,
  feePct: 0.02,
};

/** Série complète des indicateurs (utile pour le backtest et les graphiques). */
export interface IndicatorSeries {
  emaFast: number[];
  emaSlow: number[];
  emaTrend: number[];
  rsi: number[];
  atr: number[];
  vwap: number[];
  macd: number[];
  macdSignal: number[];
  macdHist: number[];
  adx: number[];
  plusDI: number[];
  minusDI: number[];
  bbUpper: number[];
  bbLower: number[];
  stochK: number[];
  relVolume: number[];
}

export function computeIndicators(
  candles: Candle[],
  params: StrategyParams = DEFAULT_PARAMS,
): IndicatorSeries {
  const close = candles.map((c) => c.close);
  const m = macd(close, params.macdFast, params.macdSlow, params.macdSignal);
  const bb = bollinger(close, params.bbPeriod, params.bbMult);
  const dx = adx(candles, params.adxPeriod);
  const st = stochastic(candles, params.stochPeriod);
  return {
    emaFast: ema(close, params.emaFast),
    emaSlow: ema(close, params.emaSlow),
    emaTrend: ema(close, params.emaTrend),
    rsi: rsi(close, params.rsiPeriod),
    atr: atr(candles, params.atrPeriod),
    vwap: vwap(candles),
    macd: m.macd,
    macdSignal: m.signal,
    macdHist: m.hist,
    adx: dx.adx,
    plusDI: dx.plusDI,
    minusDI: dx.minusDI,
    bbUpper: bb.upper,
    bbLower: bb.lower,
    stochK: st.k,
    relVolume: volumeRatio(candles, params.volPeriod),
  };
}

export interface Evaluation {
  side: "long" | "short" | "flat";
  confidence: number;
  reason: string;
  passed: number;
  total: number;
}

/**
 * Évalue les conditions à l'indice `i`. Combine des filtres durs (gates) et un
 * score de confluence sur des confirmations indépendantes.
 */
export function evaluateAt(
  ind: IndicatorSeries,
  candles: Candle[],
  i: number,
  params: StrategyParams = DEFAULT_PARAMS,
): Evaluation {
  const flat = (reason: string, passed = 0, total = 5): Evaluation => ({
    side: "flat",
    confidence: 0,
    reason,
    passed,
    total,
  });
  if (i < 1) return flat("Données insuffisantes");

  const price = candles[i].close;
  const fast = ind.emaFast[i];
  const slow = ind.emaSlow[i];
  const trend = ind.emaTrend[i];
  const r = ind.rsi[i];
  const vw = ind.vwap[i];
  const adxV = ind.adx[i];
  const pDI = ind.plusDI[i];
  const mDI = ind.minusDI[i];
  const hist = ind.macdHist[i];
  const histPrev = ind.macdHist[i - 1];
  const stoch = ind.stochK[i];
  const relVol = ind.relVolume[i];

  if ([fast, slow, trend, r, vw, adxV, hist, stoch].some((v) => !Number.isFinite(v))) {
    return flat("Indicateurs en chauffe");
  }

  // ── Filtre dur n°1 : force de tendance. ──
  if (adxV < params.adxMin) {
    return flat(`Marché sans tendance (ADX ${adxV.toFixed(0)} < ${params.adxMin})`);
  }

  const trendUp = fast > slow;
  const trendDown = fast < slow;
  const aboveTrend = price > trend;
  const belowTrend = price < trend;
  const aboveVwap = price > vw;
  const belowVwap = price < vw;

  // ── Direction candidate (filtres durs n°2/3/4). ──
  let dir: "long" | "short" | null = null;
  if (trendUp && aboveTrend && aboveVwap) dir = "long";
  else if (trendDown && belowTrend && belowVwap) dir = "short";
  if (!dir) return flat("Direction non alignée (EMA / tendance / VWAP)");

  // ── Confirmations (score de confluence). ──
  const reasons: string[] = [];
  let passed = 0;
  const total = 5;
  const check = (ok: boolean, label: string) => {
    if (ok) {
      passed++;
      reasons.push(label);
    }
  };

  if (dir === "long") {
    check(hist > 0 || hist > histPrev, "MACD haussier");
    check(r >= params.rsiLongMin && r <= params.rsiLongMax, `RSI ${r.toFixed(0)}`);
    check(pDI > mDI, "+DI>-DI");
    check(Number.isFinite(relVol) && relVol >= params.volMinRatio, "volume soutenu");
    check(stoch < 80, "stoch non suracheté");
  } else {
    check(hist < 0 || hist < histPrev, "MACD baissier");
    check(r <= params.rsiShortMax, `RSI ${r.toFixed(0)}`);
    check(mDI > pDI, "-DI>+DI");
    check(Number.isFinite(relVol) && relVol >= params.volMinRatio, "volume soutenu");
    check(stoch > 20, "stoch non survendu");
  }

  if (passed < params.minConfluences) {
    return {
      side: "flat",
      confidence: 0,
      reason: `Confluence insuffisante (${passed}/${params.minConfluences} requis)`,
      passed,
      total,
    };
  }

  // Confiance : base + part des confirmations + bonus force de tendance.
  const confidence = Math.min(1, 0.4 + (passed / total) * 0.45 + Math.min(0.15, (adxV - params.adxMin) / 100));
  return {
    side: dir,
    confidence,
    reason: `${dir === "long" ? "Haussier" : "Baissier"} · ADX ${adxV.toFixed(0)} · ${reasons.join(", ")}`,
    passed,
    total,
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
  risk: RiskParams = DEFAULT_RISK,
): Signal {
  const ind = computeIndicators(candles, params);
  const i = candles.length - 1;
  const last = candles[i];
  const ev = evaluateAt(ind, candles, i, params);

  const atrVal = ind.atr[i];
  let stopLoss: number | null = null;
  let takeProfit1: number | null = null;
  let takeProfit: number | null = null;
  if (Number.isFinite(atrVal)) {
    const riskDist = params.atrStopMult * atrVal;
    if (ev.side === "long") {
      stopLoss = last.close - riskDist;
      takeProfit1 = last.close + risk.tp1RMultiple * riskDist;
      takeProfit = last.close + params.atrTargetMult * atrVal;
    } else if (ev.side === "short") {
      stopLoss = last.close + riskDist;
      takeProfit1 = last.close - risk.tp1RMultiple * riskDist;
      takeProfit = last.close - params.atrTargetMult * atrVal;
    }
  }

  const action = ev.side === "long" ? "buy" : ev.side === "short" ? "sell" : "hold";

  return {
    symbol,
    time: last.time,
    price: last.close,
    side: ev.side,
    action,
    stopLoss,
    takeProfit1,
    takeProfit,
    confidence: ev.confidence,
    score: { passed: ev.passed, total: ev.total },
    reason: ev.reason,
    indicators: {
      emaFast: round(ind.emaFast[i]),
      emaSlow: round(ind.emaSlow[i]),
      emaTrend: round(ind.emaTrend[i]),
      vwap: round(ind.vwap[i]),
      rsi: round(ind.rsi[i]),
      atr: round(ind.atr[i]),
      macd: round(ind.macd[i]),
      macdSignal: round(ind.macdSignal[i]),
      macdHist: round(ind.macdHist[i]),
      adx: round(ind.adx[i]),
      plusDI: round(ind.plusDI[i]),
      minusDI: round(ind.minusDI[i]),
      bbUpper: round(ind.bbUpper[i]),
      bbLower: round(ind.bbLower[i]),
      stochK: round(ind.stochK[i]),
      relVolume: round(ind.relVolume[i]),
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
  return Number.isFinite(v) ? Math.round(v * 1000) / 1000 : NaN;
}
