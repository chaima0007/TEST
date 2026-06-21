import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Caste Discrimination Untouchability Engine Agent",
  domain: "caste_discrimination_untouchability",
  total_entities: 8,
  avg_composite: 57.21,
  confidence_score: 0.87,
  avg_estimated_caste_discrimination_untouchability_index: 5.72,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "human_rights_watch_caste_discrimination_2023",
    "equality_labs_caste_report_2023",
    "international_dalit_solidarity_network_2023",
    "un_special_rapporteur_minority_rights_caste_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[caste-discrimination-untouchability-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/caste-discrimination-untouchability-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
