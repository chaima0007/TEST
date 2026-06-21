import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Housing Rights Forced Evictions Engine Agent",
  domain: "housing_rights_forced_evictions",
  total_entities: 8,
  avg_composite: 60.12,
  confidence_score: 0.86,
  avg_estimated_housing_rights_forced_evictions_index: 6.01,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_habitat_world_cities_report_2022","cohre_forced_evictions_global_survey_2023","feantsa_homeless_europe_report_2023","human_rights_watch_housing_rights_database"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[housing-rights-forced-evictions-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-rights-forced-evictions-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
