import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Elder Rights Ageism Engine Agent",
  domain: "elder_rights_ageism",
  total_entities: 8,
  avg_composite: 57.24,
  confidence_score: 0.87,
  avg_estimated_elder_rights_ageism_index: 5.72,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["who_ageism_global_report_2021","helpage_global_agewatch_2023","un_open_ended_working_group_ageing_2022","human_rights_watch_elder_abuse_2023"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[elder-rights-ageism-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elder-rights-ageism-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
