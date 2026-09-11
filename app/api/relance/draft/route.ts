import { NextRequest, NextResponse } from "next/server";
import { createRelance, type PendingQuote, type Objection } from "@/lib/agents/relance";
import { CAELUM_OFFER, type Offer } from "@/lib/agents/hermes";

export const dynamic = "force-dynamic";

const OBJECTIONS: Objection[] = ["price", "timing", "trust", "none"];

// POST /api/relance/draft
// Action de l'agent RELANCE : PRÉPARE une séquence de relance de devis. Aucune
// persistance, aucun envoi — l'envoi reste manuel (§10).
export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const raw = body as { quote?: Partial<PendingQuote>; offer?: Partial<Offer> };
  const firstName = raw.quote?.firstName?.trim();
  const company = raw.quote?.company?.trim();
  if (!firstName || !company) {
    return NextResponse.json(
      { error: "quote.firstName et quote.company sont requis" },
      { status: 400 },
    );
  }

  const quote: PendingQuote = {
    firstName,
    company,
    service: raw.quote?.service?.trim() || undefined,
    city: raw.quote?.city?.trim() || undefined,
    objection: OBJECTIONS.includes(raw.quote?.objection as Objection)
      ? (raw.quote?.objection as Objection)
      : undefined,
  };

  const offer: Offer = {
    ...CAELUM_OFFER,
    ...(raw.offer?.service ? { service: raw.offer.service.trim() } : {}),
    ...(typeof raw.offer?.price === "number" && raw.offer.price > 0 ? { price: raw.offer.price } : {}),
    ...(raw.offer?.currency ? { currency: raw.offer.currency.trim() } : {}),
    ...(raw.offer?.edge ? { edge: raw.offer.edge.trim() } : {}),
  };

  const sequence = await createRelance().draft(quote, offer);
  return NextResponse.json(sequence);
}
