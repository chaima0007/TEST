import { NextRequest, NextResponse } from "next/server";
import { fetchMarketData } from "@/lib/trading/yahoo";
import { generateSignal } from "@/lib/trading/strategy";
import type { Interval, Range } from "@/lib/trading/types";

// GET /api/trading/signal?symbol=AAPL&interval=5m&range=5d
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const symbol = searchParams.get("symbol")?.toUpperCase();
  const interval = (searchParams.get("interval") as Interval) || "5m";
  const range = (searchParams.get("range") as Range) || "5d";

  if (!symbol) {
    return NextResponse.json({ error: "Paramètre 'symbol' requis" }, { status: 400 });
  }

  try {
    const market = await fetchMarketData(symbol, interval, range);
    const signal = generateSignal(symbol, market.candles);
    return NextResponse.json({
      symbol: market.symbol,
      currency: market.currency,
      exchange: market.exchange,
      lastPrice: market.lastPrice,
      candleCount: market.candles.length,
      signal,
    });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}
