import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "War Crimes Accountability Engine Agent",
  domain: "war_crimes_accountability",
  total_entities: 8,
  avg_composite: 62.40,
  confidence_score: 0.89,
  avg_estimated_war_crimes_accountability_index: 6.24,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "icc_annual_report_situations_2023",
    "un_commission_inquiry_war_crimes_2023",
    "human_rights_watch_ihl_violations_2023",
    "icrc_international_humanitarian_law_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[war-crimes-accountability-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/war-crimes-accountability-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
