import { NextRequest, NextResponse } from "next/server";
import { fetchMarketData } from "@/lib/trading/yahoo";
import { backtest } from "@/lib/trading/backtest";
import type { Interval, Range } from "@/lib/trading/types";

// GET /api/trading/backtest?symbol=AAPL&interval=5m&range=1mo&fee=0.02
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const symbol = searchParams.get("symbol")?.toUpperCase();
  const interval = (searchParams.get("interval") as Interval) || "5m";
  const range = (searchParams.get("range") as Range) || "1mo";
  const feePct = Number(searchParams.get("fee") ?? "0.02");

  if (!symbol) {
    return NextResponse.json({ error: "Paramètre 'symbol' requis" }, { status: 400 });
  }

  try {
    const market = await fetchMarketData(symbol, interval, range);
    const result = backtest(symbol, market.candles, undefined, { feePct });
    // On allège la réponse : pas besoin de toute la courbe d'equity côté liste.
    return NextResponse.json({
      symbol: result.symbol,
      metrics: result.metrics,
      trades: result.trades,
      equityCurve: result.equityCurve,
    });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}
