import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Refugees Asylum Seekers Rights Engine Agent",
  domain: "refugees_asylum_seekers_rights",
  total_entities: 8,
  avg_composite: 58.40,
  confidence_score: 0.88,
  avg_estimated_refugees_asylum_seekers_rights_index: 5.84,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "unhcr_global_trends_2023",
    "human_rights_watch_refugee_rights_2023",
    "amnesty_international_refugee_crisis_report_2023",
    "borderline_europe_pushback_monitoring_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[refugees-asylum-seekers-rights-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugees-asylum-seekers-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
