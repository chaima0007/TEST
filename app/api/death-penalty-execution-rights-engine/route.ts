import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Death Penalty Execution Rights Engine Agent",
  domain: "death_penalty_execution_rights",
  total_entities: 8,
  avg_composite: 62.72,
  confidence_score: 0.89,
  avg_estimated_death_penalty_execution_rights_index: 6.27,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["amnesty_international_death_penalty_global_report_2023","death_penalty_information_center_2023","hands_off_cain_world_report_executions_2023","cornell_center_death_penalty_worldwide_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[death-penalty-execution-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/death-penalty-execution-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
