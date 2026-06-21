import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Maternal Health Rights Obstetric Violence Engine Agent",
  domain: "maternal-health-rights-obstetric-violence",
  total_entities: 8,
  avg_composite: 60.64,
  confidence_score: 0.87,
  avg_estimated_maternal_health_rights_obstetric_violence_index: 6.06,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "who_maternal_mortality_estimates_2023",
    "lancet_obstetric_violence_systematic_review_2023",
    "unfpa_state_world_population_2023",
    "human_rights_watch_reproductive_rights_database",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[maternal-health-rights-obstetric-violence-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/maternal-health-rights-obstetric-violence-engine`,
      { next: { revalidate: 30 } }
    );
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ error: "upstream_error" }, { status: 502 })
    );
  }
}
