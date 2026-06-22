import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[rubber-plantation-labor-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Rubber Plantation Labor Rights Engine Agent",
  domain: "rubber_plantation_labor_rights",
  total_entities: 8,
  avg_composite: 61.72,
  confidence_score: 0.82,
  avg_estimated_rubber_plantation_labor_rights_index: 6.17,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_rubber_plantation_labor_2023",
    "amnesty_international_rubber_2022",
    "human_rights_watch_rubber_2021",
    "global_witness_rubber_supply_chain_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[rubber-plantation-labor-rights] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/rubber_plantation_labor_rights_engine`,
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
