import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Ethnic Minority Rights Discrimination Engine Agent",
  domain: "ethnic_minority_rights_discrimination",
  total_entities: 8,
  avg_composite: 63.11,
  confidence_score: 0.88,
  avg_estimated_ethnic_minority_rights_discrimination_index: 6.31,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["minority_rights_group_state_world_minorities_2023","human_rights_watch_ethnic_discrimination_database","un_special_rapporteur_minority_issues_2023","amnesty_international_racial_discrimination_report_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[ethnic-minority-rights-discrimination-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ethnic-minority-rights-discrimination-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
