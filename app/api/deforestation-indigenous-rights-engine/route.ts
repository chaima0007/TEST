import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Deforestation Indigenous Rights Engine Agent",
  domain: "deforestation_indigenous_rights",
  total_entities: 8,
  avg_composite: 62.00,
  confidence_score: 0.88,
  avg_estimated_deforestation_indigenous_rights_index: 6.20,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "global_forest_watch_deforestation_2023",
    "human_rights_watch_amazon_defenders_2023",
    "un_sr_indigenous_peoples_forests_2023",
    "global_witness_land_defenders_killed_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[deforestation-indigenous-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/deforestation-indigenous-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
