import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cocoa-child-labor-rights] SWARM_API_URL non défini");
}

const MOCK = {
  agent: "Cocoa Child Labor Rights Engine Agent",
  domain: "cocoa_child_labor_rights",
  total_entities: 8,
  avg_composite: 62.15,
  confidence_score: 0.85,
  avg_estimated_cocoa_child_labor_rights_index: 6.22,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_child_labour_cocoa_2023",
    "us_department_labor_cocoa_2022",
    "cocoabarometer_2023",
    "human_rights_watch_cocoa_2021",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[cocoa-child-labor-rights] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/cocoa_child_labor_rights_engine`,
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
