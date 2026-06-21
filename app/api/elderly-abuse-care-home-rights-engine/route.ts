import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Elderly Abuse Care Home Rights Engine Agent",
  domain: "elderly_abuse_care_home_rights",
  total_entities: 8,
  avg_composite: 52.51,
  confidence_score: 0.86,
  avg_estimated_elderly_abuse_care_home_rights_index: 5.25,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["who_elder_abuse_report_2022","human_rights_watch_nursing_homes_2021","un_decade_healthy_ageing_2022","age_platform_europe_2023"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[elderly-abuse-care-home-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elderly-abuse-care-home-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
