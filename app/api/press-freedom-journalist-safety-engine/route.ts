import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[press-freedom-journalist-safety-engine] SWARM_API_URL not set — returning mock");
}

const MOCK = {
  agent: "Press Freedom Journalist Safety Engine Agent",
  domain: "press_freedom_journalist_safety",
  total_entities: 8,
  avg_composite: 62.63,
  confidence_score: 0.89,
  avg_estimated_press_freedom_journalist_safety_index: 6.26,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "rsf_world_press_freedom_index_2024",
    "committee_protect_journalists_impunity_index_2023",
    "reporters_without_borders_barometer_2024",
    "cpj_journalists_imprisoned_database_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/press-freedom-journalist-safety-engine`,
      { next: { revalidate: 30 } }
    );
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(
      NextResponse.json({ error: "upstream_error" }, { status: 502 })
    );
  }
}
