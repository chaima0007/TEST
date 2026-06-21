import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Disability Rights Inclusive Society Engine Agent",
  domain: "disability_rights_inclusive_society",
  total_entities: 8,
  avg_composite: 60.33,
  confidence_score: 0.87,
  avg_estimated_disability_rights_inclusive_society_index: 6.03,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_crpd_implementation_report_2023",
    "human_rights_watch_disability_2023",
    "international_disability_alliance_2022",
    "who_disability_world_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[disability-rights-inclusive-society-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-inclusive-society-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
