import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Death Penalty Abolition Rights Engine Agent",
  domain: "death_penalty_abolition_rights",
  total_entities: 8, avg_composite: 57.23, confidence_score: 0.87,
  avg_estimated_death_penalty_abolition_rights_index: 5.72,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["amnesty_death_penalty_global_report_2023","hands_off_cain_2023","cornell_death_penalty_worldwide_2022","un_ohchr_capital_punishment_2023"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[death-penalty-abolition-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/death-penalty-abolition-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
