import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { resumeRun } from "@/lib/pipeline/orchestrator";

export const dynamic = "force-dynamic";

// POST /api/pipeline/runs/[id]/resume — reprend un run en échec depuis l'étape fautive.
export async function POST(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const run = await prisma.pipelineRun.findUnique({ where: { id } });
  if (!run) return NextResponse.json({ error: "Run introuvable" }, { status: 404 });
  if (run.status === "completed") {
    return NextResponse.json({ error: "Run déjà terminé" }, { status: 409 });
  }

  await resumeRun(id);
  const updated = await prisma.pipelineRun.findUnique({
    where: { id },
    include: { steps: { orderBy: { createdAt: "asc" } } },
  });
  return NextResponse.json(updated);
}
