import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "HIV AIDS Stigma Rights Engine Agent",
  domain: "hiv_aids_stigma_rights",
  total_entities: 8,
  avg_composite: 60.00,
  confidence_score: 0.89,
  avg_estimated_hiv_aids_stigma_rights_index: 6.00,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["unaids_global_aids_report_2023","human_rights_watch_hiv_2023","amnesty_hiv_criminalization_2022","who_hiv_stigma_report_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[hiv-aids-stigma-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hiv-aids-stigma-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
