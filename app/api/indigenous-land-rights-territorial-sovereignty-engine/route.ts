import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Indigenous Land Rights Territorial Sovereignty Engine Agent",
  domain: "indigenous_land_rights_territorial_sovereignty",
  total_entities: 8,
  avg_composite: 57.06,
  confidence_score: 0.88,
  avg_estimated_indigenous_land_rights_territorial_sovereignty_index: 5.71,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "un_special_rapporteur_indigenous_peoples_2023",
    "forest_peoples_programme_land_rights_2023",
    "global_witness_land_defenders_killed_2023",
    "cultural_survival_quarterly_indigenous_land_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[indigenous_land_rights_territorial_sovereignty-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-land-rights-territorial-sovereignty-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
