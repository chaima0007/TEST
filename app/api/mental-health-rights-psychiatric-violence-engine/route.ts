import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Mental Health Rights Psychiatric Violence Engine Agent",
  domain: "mental_health_rights_psychiatric_violence",
  total_entities: 8,
  avg_composite: 57.06,
  confidence_score: 0.86,
  avg_estimated_mental_health_rights_psychiatric_violence_index: 5.71,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "who_mental_health_atlas_2023",
    "disability_rights_international_psychiatric_report",
    "mad_in_america_forced_treatment_database",
    "mental_health_europe_annual_report_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[mental_health_rights_psychiatric_violence-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mental-health-rights-psychiatric-violence-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
