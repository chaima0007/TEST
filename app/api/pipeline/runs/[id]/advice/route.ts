import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { createAdvisor, type AdviceInput } from "@/lib/pipeline/advisor";
import type { Seniority } from "@/lib/pipeline/simulator";

export const dynamic = "force-dynamic";

const SENIORITIES: Seniority[] = ["junior", "mid", "senior"];
const asSeniority = (s: string): Seniority =>
  SENIORITIES.includes(s as Seniority) ? (s as Seniority) : "mid";

// GET /api/pipeline/runs/[id]/advice
// L'agent Conseiller : classe les propositions du run, simule la réussite et
// rédige une recommandation (heuristique, ou Claude si ANTHROPIC_API_KEY).
export async function GET(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const matches = await prisma.jobMatch.findMany({
    where: { runId: id, status: "proposed" },
    include: { analyzedJob: true, profile: true },
  });

  const items: AdviceInput[] = matches.map((m) => ({
    id: m.id,
    title: m.analyzedJob.title,
    profileName: m.profile.name,
    confidence: m.confidence,
    seniority: asSeniority(m.profile.seniority),
    budget: m.analyzedJob.budget,
  }));

  const advice = await createAdvisor().advise(items);
  return NextResponse.json(advice);
}
