import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Peasant Land Tenure Rights Engine Agent",
  domain: "peasant_land_tenure_rights",
  total_entities: 8,
  avg_composite: 61.50,
  confidence_score: 0.87,
  avg_estimated_peasant_land_tenure_rights_index: 6.15,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_declaration_peasants_rights_2018",
    "fao_voluntary_guidelines_land_tenure_2012",
    "land_matrix_initiative_global_report_2023",
    "oxfam_land_grabs_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[peasant-land-tenure-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/peasant-land-tenure-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
