import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

// GET /api/pipeline/runs/[id] — détail d'un run : étapes, offres analysées, matchs.
export async function GET(
  _req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const run = await prisma.pipelineRun.findUnique({
    where: { id },
    include: {
      steps: { orderBy: { createdAt: "asc" } },
      analyzed: { orderBy: { status: "asc" } },
      matches: {
        orderBy: { confidence: "desc" },
        include: { analyzedJob: true, profile: true },
      },
    },
  });

  if (!run) {
    return NextResponse.json({ error: "Run introuvable" }, { status: 404 });
  }
  return NextResponse.json(run);
}
