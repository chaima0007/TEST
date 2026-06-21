import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Academic Freedom Scholar Persecution Engine Agent",
  domain: "academic-freedom-scholar-persecution",
  total_entities: 8,
  avg_composite: 57.62,
  confidence_score: 0.86,
  avg_estimated_academic_freedom_scholar_persecution_index: 5.76,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "scholars_at_risk_network_monitoring_project_2023",
    "academic_freedom_index_fau_erlangen_2023",
    "human_rights_watch_academic_freedom_reports",
    "aaup_annual_report_academic_freedom_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[academic-freedom-scholar-persecution-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/academic-freedom-scholar-persecution-engine`,
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
