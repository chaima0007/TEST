import { NextResponse } from "next/server";
import { getAccount } from "@/lib/trading/broker";

// GET /api/trading/account — état du compte courtier (paper par défaut).
export async function GET() {
  try {
    const account = await getAccount();
    return NextResponse.json(account);
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 502 });
  }
}
