import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Indigenous Land Cultural Rights Engine Agent",
  domain: "indigenous_land_cultural_rights",
  total_entities: 8,
  avg_composite: 61.44,
  confidence_score: 0.87,
  avg_estimated_indigenous_land_cultural_rights_index: 6.14,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_special_rapporteur_indigenous_peoples_annual_report",
    "forest_peoples_programme_land_rights_violations",
    "cultural_survival_indigenous_rights_monitor",
    "hrw_indigenous_land_documentation",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[indigenous-land-cultural-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-land-cultural-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
