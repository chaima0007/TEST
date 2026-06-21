import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Water Pollution Environmental Rights Engine Agent",
  domain: "water_pollution_environmental_rights",
  total_entities: 8,
  avg_composite: 62.28,
  confidence_score: 0.88,
  avg_estimated_water_pollution_environmental_rights_index: 6.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["who_drinking_water_quality_guidelines_2022","unep_pollution_action_note_2023","business_human_rights_resource_pollution_database","amnesty_international_environmental_rights_report_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[water-pollution-environmental-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-pollution-environmental-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
