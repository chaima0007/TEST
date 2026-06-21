import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Stateless Persons Nationality Rights Engine Agent",
  domain: "stateless_persons_nationality_rights",
  total_entities: 8,
  avg_composite: 56.40,
  confidence_score: 0.87,
  avg_estimated_stateless_persons_nationality_rights_index: 5.64,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "unhcr_global_trends_statelessness_2023",
    "institute_statelessness_inclusion_report_2023",
    "open_society_justice_initiative_citizenship_2023",
    "human_rights_watch_statelessness_database",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[stateless_persons_nationality_rights-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/stateless-persons-nationality-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
