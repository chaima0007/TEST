import { NextRequest, NextResponse } from "next/server";
import { runAutopilot } from "@/lib/pipeline/autopilot";
import type { Recommendation } from "@/lib/pipeline/simulator";

export const dynamic = "force-dynamic";

const LEVELS: Recommendation[] = ["skip", "consider", "strong"];

// POST /api/pipeline/runs/[id]/autopilot
// body (optionnel): { level?: "strong"|"consider"|"skip", force?: boolean }
// L'agent auto-pilote prépare les dossiers des opportunités prioritaires.
export async function POST(
  req: NextRequest,
  props: { params: Promise<{ id: string }> },
) {
  const { id } = await props.params;
  const body = (await req.json().catch(() => ({}))) as { level?: string; force?: boolean };
  const level = LEVELS.includes(body.level as Recommendation) ? (body.level as Recommendation) : "strong";

  const report = await runAutopilot(id, { level, force: body.force });
  return NextResponse.json(report);
}
