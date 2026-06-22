import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[coffee-labor-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Coffee Labor Rights Engine Agent",
  domain: "coffee_labor_rights",
  total_entities: 8,
  avg_composite: 61.88,
  confidence_score: 0.84,
  avg_estimated_coffee_labor_rights_index: 6.19,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_coffee_labor_standards_2023",
    "fairtrade_international_coffee_2022",
    "human_rights_watch_coffee_2021",
    "oxfam_coffee_supply_chain_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[coffee-labor-rights] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/coffee_labor_rights_engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(
      NextResponse.json({ error: "Upstream unavailable" }, { status: 502 })
    );
  }
}
