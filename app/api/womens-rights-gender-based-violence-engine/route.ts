import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Womens Rights Gender Based Violence Engine Agent",
  domain: "womens_rights_gender_based_violence",
  total_entities: 8,
  avg_composite: 62.84,
  confidence_score: 0.88,
  avg_estimated_womens_rights_gender_based_violence_index: 6.28,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_women_gender_based_violence_report_2023","who_global_prevalence_violence_against_women_2021","girls_not_brides_child_marriage_database_2023","equality_now_womens_rights_global_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[womens-rights-gender-based-violence-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/womens-rights-gender-based-violence-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
