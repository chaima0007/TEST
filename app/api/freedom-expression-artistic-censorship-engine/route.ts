import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Freedom Expression Artistic Censorship Engine Agent",
  domain: "freedom_expression_artistic_censorship",
  total_entities: 8,
  avg_composite: 62.66,
  confidence_score: 0.86,
  avg_estimated_freedom_expression_artistic_censorship_index: 6.27,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "freemuse_state_of_artistic_freedom_2023",
    "pen_international_artistic_freedom_violations_2023",
    "human_rights_watch_cultural_rights_2023",
    "ipi_artistic_expression_press_freedom_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[freedom-expression-artistic-censorship-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/freedom-expression-artistic-censorship-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
