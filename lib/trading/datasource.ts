// Sélecteur de source de données — interface unique pour la stratégie/API/bot.
//
// Choix du fournisseur via MARKET_DATA_PROVIDER :
//   • "yahoo"  (défaut) — API publique Yahoo Finance, sans clé.
//   • "alpaca"          — Alpaca Market Data (mêmes clés que l'exécution).
//
// En mode yahoo, si l'appel échoue (ex. hôte bloqué par une politique réseau) et
// que des clés Alpaca sont configurées, on bascule automatiquement sur Alpaca.

import type { Interval, Range } from "./types";
import { fetchMarketData, type MarketData } from "./yahoo";
import { fetchAlpacaBars } from "./alpaca-data";
import { hasCredentials } from "./broker";

export type DataProvider = "yahoo" | "alpaca";

export function activeProvider(): DataProvider {
  return (process.env.MARKET_DATA_PROVIDER || "yahoo").toLowerCase() === "alpaca" ? "alpaca" : "yahoo";
}

export async function getMarketData(
  symbol: string,
  interval: Interval = "5m",
  range: Range = "5d",
): Promise<MarketData & { provider: DataProvider }> {
  const provider = activeProvider();

  if (provider === "alpaca") {
    return { ...(await fetchAlpacaBars(symbol, interval, range)), provider: "alpaca" };
  }

  try {
    return { ...(await fetchMarketData(symbol, interval, range)), provider: "yahoo" };
  } catch (err) {
    // Repli automatique sur Alpaca si Yahoo est injoignable et que les clés existent.
    if (hasCredentials()) {
      return { ...(await fetchAlpacaBars(symbol, interval, range)), provider: "alpaca" };
    }
    throw err;
  }
}
