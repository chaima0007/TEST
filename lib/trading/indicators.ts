// Indicateurs techniques utilisés par la stratégie de day trading.
// Toutes les fonctions renvoient un tableau aligné sur l'entrée
// (valeurs `NaN` tant que la période de chauffe n'est pas atteinte).

import type { Candle } from "./types";

/** Moyenne mobile simple. */
export function sma(values: number[], period: number): number[] {
  const out: number[] = new Array(values.length).fill(NaN);
  let sum = 0;
  for (let i = 0; i < values.length; i++) {
    sum += values[i];
    if (i >= period) sum -= values[i - period];
    if (i >= period - 1) out[i] = sum / period;
  }
  return out;
}

/** Moyenne mobile exponentielle. Amorcée par la SMA de la première fenêtre. */
export function ema(values: number[], period: number): number[] {
  const out: number[] = new Array(values.length).fill(NaN);
  if (values.length < period) return out;
  const k = 2 / (period + 1);
  let prev = 0;
  for (let i = 0; i < period; i++) prev += values[i];
  prev /= period;
  out[period - 1] = prev;
  for (let i = period; i < values.length; i++) {
    prev = values[i] * k + prev * (1 - k);
    out[i] = prev;
  }
  return out;
}

/** RSI de Wilder. */
export function rsi(values: number[], period = 14): number[] {
  const out: number[] = new Array(values.length).fill(NaN);
  if (values.length <= period) return out;
  let gain = 0;
  let loss = 0;
  for (let i = 1; i <= period; i++) {
    const diff = values[i] - values[i - 1];
    if (diff >= 0) gain += diff;
    else loss -= diff;
  }
  let avgGain = gain / period;
  let avgLoss = loss / period;
  out[period] = avgLoss === 0 ? 100 : 100 - 100 / (1 + avgGain / avgLoss);
  for (let i = period + 1; i < values.length; i++) {
    const diff = values[i] - values[i - 1];
    const g = diff > 0 ? diff : 0;
    const l = diff < 0 ? -diff : 0;
    avgGain = (avgGain * (period - 1) + g) / period;
    avgLoss = (avgLoss * (period - 1) + l) / period;
    out[i] = avgLoss === 0 ? 100 : 100 - 100 / (1 + avgGain / avgLoss);
  }
  return out;
}

/** ATR de Wilder (Average True Range) — mesure de volatilité. */
export function atr(candles: Candle[], period = 14): number[] {
  const out: number[] = new Array(candles.length).fill(NaN);
  if (candles.length <= period) return out;
  const tr: number[] = new Array(candles.length).fill(NaN);
  tr[0] = candles[0].high - candles[0].low;
  for (let i = 1; i < candles.length; i++) {
    const h = candles[i].high;
    const l = candles[i].low;
    const pc = candles[i - 1].close;
    tr[i] = Math.max(h - l, Math.abs(h - pc), Math.abs(l - pc));
  }
  let sum = 0;
  for (let i = 1; i <= period; i++) sum += tr[i];
  let prev = sum / period;
  out[period] = prev;
  for (let i = period + 1; i < candles.length; i++) {
    prev = (prev * (period - 1) + tr[i]) / period;
    out[i] = prev;
  }
  return out;
}

/** EMA amorcée au premier indice non-NaN (utile sur des séries dérivées). */
function emaFromValid(values: number[], period: number): number[] {
  const start = values.findIndex((v) => Number.isFinite(v));
  if (start < 0) return new Array(values.length).fill(NaN);
  const e = ema(values.slice(start), period);
  const out: number[] = new Array(values.length).fill(NaN);
  for (let i = 0; i < e.length; i++) out[start + i] = e[i];
  return out;
}

/** MACD : ligne MACD, ligne de signal et histogramme. */
export function macd(
  values: number[],
  fast = 12,
  slow = 26,
  signalPeriod = 9,
): { macd: number[]; signal: number[]; hist: number[] } {
  const emaFast = ema(values, fast);
  const emaSlow = ema(values, slow);
  const line = values.map((_, i) =>
    Number.isFinite(emaFast[i]) && Number.isFinite(emaSlow[i]) ? emaFast[i] - emaSlow[i] : NaN,
  );
  const signal = emaFromValid(line, signalPeriod);
  const hist = line.map((v, i) => (Number.isFinite(v) && Number.isFinite(signal[i]) ? v - signal[i] : NaN));
  return { macd: line, signal, hist };
}

/** Bandes de Bollinger (moyenne ± mult × écart-type). */
export function bollinger(
  values: number[],
  period = 20,
  mult = 2,
): { middle: number[]; upper: number[]; lower: number[]; bandwidth: number[] } {
  const middle = sma(values, period);
  const upper: number[] = new Array(values.length).fill(NaN);
  const lower: number[] = new Array(values.length).fill(NaN);
  const bandwidth: number[] = new Array(values.length).fill(NaN);
  for (let i = period - 1; i < values.length; i++) {
    const m = middle[i];
    let sq = 0;
    for (let j = i - period + 1; j <= i; j++) sq += (values[j] - m) ** 2;
    const sd = Math.sqrt(sq / period);
    upper[i] = m + mult * sd;
    lower[i] = m - mult * sd;
    bandwidth[i] = m !== 0 ? ((upper[i] - lower[i]) / m) * 100 : NaN;
  }
  return { middle, upper, lower, bandwidth };
}

