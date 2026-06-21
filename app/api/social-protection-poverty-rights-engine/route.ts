import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Social Protection Poverty Rights Engine Agent",
  domain: "social_protection_poverty_rights",
  total_entities: 8,
  avg_composite: 63.75,
  confidence_score: 0.86,
  avg_estimated_social_protection_poverty_rights_index: 6.38,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_world_social_protection_report_2022_2023",
    "world_bank_poverty_social_protection_2023",
    "un_special_rapporteur_extreme_poverty_2023",
    "oxfam_inequality_report_social_protection_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[social-protection-poverty-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/social-protection-poverty-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
