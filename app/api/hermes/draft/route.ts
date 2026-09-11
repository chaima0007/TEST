import { NextRequest, NextResponse } from "next/server";
import { createHermes, CAELUM_OFFER, type Prospect, type Offer } from "@/lib/agents/hermes";

export const dynamic = "force-dynamic";

// POST /api/hermes/draft
// Action de l'agent HERMES : PRÉPARE des brouillons de prospection LinkedIn
// (note de connexion + variante A/B + 1er message + relance) pour un prospect.
// HERMES n'envoie RIEN : l'envoi reste MANUEL par Chaima après relecture (§10).
// Aucune persistance ici — le drafter est sans état ; rien n'est écrit en base.
export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const raw = body as { prospect?: Partial<Prospect>; offer?: Partial<Offer> };
  const firstName = raw.prospect?.firstName?.trim();
  const company = raw.prospect?.company?.trim();
  if (!firstName || !company) {
    return NextResponse.json(
      { error: "prospect.firstName et prospect.company sont requis" },
      { status: 400 },
    );
  }

  const prospect: Prospect = {
    firstName,
    company,
    sector: raw.prospect?.sector?.trim() || undefined,
    signal: raw.prospect?.signal?.trim() || undefined,
    city: raw.prospect?.city?.trim() || undefined,
  };

  // Offre par défaut = offre Caelum (site web premium 500€) ; surchargeable.
  const offer: Offer = {
    ...CAELUM_OFFER,
    ...(raw.offer?.service ? { service: raw.offer.service.trim() } : {}),
    ...(typeof raw.offer?.price === "number" && raw.offer.price > 0
      ? { price: raw.offer.price }
      : {}),
    ...(raw.offer?.currency ? { currency: raw.offer.currency.trim() } : {}),
    ...(raw.offer?.edge ? { edge: raw.offer.edge.trim() } : {}),
  };

  const draft = await createHermes().draft(prospect, offer);
  return NextResponse.json(draft);
}
