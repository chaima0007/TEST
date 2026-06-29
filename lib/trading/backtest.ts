// Moteur de backtest pour la stratégie de day trading.
//
// Gestion de position avancée, simulée bougie par bougie :
//   • Stop initial ATR + objectif final (TP2).
//   • Prise partielle au TP1 (1R) puis passage du stop au point d'entrée (break-even).
//   • Stop suiveur « chandelier » (ATR) sur le reliquat une fois en profit.
//   • Sortie sur signal inverse, clôture forcée en fin de séance (flat overnight).
//   • Garde-fous journaliers : nombre de trades/jour, limite de perte (en R),
//     pas de nouvelle entrée dans les N dernières bougies de la séance.

import type { Candle, BacktestResult, BacktestTrade, StrategyParams, RiskParams } from "./types";
import { computeIndicators, evaluateAt, DEFAULT_PARAMS, DEFAULT_RISK } from "./strategy";

interface OpenPosition {
  side: "long" | "short";
  entryTime: number;
  entryPrice: number;
  /** Risque initial par unité (|entrée − stop initial|), sert d'unité « R ». */
  rUnit: number;
  stop: number;
  tp1: number;
  tp2: number;
  /** Fraction de position encore ouverte (1 → 0). */
  remaining: number;
  tookPartial: boolean;
  /** Extrême atteint depuis l'entrée (pour le stop suiveur). */
  extreme: number;
  /** Rendement déjà réalisé (fraction, pondéré par la part clôturée). */
  realized: number;
  partial?: { price: number; portion: number; returnPct: number };
}

const dayOf = (t: number) => new Date(t).toISOString().slice(0, 10);

/** Pré-calcule, pour chaque bougie, le nombre de bougies restantes dans sa séance. */
function barsToDayEnd(candles: Candle[]): number[] {
  const out = new Array(candles.length).fill(0);
  let lastIdxOfDay = candles.length - 1;
  for (let i = candles.length - 1; i >= 0; i--) {
    if (i < candles.length - 1 && dayOf(candles[i].time) !== dayOf(candles[i + 1].time)) {
      lastIdxOfDay = i;
    }
    out[i] = lastIdxOfDay - i;
  }
  return out;
}