/**
 * ADX de Wilder + indicateurs directionnels (+DI / -DI).
 * ADX mesure la FORCE de la tendance (pas sa direction) : sous ~20 le marché
 * est sans tendance (range), zone à éviter pour une stratégie de momentum.
 */
export function adx(
  candles: Candle[],
  period = 14,
): { adx: number[]; plusDI: number[]; minusDI: number[] } {
  const n = candles.length;
  const out = { adx: new Array(n).fill(NaN), plusDI: new Array(n).fill(NaN), minusDI: new Array(n).fill(NaN) };
  if (n <= period * 2) return out;

  const tr = new Array(n).fill(0);
  const plusDM = new Array(n).fill(0);
  const minusDM = new Array(n).fill(0);
  for (let i = 1; i < n; i++) {
    const up = candles[i].high - candles[i - 1].high;
    const down = candles[i - 1].low - candles[i].low;
    plusDM[i] = up > down && up > 0 ? up : 0;
    minusDM[i] = down > up && down > 0 ? down : 0;
    const h = candles[i].high;
    const l = candles[i].low;
    const pc = candles[i - 1].close;
    tr[i] = Math.max(h - l, Math.abs(h - pc), Math.abs(l - pc));
  }

  // Sommes lissées de Wilder.
  let trS = 0;
  let pS = 0;
  let mS = 0;
  for (let i = 1; i <= period; i++) {
    trS += tr[i];
    pS += plusDM[i];
    mS += minusDM[i];
  }
  const dx: number[] = new Array(n).fill(NaN);
  for (let i = period + 1; i < n; i++) {
    trS = trS - trS / period + tr[i];
    pS = pS - pS / period + plusDM[i];
    mS = mS - mS / period + minusDM[i];
    const pDI = trS ? (100 * pS) / trS : 0;
    const mDI = trS ? (100 * mS) / trS : 0;
    out.plusDI[i] = pDI;
    out.minusDI[i] = mDI;
    const sum = pDI + mDI;
    dx[i] = sum ? (100 * Math.abs(pDI - mDI)) / sum : 0;
  }

  // ADX = lissage de Wilder du DX.
  const firstDx = period + 1;
  let adxSum = 0;
  let count = 0;
  let started = false;
  let prevAdx = 0;
  for (let i = firstDx; i < n; i++) {
    if (!started) {
      adxSum += dx[i];
      count++;
      if (count === period) {
        prevAdx = adxSum / period;
        out.adx[i] = prevAdx;
        started = true;
      }
    } else {
      prevAdx = (prevAdx * (period - 1) + dx[i]) / period;
      out.adx[i] = prevAdx;
    }
  }
  return out;
}

/** Oscillateur stochastique (%K et %D lissé). */
export function stochastic(
  candles: Candle[],
  period = 14,
  smoothD = 3,
): { k: number[]; d: number[] } {
  const n = candles.length;
  const k: number[] = new Array(n).fill(NaN);
  for (let i = period - 1; i < n; i++) {
    let hh = -Infinity;
    let ll = Infinity;
    for (let j = i - period + 1; j <= i; j++) {
      if (candles[j].high > hh) hh = candles[j].high;
      if (candles[j].low < ll) ll = candles[j].low;
    }
    k[i] = hh > ll ? (100 * (candles[i].close - ll)) / (hh - ll) : 50;
  }
  const d = sma(k.map((v) => (Number.isFinite(v) ? v : 0)), smoothD).map((v, i) =>
    Number.isFinite(k[i - smoothD + 1]) ? v : NaN,
  );
  return { k, d };
}

/** Volume relatif : volume courant / moyenne mobile du volume. */
export function volumeRatio(candles: Candle[], period = 20): number[] {
  const vol = candles.map((c) => c.volume);
  const avg = sma(vol, period);
  return vol.map((v, i) => (Number.isFinite(avg[i]) && avg[i] > 0 ? v / avg[i] : NaN));
}

/**
 * VWAP (Volume Weighted Average Price) cumulé, ré-initialisé à chaque nouvelle
 * journée de bourse — indicateur de référence intraday.
 */
export function vwap(candles: Candle[]): number[] {
  const out: number[] = new Array(candles.length).fill(NaN);
  let cumPV = 0;
  let cumVol = 0;
  let currentDay = "";
  for (let i = 0; i < candles.length; i++) {
    const c = candles[i];
    const day = new Date(c.time).toISOString().slice(0, 10);
    if (day !== currentDay) {
      currentDay = day;
      cumPV = 0;
      cumVol = 0;
    }
    const typical = (c.high + c.low + c.close) / 3;
    cumPV += typical * c.volume;
    cumVol += c.volume;
    out[i] = cumVol > 0 ? cumPV / cumVol : c.close;
  }
  return out;
}
