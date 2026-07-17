import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[api/aiads] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/aiads`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(
      NextResponse.json(
        {
          domain: "aiads",
          entities: [],
          avg_composite: 61.03,
          estimated_aiads_index: 6.1,
          distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
          generatedAt: new Date().toISOString(),
          mode: "fallback",
        },
        { status: 502 }
      )
    );
  }
}
