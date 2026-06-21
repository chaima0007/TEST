import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Apostasy Blasphemy Persecution Engine Agent",
  domain: "apostasy_blasphemy_persecution",
  total_entities: 8,
  avg_composite: 63.30,
  confidence_score: 0.88,
  avg_estimated_apostasy_blasphemy_persecution_index: 6.33,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "uscirf_annual_report_2023",
    "human_rights_watch_apostasy_laws_2023",
    "amnesty_blasphemy_laws_report_2022",
    "un_sr_freedom_religion_belief_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[apostasy-blasphemy-persecution-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/apostasy-blasphemy-persecution-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
