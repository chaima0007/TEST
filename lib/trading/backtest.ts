// Moteur de backtest pour la stratégie de day trading.
// Simule l'exécution bougie par bougie avec stop-loss / take-profit ATR,
// sortie sur signal inverse et clôture forcée en fin de séance (flat overnight).

import type { Candle, BacktestResult, BacktestTrade, StrategyParams } from "./types";
import { computeIndicators, evaluateAt, DEFAULT_PARAMS } from "./strategy";

interface OpenPosition {
  side: "long" | "short";
  entryTime: number;
  entryPrice: number;
  stop: number;
  target: number;
}

/** Vrai si deux horodatages tombent un jour calendaire différent. */
function isNewDay(a: number, b: number): boolean {
  return new Date(a).toISOString().slice(0, 10) !== new Date(b).toISOString().slice(0, 10);
}

export function backtest(
  symbol: string,
  candles: Candle[],
  params: StrategyParams = DEFAULT_PARAMS,
  opts: { feePct?: number } = {},
): BacktestResult {
  const feePct = opts.feePct ?? 0.02; // frais + slippage par côté (%)
  const ind = computeIndicators(candles, params);
  const trades: BacktestTrade[] = [];

  let equity = 1; // capital normalisé (1 = 100%)
  const equityCurve: { time: number; equity: number }[] = [];
  let pos: OpenPosition | null = null;

  const close = (exitPrice: number, exitTime: number, reason: BacktestTrade["exitReason"]) => {
    if (!pos) return;
    const gross = pos.side === "long" ? exitPrice / pos.entryPrice - 1 : 1 - exitPrice / pos.entryPrice;
    const net = gross - (feePct / 100) * 2; // entrée + sortie
    trades.push({
      side: pos.side,
      entryTime: pos.entryTime,
      entryPrice: pos.entryPrice,
      exitTime,
      exitPrice,
      returnPct: net * 100,
      exitReason: reason,
    });
    equity *= 1 + net;
    pos = null;
  };

  for (let i = 1; i < candles.length; i++) {
    const c = candles[i];

    // Clôture forcée au changement de séance (pas de position overnight).
    if (pos && isNewDay(candles[i - 1].time, c.time)) {
      close(candles[i - 1].close, candles[i - 1].time, "eod");
    }

    // Gestion d'une position ouverte : stop / take-profit intra-bougie.
    if (pos) {
      if (pos.side === "long") {
        if (c.low <= pos.stop) close(pos.stop, c.time, "stop");
        else if (c.high >= pos.target) close(pos.target, c.time, "target");
      } else {
        if (c.high >= pos.stop) close(pos.stop, c.time, "stop");
        else if (c.low <= pos.target) close(pos.target, c.time, "target");
      }
    }

    const { side } = evaluateAt(ind, candles, i, params);

    // Sortie sur signal inverse.
    if (pos && ((pos.side === "long" && side !== "long") || (pos.side === "short" && side !== "short"))) {
      close(c.close, c.time, "signal");
    }

    // Entrée si pas de position et signal directionnel.
    if (!pos && (side === "long" || side === "short")) {
      const atrVal = ind.atr[i];
      if (!Number.isNaN(atrVal)) {
        const entry = c.close;
        pos =
          side === "long"
            ? { side, entryTime: c.time, entryPrice: entry, stop: entry - params.atrStopMult * atrVal, target: entry + params.atrTargetMult * atrVal }
            : { side, entryTime: c.time, entryPrice: entry, stop: entry + params.atrStopMult * atrVal, target: entry - params.atrTargetMult * atrVal };
      }
    }

    equityCurve.push({ time: c.time, equity });
  }

  // Liquidation finale.
  if (pos) close(candles.at(-1)!.close, candles.at(-1)!.time, "eod");

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
    winRate: trades.length ? (wins.length / trades.length) * 100 : 0,
    totalReturnPct: round2(totalReturn),
    avgReturnPct: trades.length ? round2(trades.reduce((s, t) => s + t.returnPct, 0) / trades.length) : 0,
    maxDrawdownPct: round2(maxDD * 100),
    profitFactor: grossLoss > 0 ? round2(grossWin / grossLoss) : grossWin > 0 ? Infinity : 0,
  };
}

function round2(v: number): number {
  return Math.round(v * 100) / 100;
}
