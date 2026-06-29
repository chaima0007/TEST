import { NextRequest, NextResponse } from "next/server";
import { runBot, type BotOptions } from "@/lib/trading/bot";

// POST /api/trading/order
// Body JSON : { symbol, interval?, range?, capital?, riskPerTradePct?,
//               minConfidence?, strikeOffset?, expiration?, analyzeOnly?, confirmLive? }
//
// Lance le pipeline complet : signal -> sélection du contrat d'option -> ordre.
// Par défaut le courtier est en mode paper / dry-run (voir lib/trading/broker.ts).
export async function POST(req: NextRequest) {
  let body: Partial<BotOptions>;
  try {
    body = (await req.json()) as Partial<BotOptions>;
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const symbol = body.symbol?.toUpperCase();
  if (!symbol) {
    return NextResponse.json({ error: "Champ 'symbol' requis" }, { status: 400 });
  }

  try {
    const run = await runBot({ ...body, symbol });
    return NextResponse.json(run);
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}
