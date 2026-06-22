import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[vanilla-child-labor-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Vanilla Child Labor Rights Engine Agent",
  domain: "vanilla_child_labor_rights",
  total_entities: 8,
  avg_composite: 62.43,
  confidence_score: 0.83,
  avg_estimated_vanilla_child_labor_rights_index: 6.24,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_child_labour_vanilla_2023",
    "us_department_labor_vanilla_2022",
    "human_rights_watch_madagascar_2021",
    "fairtrade_vanilla_supply_chain_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[vanilla-child-labor-rights] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/vanilla_child_labor_rights_engine`,
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
