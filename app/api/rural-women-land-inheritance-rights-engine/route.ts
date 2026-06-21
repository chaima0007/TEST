import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Rural Women Land Inheritance Rights Engine Agent",
  domain: "rural_women_land_inheritance_rights",
  total_entities: 8,
  avg_composite: 61.80,
  confidence_score: 0.87,
  avg_estimated_rural_women_land_inheritance_rights_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "fao_women_land_rights_report_2023",
    "un_women_rural_women_report_2023",
    "landesa_gender_land_rights_2022",
    "african_union_gender_protocol_implementation_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[rural-women-land-inheritance-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/rural-women-land-inheritance-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
