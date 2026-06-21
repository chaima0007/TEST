import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Human Rights Education Rights Engine Agent",
  domain: "human_rights_education_rights",
  total_entities: 8,
  avg_composite: 56.66,
  confidence_score: 0.86,
  avg_estimated_human_rights_education_rights_index: 5.67,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_declaration_hre_2011","amnesty_human_rights_education_2022","ohchr_hre_report_2023","global_campaign_hre_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[human-rights-education-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-education-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
