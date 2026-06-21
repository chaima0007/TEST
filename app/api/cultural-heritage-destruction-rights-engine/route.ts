import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Cultural Heritage Destruction Rights Engine Agent",
  domain: "cultural_heritage_destruction_rights",
  total_entities: 8,
  avg_composite: 59.76,
  confidence_score: 0.87,
  avg_estimated_cultural_heritage_destruction_rights_index: 5.98,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unesco_convention_1954_hague_cultural_property_protection",
    "icc_al_mahdi_cultural_heritage_destruction_judgment_2016",
    "interpol_works_of_art_unit_illicit_trafficking_report_2023",
    "blue_shield_international_armed_conflict_heritage_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[cultural-heritage-destruction-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cultural-heritage-destruction-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