export function backtest(
  symbol: string,
  candles: Candle[],
  params: StrategyParams = DEFAULT_PARAMS,
  risk: RiskParams = DEFAULT_RISK,
): BacktestResult {
  const feePct = risk.feePct;
  const fee = (feePct / 100) * 2; // aller-retour approximatif par portion
  const ind = computeIndicators(candles, params);
  const toDayEnd = barsToDayEnd(candles);
  const trades: BacktestTrade[] = [];

  let equity = 1; // capital normalisé (1 = 100%)
  const equityCurve: { time: number; equity: number }[] = [];
  let pos: OpenPosition | null = null;

  // Suivi journalier pour les garde-fous.
  let curDay = "";
  let tradesToday = 0;
  let rToday = 0;

  const grossReturn = (side: "long" | "short", entry: number, exit: number) =>
    side === "long" ? exit / entry - 1 : 1 - exit / entry;

  /** Clôture le reliquat de la position et enregistre le trade complet. */
  const closeRemainder = (exitPrice: number, exitTime: number, reason: BacktestTrade["exitReason"]) => {
    if (!pos) return;
    const portion = pos.remaining;
    const net = grossReturn(pos.side, pos.entryPrice, exitPrice) - fee;
    const contribution = net * portion;
    equity *= 1 + contribution;

    const totalReturnPct = (pos.realized + contribution) * 100;
    rToday += pos.rUnit > 0 ? (pos.side === "long" ? exitPrice - pos.entryPrice : pos.entryPrice - exitPrice) / pos.rUnit * portion : 0;

    trades.push({
      side: pos.side,
      entryTime: pos.entryTime,
      entryPrice: pos.entryPrice,
      exitTime,
      exitPrice,
      returnPct: round2(totalReturnPct),
      exitReason: reason,
      partial: pos.partial,
    });
    pos = null;
  };

  for (let i = 1; i < candles.length; i++) {
    const c = candles[i];

    // Réinitialisation des compteurs au changement de séance.
    if (dayOf(c.time) !== curDay) {
      curDay = dayOf(c.time);
      tradesToday = 0;
      rToday = 0;
    }

    // Clôture forcée à la dernière bougie de la veille (pas d'overnight).
    if (pos && dayOf(candles[i - 1].time) !== dayOf(c.time)) {
      closeRemainder(candles[i - 1].close, candles[i - 1].time, "eod");
    }

    // ── Gestion d'une position ouverte ──
    if (pos) {
      const long = pos.side === "long";
      pos.extreme = long ? Math.max(pos.extreme, c.high) : Math.min(pos.extreme, c.low);

      // 1) Stop touché → on clôture le reliquat.
      const stopHit = long ? c.low <= pos.stop : c.high >= pos.stop;
      if (stopHit) {
        const reason = pos.tookPartial && pos.stop === pos.entryPrice ? "breakeven" : pos.tookPartial ? "trail" : "stop";
        closeRemainder(pos.stop, c.time, reason);
      }

      // 2) TP1 → prise partielle + stop au break-even.
      if (pos && !pos.tookPartial) {
        const tp1Hit = long ? c.high >= pos.tp1 : c.low <= pos.tp1;
        if (tp1Hit) {
          const portion = Math.min(risk.partialExitPct, pos.remaining);
          const net = grossReturn(pos.side, pos.entryPrice, pos.tp1) - fee;
          equity *= 1 + net * portion;
          pos.realized += net * portion;
          pos.remaining -= portion;
          pos.tookPartial = true;
          pos.partial = { price: pos.tp1, portion, returnPct: round2(net * 100) };
          if (risk.breakevenAtR <= risk.tp1RMultiple) pos.stop = pos.entryPrice; // break-even
        }
      }

      // 3) TP2 (objectif final) → clôture du reliquat.
      if (pos) {
        const tp2Hit = long ? c.high >= pos.tp2 : c.low <= pos.tp2;
        if (tp2Hit) closeRemainder(pos.tp2, c.time, "target");
      }

      // 4) Stop suiveur (chandelier) une fois suffisamment en profit.
      if (pos) {
        const atrVal = ind.atr[i];
        const moveR = pos.rUnit > 0 ? (long ? pos.extreme - pos.entryPrice : pos.entryPrice - pos.extreme) / pos.rUnit : 0;
        if (Number.isFinite(atrVal) && moveR >= risk.trailActivateR) {
          const trail = long ? pos.extreme - risk.trailAtrMult * atrVal : pos.extreme + risk.trailAtrMult * atrVal;
          pos.stop = long ? Math.max(pos.stop, trail) : Math.min(pos.stop, trail);
        }
      }
    }

    const ev = evaluateAt(ind, candles, i, params);

    // Sortie sur signal inverse.
    if (pos && ((pos.side === "long" && ev.side !== "long") || (pos.side === "short" && ev.side !== "short"))) {
      closeRemainder(c.close, c.time, "signal");
    }

    // ── Entrée ── (garde-fous : limites journalières, fin de séance)
    const canEnter =
      !pos &&
      (ev.side === "long" || ev.side === "short") &&
      tradesToday < risk.maxTradesPerDay &&
      rToday > -risk.dailyLossLimitR &&
      toDayEnd[i] > risk.noEntryLastBars;

    if (canEnter) {
      const atrVal = ind.atr[i];
      if (Number.isFinite(atrVal)) {
        const entry = c.close;
        const rUnit = params.atrStopMult * atrVal;
        const long = ev.side === "long";
        pos = {
          side: ev.side as "long" | "short",
          entryTime: c.time,
          entryPrice: entry,
          rUnit,
          stop: long ? entry - rUnit : entry + rUnit,
          tp1: long ? entry + risk.tp1RMultiple * rUnit : entry - risk.tp1RMultiple * rUnit,
          tp2: long ? entry + params.atrTargetMult * atrVal : entry - params.atrTargetMult * atrVal,
          remaining: 1,
          tookPartial: false,
          extreme: entry,
          realized: 0,
        };
        tradesToday++;
      }
    }

    equityCurve.push({ time: c.time, equity });
  }

  // Liquidation finale.
  if (pos) closeRemainder(candles.at(-1)!.close, candles.at(-1)!.time, "eod");

  return { symbol, trades, equityCurve, metrics: computeMetrics(trades, equityCurve) };
}

function computeMetrics(trades: BacktestTrade[], curve: { time: number; equity: number }[]): BacktestResult["metrics"] {
  const wins = trades.filter((t) => t.returnPct > 0);
  const losses = trades.filter((t) => t.returnPct <= 0);
  const grossWin = wins.reduce((s, t) => s + t.returnPct, 0);
  const grossLoss = Math.abs(losses.reduce((s, t) => s + t.returnPct, 0));

  let peak = curve.length ? curve[0].equity : 1;
  let maxDD = 0;
  for (const p of curve) {
    if (p.equity > peak) peak = p.equity;
    const dd = (peak - p.equity) / peak;
    if (dd > maxDD) maxDD = dd;
  }

  const totalReturn = curve.length ? (curve.at(-1)!.equity - 1) * 100 : 0;

  return {
    trades: trades.length,
    wins: wins.length,
    losses: losses.length,
    winRate: trades.length ? round2((wins.length / trades.length) * 100) : 0,
    totalReturnPct: round2(totalReturn),
    avgReturnPct: trades.length ? round2(trades.reduce((s, t) => s + t.returnPct, 0) / trades.length) : 0,
    maxDrawdownPct: round2(maxDD * 100),
    profitFactor: grossLoss > 0 ? round2(grossWin / grossLoss) : grossWin > 0 ? Infinity : 0,
  };
}

function round2(v: number): number {
  return Math.round(v * 100) / 100;
}
