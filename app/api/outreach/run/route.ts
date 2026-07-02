import { NextRequest, NextResponse } from "next/server";
import { runPipeline } from "@/lib/outreach/agents/orchestrator";

// POST /api/outreach/run
// Lance le pipeline complet (Scout → Qualifier → Copywriter → Sequencer → Mailer).
export async function POST(request: NextRequest) {
  let body: {
    categories?: unknown;
    cities?: unknown;
    dryRun?: unknown;
    skipDiscovery?: unknown;
  } = {};
  try {
    const parsed = await request.json();
    if (parsed && typeof parsed === "object") body = parsed;
  } catch {
    // Corps vide ou invalide : on garde les valeurs par défaut.
  }

  const categories = Array.isArray(body.categories)
    ? body.categories.map(String)
    : [];
  const cities = Array.isArray(body.cities) ? body.cities.map(String) : [];

  // Sans catégories ou villes, la découverte n'a pas de sens : on la saute.
  const skipDiscovery =
    categories.length === 0 || cities.length === 0
      ? true
      : Boolean(body.skipDiscovery);

  try {
    const report = await runPipeline({
      categories,
      cities,
      ...(typeof body.dryRun === "boolean" ? { dryRun: body.dryRun } : {}),
      skipDiscovery,
    });
    return NextResponse.json(report);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Erreur interne";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
