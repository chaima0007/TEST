import { NextRequest, NextResponse } from "next/server";
import { runScout } from "@/lib/outreach/agents/scout";
import { runQualifier } from "@/lib/outreach/agents/qualifier";

// POST /api/outreach/discover
// Lance la découverte (Scout) puis la qualification (Qualifier).
export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const { categories, cities } = (body ?? {}) as {
    categories?: unknown;
    cities?: unknown;
  };

  if (!Array.isArray(categories) || categories.length === 0) {
    return NextResponse.json(
      { error: "Le champ \"categories\" doit être un tableau non vide." },
      { status: 400 }
    );
  }
  if (!Array.isArray(cities) || cities.length === 0) {
    return NextResponse.json(
      { error: "Le champ \"cities\" doit être un tableau non vide." },
      { status: 400 }
    );
  }

  try {
    const scout = await runScout({
      categories: categories.map(String),
      cities: cities.map(String),
    });
    const qualifier = await runQualifier();
    return NextResponse.json({ scout, qualifier });
  } catch (err) {
    const message = err instanceof Error ? err.message : "Erreur interne";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
