import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Border Wall Migration Rights Engine Agent",
  domain: "border_wall_migration_rights",
  total_entities: 8,
  avg_composite: 58.85,
  confidence_score: 0.87,
  avg_estimated_border_wall_migration_rights_index: 5.89,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unhcr_global_trends_forced_displacement_report",
    "hrw_border_violence_pushback_documentation",
    "amnesty_international_migration_detention_report",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[border-wall-migration-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/border-wall-migration-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
