import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Caste Discrimination Dalit Rights Engine Agent",
  domain: "caste_discrimination_dalit_rights",
  total_entities: 8,
  avg_composite: 62.50,
  confidence_score: 0.88,
  avg_estimated_caste_discrimination_dalit_rights_index: 6.25,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_special_rapporteur_minority_issues_caste_2023",
    "human_rights_watch_dalit_india_2023",
    "amnesty_caste_discrimination_report_2022",
    "international_dalit_solidarity_network_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[caste-discrimination-dalit-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/caste-discrimination-dalit-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
