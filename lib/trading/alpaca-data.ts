// Source de données alternative : Alpaca Market Data (actions).
// Même forme de sortie que yahoo.ts (MarketData), interchangeable via datasource.ts.
// Réutilise les clés Alpaca (ALPACA_KEY_ID / ALPACA_SECRET_KEY) — une seule clé
// sert ainsi aux données ET à l'exécution des ordres.

import type { Candle, Interval, Range } from "./types";
import type { MarketData } from "./yahoo";
import { loadConfig, hasCredentials } from "./broker";

const DATA_BASE = "https://data.alpaca.markets/v2/stocks";

const TIMEFRAME: Record<Interval, string> = {
  "1m": "1Min",
  "2m": "2Min",
  "5m": "5Min",
  "15m": "15Min",
  "30m": "30Min",
  "60m": "1Hour",
  "1d": "1Day",
};

const RANGE_DAYS: Record<Range, number> = {
  "1d": 1,
  "5d": 5,
  "1mo": 30,
  "3mo": 90,
  "6mo": 180,
  "1y": 365,
};

interface AlpacaBar {
  t: string; // RFC3339
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
}

interface AlpacaBarsResponse {
  bars: AlpacaBar[] | null;
  symbol: string;
  next_page_token: string | null;
}

/**
 * Télécharge les bougies d'un symbole via Alpaca Market Data.
 * Utilise le flux IEX (gratuit) par défaut ; passez ALPACA_DATA_FEED=sip si vous
 * disposez d'un abonnement aux données consolidées.
 */
export async function fetchAlpacaBars(
  symbol: string,
  interval: Interval = "5m",
  range: Range = "5d",
): Promise<MarketData> {
  const cfg = loadConfig();
  if (!hasCredentials(cfg)) {
    throw new Error(
      "Alpaca Market Data requiert ALPACA_KEY_ID / ALPACA_SECRET_KEY (les mêmes clés que pour l'exécution).",
    );
  }

  const feed = process.env.ALPACA_DATA_FEED || "iex";
  const timeframe = TIMEFRAME[interval];
  const days = RANGE_DAYS[range];
  const start = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();

  const headers = {
    "APCA-API-KEY-ID": cfg.keyId,
    "APCA-API-SECRET-KEY": cfg.secretKey,
    Accept: "application/json",
  };

  const candles: Candle[] = [];
  let pageToken: string | null = null;
  let guard = 0;

  do {
    const params = new URLSearchParams({
      timeframe,
      start,
      limit: "10000",
      adjustment: "raw",
      feed,
    });
    if (pageToken) params.set("page_token", pageToken);

    const res = await fetch(`${DATA_BASE}/${encodeURIComponent(symbol)}/bars?${params}`, { headers });
    if (!res.ok) {
      const body = await res.text();
      throw new Error(`Alpaca Market Data a renvoyé ${res.status} pour ${symbol} : ${body.slice(0, 200)}`);
    }
    const data = (await res.json()) as AlpacaBarsResponse;
    for (const b of data.bars ?? []) {
      candles.push({ time: Date.parse(b.t), open: b.o, high: b.h, low: b.l, close: b.c, volume: b.v });
    }
    pageToken = data.next_page_token;
  } while (pageToken && ++guard < 20);

  if (!candles.length) {
    throw new Error(`Aucune donnée Alpaca pour "${symbol}" (vérifiez le symbole et le flux ${feed}).`);
  }

  return {
    symbol,
    currency: "USD",
    exchange: `Alpaca (${feed})`,
    lastPrice: candles[candles.length - 1].close,
    candles,
  };
}
