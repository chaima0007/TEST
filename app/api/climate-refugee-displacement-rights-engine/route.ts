import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Climate Refugee Displacement Rights Engine Agent",
  domain: "climate-refugee-displacement-rights",
  total_entities: 8,
  avg_composite: 60.26,
  confidence_score: 0.88,
  avg_estimated_climate_refugee_displacement_rights_index: 6.03,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "idmc_global_report_internal_displacement_2023",
    "unhcr_climate_change_displacement_report_2023",
    "platform_disaster_displacement_2023",
    "ipcc_sixth_assessment_report_displacement_chapter",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[climate-refugee-displacement-rights-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/climate-refugee-displacement-rights-engine`,
      { next: { revalidate: 30 } }
    );
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ error: "upstream_error" }, { status: 502 })
    );
  }
}
