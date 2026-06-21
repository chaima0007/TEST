import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Corruption Human Rights Nexus Engine Agent",
  domain: "corruption_human_rights_nexus",
  total_entities: 8,
  avg_composite: 63.04,
  confidence_score: 0.87,
  avg_estimated_corruption_human_rights_nexus_index: 6.30,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["transparency_international_cpi_2023","human_rights_watch_corruption_impunity_2023","global_integrity_report_2023","unodc_corruption_human_rights_nexus_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[corruption-human-rights-nexus-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corruption-human-rights-nexus-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
