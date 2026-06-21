import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Elderly Rights Age Discrimination Engine Agent",
  domain: "elderly_rights_age_discrimination",
  total_entities: 8,
  avg_composite: 59.95,
  confidence_score: 0.85,
  avg_estimated_elderly_rights_age_discrimination_index: 6.00,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["who_global_report_ageism_2021","helpage_global_agewatch_index_2023","human_rights_watch_elder_care_database","un_open_ended_working_group_ageing_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[elderly-rights-age-discrimination-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elderly-rights-age-discrimination-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
