import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[lgbtq-rights-violence-criminalization-engine] SWARM_API_URL not set — returning mock");
}

const MOCK = {
  agent: "LGBTQ Rights Violence Criminalization Engine Agent",
  domain: "lgbtq_rights_violence_criminalization",
  total_entities: 8,
  avg_composite: 62.89,
  confidence_score: 0.87,
  avg_estimated_lgbtq_rights_violence_criminalization_index: 6.29,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilga_world_state_sponsored_homophobia_2023",
    "human_rights_watch_lgbtq_database_2023",
    "amnesty_international_sexual_orientation_rights_2023",
    "outright_international_violence_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/lgbtq-rights-violence-criminalization-engine`,
      { next: { revalidate: 30 } }
    );
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(
      NextResponse.json({ error: "upstream_error" }, { status: 502 })
    );
  }
}
