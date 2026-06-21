import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Migrant Workers Rights Kafala Engine Agent",
  domain: "migrant_workers_rights_kafala",
  total_entities: 8,
  avg_composite: 61.83,
  confidence_score: 0.89,
  avg_estimated_migrant_workers_rights_kafala_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ilo_migrant_workers_report_2023","human_rights_watch_kafala_system_2023","amnesty_international_migrant_workers_gulf_2023","business_human_rights_resource_centre_migrant_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[migrant-workers-rights-kafala-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/migrant-workers-rights-kafala-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
