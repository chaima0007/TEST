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
  /** Premier objectif (prise partielle). */
  takeProfit1: number | null;
  /** Objectif final / take-profit (si position ouverte). */
  takeProfit: number | null;
  /** Score de confiance 0..1 dérivé de la confluence des indicateurs. */
  confidence: number;
  /** Confluences validées (cases cochées) sur le total évalué. */
  score: { passed: number; total: number };
  /** Explication lisible des conditions déclenchées. */
  reason: string;
  /** Snapshot des indicateurs à la dernière bougie. */
  indicators: {
    emaFast: number;
    emaSlow: number;
    emaTrend: number;
    vwap: number;
    rsi: number;
    atr: number;
    macd: number;
    macdSignal: number;
    macdHist: number;
    adx: number;
    plusDI: number;
    minusDI: number;
    bbUpper: number;
    bbLower: number;
    stochK: number;
    relVolume: number;
  };
}

/** Paramètres de la stratégie (valeurs par défaut dans strategy.ts). */
export interface StrategyParams {
  emaFast: number;
  emaSlow: number;
  /** EMA de tendance long terme (filtre de fond). */
  emaTrend: number;
  rsiPeriod: number;
  atrPeriod: number;
  /** RSI minimal pour valider un long. */
  rsiLongMin: number;
  /** RSI maximal pour éviter d'acheter en surachat. */
  rsiLongMax: number;
  /** RSI maximal pour valider un short. */
  rsiShortMax: number;
  /** Périodes MACD. */
  macdFast: number;
  macdSlow: number;
  macdSignal: number;
  /** Période ADX et seuil minimal de force de tendance. */
  adxPeriod: number;
  adxMin: number;
  /** Bandes de Bollinger. */
  bbPeriod: number;
  bbMult: number;
  /** Stochastique. */
  stochPeriod: number;
  /** Volume relatif minimal pour confirmer une entrée. */
  volPeriod: number;
  volMinRatio: number;
  /** Nombre minimal de confluences pour déclencher un signal. */
  minConfluences: number;
  /** Multiplicateur d'ATR pour le stop-loss. */
  atrStopMult: number;
  /** Multiplicateur d'ATR pour le take-profit final. */
  atrTargetMult: number;
}

/** Paramètres de gestion de position (money & risk management). */
export interface RiskParams {
  /** Premier objectif exprimé en multiple de R (risque initial). */
  tp1RMultiple: number;
  /** Fraction de la position clôturée au TP1 (0..1). */
  partialExitPct: number;
  /** Déplace le stop au point d'entrée après ce multiple de R. */
  breakevenAtR: number;
  /** Active le stop suiveur après ce multiple de R. */
  trailActivateR: number;
  /** Distance du stop suiveur (chandelier) en multiples d'ATR. */
  trailAtrMult: number;
  /** Nombre maximum de trades par jour. */
  maxTradesPerDay: number;
  /** Arrêt des entrées du jour après cette perte cumulée (en R). */
  dailyLossLimitR: number;
  /** Pas de nouvelle entrée dans les N dernières bougies de la séance. */
  noEntryLastBars: number;
  /** Frais + slippage par côté (%). */
  feePct: number;
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
  /** Prix de sortie du reliquat (le partiel éventuel est dans `partial`). */
  exitPrice: number;
  /** Rendement net pondéré de la position (partiel + reliquat), en %. */
  returnPct: number;
  exitReason: "stop" | "target" | "signal" | "eod" | "trail" | "breakeven";
  /** Prise partielle au TP1, si elle a eu lieu. */
  partial?: { price: number; portion: number; returnPct: number };
}
