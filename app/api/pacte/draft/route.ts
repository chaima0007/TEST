import { NextRequest, NextResponse } from "next/server";
import { createPacte, type LeadBrief } from "@/lib/agents/pacte";
import { CAELUM_OFFER, type Offer } from "@/lib/agents/hermes";

export const dynamic = "force-dynamic";

// POST /api/pacte/draft
// Action de l'agent PACTE : PRÉPARE un devis / proposition commerciale pour un
// lead qualifié. PACTE n'envoie et ne signe RIEN (§10/§11) ; aucune persistance.
export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const raw = body as { lead?: Partial<LeadBrief>; offer?: Partial<Offer> };
  const firstName = raw.lead?.firstName?.trim();
  const company = raw.lead?.company?.trim();
  if (!firstName || !company) {
    return NextResponse.json(
      { error: "lead.firstName et lead.company sont requis" },
      { status: 400 },
    );
  }

  const lead: LeadBrief = {
    firstName,
    company,
    sector: raw.lead?.sector?.trim() || undefined,
    need: raw.lead?.need?.trim() || undefined,
    city: raw.lead?.city?.trim() || undefined,
  };

  const offer: Offer = {
    ...CAELUM_OFFER,
    ...(raw.offer?.service ? { service: raw.offer.service.trim() } : {}),
    ...(typeof raw.offer?.price === "number" && raw.offer.price > 0
      ? { price: raw.offer.price }
      : {}),
    ...(raw.offer?.currency ? { currency: raw.offer.currency.trim() } : {}),
    ...(raw.offer?.edge ? { edge: raw.offer.edge.trim() } : {}),
  };

  const proposal = await createPacte().draft(lead, offer);
  return NextResponse.json(proposal);
}
