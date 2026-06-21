import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Water Scarcity Conflict Rights Engine Agent",
  domain: "water_scarcity_conflict_rights",
  total_entities: 8,
  avg_composite: 58.78,
  confidence_score: 0.87,
  avg_estimated_water_scarcity_conflict_rights_index: 5.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "who_unicef_jmp_water_sanitation_report",
    "un_water_world_water_development_report",
    "hrw_water_conflict_rights_violations_documentation",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[water-scarcity-conflict-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-scarcity-conflict-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
