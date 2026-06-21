import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Land Grabbing Displacement Rights Engine Agent",
  domain: "land_grabbing_displacement_rights",
  total_entities: 8,
  avg_composite: 61.52,
  confidence_score: 0.87,
  avg_estimated_land_grabbing_displacement_rights_index: 6.15,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["global_witness_land_defenders_killed_2023","oakland_institute_land_grabbing_database_2023","grain_land_grabbing_global_2023","business_human_rights_resource_centre_land_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[land-grabbing-displacement-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-grabbing-displacement-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
