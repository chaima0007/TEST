import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Mental Health Forced Treatment Rights Engine Agent",
  domain: "mental_health_forced_treatment_rights",
  total_entities: 8,
  avg_composite: 57.98,
  confidence_score: 0.87,
  avg_estimated_mental_health_forced_treatment_rights_index: 5.80,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "who_mental_health_report_2022",
    "un_crpd_monitoring_2023",
    "mental_disability_rights_international_2022",
    "ohchr_psychiatric_detention_2022",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[mental-health-forced-treatment-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mental-health-forced-treatment-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
