import { NextRequest, NextResponse } from "next/server";
import { fetchOptionsChain, selectContract } from "@/lib/trading/options";

// GET /api/trading/options?symbol=AAPL&direction=long&offset=0&expiration=<ms>
// Renvoie la chaîne d'options et, si `direction` est fournie, le contrat retenu.
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const symbol = searchParams.get("symbol")?.toUpperCase();
  const direction = searchParams.get("direction") as "long" | "short" | null;
  const offset = Number(searchParams.get("offset") ?? "0");
  const expirationParam = searchParams.get("expiration");
  const expiration = expirationParam ? Number(expirationParam) : undefined;

  if (!symbol) {
    return NextResponse.json({ error: "Paramètre 'symbol' requis" }, { status: 400 });
  }

  try {
    const chain = await fetchOptionsChain(symbol, expiration);
    const selection =
      direction === "long" || direction === "short"
        ? selectContract(chain, direction, offset)
        : null;
    return NextResponse.json({
      symbol: chain.symbol,
      underlyingPrice: chain.underlyingPrice,
      expiration: chain.expiration,
      expirationDates: chain.expirationDates,
      selection,
      // On limite la chaîne renvoyée aux strikes proches de la monnaie.
      calls: nearMoney(chain.calls, chain.underlyingPrice),
      puts: nearMoney(chain.puts, chain.underlyingPrice),
    });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}

function nearMoney<T extends { strike: number }>(list: T[], price: number): T[] {
  return list
    .slice()
    .sort((a, b) => Math.abs(a.strike - price) - Math.abs(b.strike - price))
    .slice(0, 12)
    .sort((a, b) => a.strike - b.strike);
}
