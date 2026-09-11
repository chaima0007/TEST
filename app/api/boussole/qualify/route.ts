import { NextRequest, NextResponse } from "next/server";
import { qualify, type Lead, type Timing, type WebsiteState } from "@/lib/agents/boussole";

export const dynamic = "force-dynamic";

const TIMINGS: Timing[] = ["now", "soon", "later", "unknown"];
const SITES: WebsiteState[] = ["none", "outdated", "recent", "unknown"];

// POST /api/boussole/qualify
// Action de l'agent BOUSSOLE : qualifie un lead de façon déterministe et
// RECOMMANDE une prochaine action. Aucune persistance, aucune décision engagée.
export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const raw = body as { lead?: Partial<Lead> };
  const firstName = raw.lead?.firstName?.trim();
  const company = raw.lead?.company?.trim();
  if (!firstName || !company) {
    return NextResponse.json(
      { error: "lead.firstName et lead.company sont requis" },
      { status: 400 },
    );
  }

  const lead: Lead = {
    firstName,
    company,
    sector: raw.lead?.sector?.trim() || undefined,
    reply: raw.lead?.reply?.trim() || undefined,
    needClear: typeof raw.lead?.needClear === "boolean" ? raw.lead.needClear : undefined,
    budgetSignal: typeof raw.lead?.budgetSignal === "boolean" ? raw.lead.budgetSignal : undefined,
    timing: TIMINGS.includes(raw.lead?.timing as Timing) ? (raw.lead?.timing as Timing) : undefined,
    decisionMaker: typeof raw.lead?.decisionMaker === "boolean" ? raw.lead.decisionMaker : undefined,
    hasWebsite: SITES.includes(raw.lead?.hasWebsite as WebsiteState)
      ? (raw.lead?.hasWebsite as WebsiteState)
      : undefined,
  };

  return NextResponse.json(qualify(lead));
}
