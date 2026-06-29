import { NextRequest, NextResponse } from "next/server";
import { getMarketData } from "@/lib/trading/datasource";
import { computeIndicators } from "@/lib/trading/strategy";
import type { Interval, Range } from "@/lib/trading/types";

// GET /api/trading/candles?symbol=AAPL&interval=5m&range=5d
// Renvoie les bougies + les séries d'indicateurs pour les graphiques.
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const symbol = searchParams.get("symbol")?.toUpperCase();
  const interval = (searchParams.get("interval") as Interval) || "5m";
  const range = (searchParams.get("range") as Range) || "5d";

  if (!symbol) {
    return NextResponse.json({ error: "Paramètre 'symbol' requis" }, { status: 400 });
  }

  try {
    const market = await getMarketData(symbol, interval, range);
    const indicators = computeIndicators(market.candles);
    return NextResponse.json({ ...market, indicators });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}
