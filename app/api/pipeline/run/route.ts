import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { startRun } from "@/lib/pipeline/orchestrator";
import { getMinBudgetThreshold } from "@/lib/pipeline/settings";

export const dynamic = "force-dynamic";

// POST /api/pipeline/run — déclenche un nouveau passage complet du pipeline.
export async function POST() {
  const runId = await startRun();
  const run = await prisma.pipelineRun.findUnique({
    where: { id: runId },
    include: { steps: { orderBy: { createdAt: "asc" } } },
  });
  return NextResponse.json(run, { status: 201 });
}

// GET /api/pipeline/run — liste les runs récents + le seuil budget courant.
export async function GET() {
  const [runs, threshold] = await Promise.all([
    prisma.pipelineRun.findMany({
      orderBy: { startedAt: "desc" },
      take: 20,
      include: {
        steps: { orderBy: { createdAt: "asc" } },
        _count: { select: { matches: true, analyzed: true } },
      },
    }),
    getMinBudgetThreshold(),
  ]);
  return NextResponse.json({ runs, minBudgetThreshold: threshold });
}
