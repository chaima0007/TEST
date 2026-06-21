import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Mining Extraction Community Rights Engine Agent",
  domain: "mining_extraction_community_rights",
  total_entities: 8,
  avg_composite: 57.83,
  confidence_score: 0.86,
  avg_estimated_mining_extraction_community_rights_index: 5.78,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "oecd_due_diligence_guidance_minerals_conflict_affected_2016",
    "un_guiding_principles_business_human_rights_extractives_2023",
    "global_witness_mining_community_displacement_report_2023",
    "ipcc_environmental_pollution_mining_indigenous_communities_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[mining-extraction-community-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mining-extraction-community-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
