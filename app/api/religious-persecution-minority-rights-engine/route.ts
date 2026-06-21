import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Religious Persecution Minority Rights Engine Agent",
  domain: "religious_persecution_minority_rights",
  total_entities: 8,
  avg_composite: 63.43,
  confidence_score: 0.86,
  avg_estimated_religious_persecution_minority_rights_index: 6.34,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["open_doors_world_watch_list_2024","us_commission_international_religious_freedom_2023","pew_research_global_restrictions_religion_2023","human_rights_watch_religious_persecution_database"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[religious-persecution-minority-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/religious-persecution-minority-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
