// Récupération des données de marché depuis l'API publique Yahoo Finance.
// Endpoint "chart" : aucune clé requise. Renvoie des bougies OHLCV.

import type { Candle, Interval, Range } from "./types";

const BASE = "https://query1.finance.yahoo.com/v8/finance/chart";

interface YahooChartResponse {
  chart: {
    result?: Array<{
      meta: {
        symbol: string;
        regularMarketPrice: number;
        currency: string;
        exchangeName: string;
      };
      timestamp?: number[];
      indicators: {
        quote: Array<{
          open: (number | null)[];
          high: (number | null)[];
          low: (number | null)[];
          close: (number | null)[];
          volume: (number | null)[];
        }>;
      };
    }>;
    error?: { code: string; description: string } | null;
  };
}

export interface MarketData {
  symbol: string;
  currency: string;
  exchange: string;
  lastPrice: number;
  candles: Candle[];
}

/**
 * Télécharge les bougies intraday d'un symbole (ex: "AAPL", "BTC-USD", "MC.PA").
 * @param symbol  Ticker Yahoo Finance.
 * @param interval Granularité des bougies (par défaut 5m, adaptée au day trading).
 * @param range   Profondeur d'historique (par défaut 5d).
 */
export async function fetchMarketData(
  symbol: string,
  interval: Interval = "5m",
  range: Range = "5d",
): Promise<MarketData> {
  const url = `${BASE}/${encodeURIComponent(symbol)}?interval=${interval}&range=${range}&includePrePost=false`;

  const res = await fetch(url, {
    headers: {
      // Yahoo refuse les requêtes sans User-Agent de navigateur.
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
      Accept: "application/json",
    },
    // Données fraîches mais on autorise un cache court côté serveur Next.
    next: { revalidate: 30 },
  });

  if (!res.ok) {
    throw new Error(`Yahoo Finance a renvoyé ${res.status} pour ${symbol}`);
  }

  const data = (await res.json()) as YahooChartResponse;
  if (data.chart.error) {
    throw new Error(`Yahoo Finance: ${data.chart.error.description}`);
  }

  const result = data.chart.result?.[0];
  if (!result || !result.timestamp) {
    throw new Error(`Aucune donnée pour le symbole "${symbol}"`);
  }

  const q = result.indicators.quote[0];
  const candles: Candle[] = [];
  for (let i = 0; i < result.timestamp.length; i++) {
    const open = q.open[i];
    const high = q.high[i];
    const low = q.low[i];
    const close = q.close[i];
    const volume = q.volume[i];
    // Yahoo insère parfois des trous (null) — on les ignore.
    if (open == null || high == null || low == null || close == null) continue;
    candles.push({
      time: result.timestamp[i] * 1000,
      open,
      high,
      low,
      close,
      volume: volume ?? 0,
    });
  }

  return {
    symbol: result.meta.symbol,
    currency: result.meta.currency,
    exchange: result.meta.exchangeName,
    lastPrice: result.meta.regularMarketPrice ?? candles.at(-1)?.close ?? 0,
    candles,
  };
}
