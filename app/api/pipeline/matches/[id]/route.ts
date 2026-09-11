import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getMinBudgetThreshold, setMinBudgetThreshold } from "@/lib/pipeline/settings";

export const dynamic = "force-dynamic";

// POST /api/pipeline/matches/[id] — validation humaine d'une proposition.
// body: { action: "approve" | "reject", reason?: "budget" | "skills" | "other" }
//
// Boucle de rétroaction : un rejet pour "budget" relève automatiquement le seuil
// budget global, pour que les futures offres trop basses soient filtrées d'office.
export async function POST(
  req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const body = (await req.json()) as { action?: string; reason?: string };
  const action = body.action;

  if (action !== "approve" && action !== "reject") {
    return NextResponse.json({ error: "action doit être 'approve' ou 'reject'" }, { status: 400 });
  }

  const match = await prisma.jobMatch.findUnique({
    where: { id },
    include: { analyzedJob: true },
  });
  if (!match) return NextResponse.json({ error: "Match introuvable" }, { status: 404 });

  let thresholdAdjusted: number | null = null;

  if (action === "reject" && body.reason === "budget") {
    const current = await getMinBudgetThreshold();
    const jobBudget = match.analyzedJob.budget ?? 0;
    // On vise juste au-dessus de l'offre rejetée, sinon +20% par défaut.
    const next = Math.round(Math.max(current * 1.2, jobBudget + 1));
    if (next > current) {
      await setMinBudgetThreshold(next);
      thresholdAdjusted = next;
    }
  }

  const updated = await prisma.jobMatch.update({
    where: { id },
    data: {
      status: action === "approve" ? "approved" : "rejected",
      rejectReason: action === "reject" ? (body.reason ?? "other") : null,
    },
  });

  return NextResponse.json({ match: updated, thresholdAdjusted });
}
