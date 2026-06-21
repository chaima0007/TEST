import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Residential School Indigenous Assimilation Engine Agent",
  domain: "residential_school_indigenous_assimilation",
  total_entities: 8,
  avg_composite: 53.51,
  confidence_score: 0.89,
  avg_estimated_residential_school_indigenous_assimilation_index: 5.35,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["truth_reconciliation_canada_2015","un_indigenous_peoples_forum_2022","residential_school_survivor_network_2023","ohchr_indigenous_assimilation_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[residential-school-indigenous-assimilation-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/residential-school-indigenous-assimilation-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
