// Types partagés du module de day trading.

/** Une bougie OHLCV (Open / High / Low / Close / Volume). */
export interface Candle {
  /** Horodatage de début de bougie (ms epoch). */
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

/** Intervalle des bougies supporté par Yahoo Finance pour l'intraday. */
export type Interval = "1m" | "2m" | "5m" | "15m" | "30m" | "60m" | "1d";

/** Période d'historique demandée à Yahoo Finance. */
export type Range = "1d" | "5d" | "1mo" | "3mo" | "6mo" | "1y";

export type Side = "long" | "short" | "flat";
export type Action = "buy" | "sell" | "hold" | "close";

/** Signal produit par la stratégie pour la dernière bougie connue. */
export interface Signal {
  symbol: string;
  time: number;
  /** Prix de référence (close de la dernière bougie). */
  price: number;
  /** Position recommandée. */
  side: Side;
  /** Action concrète à passer au courtier. */
  action: Action;
  /** Niveau de stop-loss recommandé (si position ouverte). */
  stopLoss: number | null;
  /** Niveau de take-profit recommandé (si position ouverte). */
  takeProfit: number | null;
  /** Score de confiance 0..1 dérivé de la confluence des indicateurs. */
  confidence: number;
  /** Explication lisible des conditions déclenchées. */
  reason: string;
  /** Snapshot des indicateurs à la dernière bougie. */
  indicators: {
    emaFast: number;
    emaSlow: number;
    vwap: number;
    rsi: number;
    atr: number;
  };
}

/** Paramètres de la stratégie (valeurs par défaut dans strategy.ts). */
export interface StrategyParams {
  emaFast: number;
  emaSlow: number;
  rsiPeriod: number;
  atrPeriod: number;
  /** RSI minimal pour valider un long. */
  rsiLongMin: number;
  /** RSI maximal pour éviter d'acheter en surachat. */
  rsiLongMax: number;
  /** RSI maximal pour valider un short. */
  rsiShortMax: number;
  /** Multiplicateur d'ATR pour le stop-loss. */
  atrStopMult: number;
  /** Multiplicateur d'ATR pour le take-profit. */
  atrTargetMult: number;
}

/** Résultat d'un backtest. */
export interface BacktestResult {
  symbol: string;
  trades: BacktestTrade[];
  equityCurve: { time: number; equity: number }[];
  metrics: {
    trades: number;
    wins: number;
    losses: number;
    winRate: number;
    totalReturnPct: number;
    avgReturnPct: number;
    maxDrawdownPct: number;
    profitFactor: number;
  };
}

export interface BacktestTrade {
  side: "long" | "short";
  entryTime: number;
  entryPrice: number;
  exitTime: number;
  exitPrice: number;
  returnPct: number;
  exitReason: "stop" | "target" | "signal" | "eod";
}
