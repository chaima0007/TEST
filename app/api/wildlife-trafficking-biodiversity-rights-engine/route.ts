import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Wildlife Trafficking Biodiversity Rights Engine Agent",
  domain: "wildlife_trafficking_biodiversity_rights",
  total_entities: 8,
  avg_composite: 61.50,
  confidence_score: 0.87,
  avg_estimated_wildlife_trafficking_biodiversity_rights_index: 6.15,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "cites_wildlife_trade_report_2023",
    "unodc_wildlife_crime_report_2023",
    "wwf_living_planet_report_2022",
    "traffic_wildlife_trafficking_analysis_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[wildlife-trafficking-biodiversity-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/wildlife-trafficking-biodiversity-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
