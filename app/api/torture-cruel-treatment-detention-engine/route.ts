import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Torture Cruel Treatment Detention Engine Agent",
  domain: "torture_cruel_treatment_detention",
  total_entities: 8,
  avg_composite: 63.69,
  confidence_score: 0.90,
  avg_estimated_torture_cruel_treatment_detention_index: 6.37,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_committee_against_torture_annual_report_2023","amnesty_international_torture_2023","human_rights_watch_torture_detention_database","association_prevention_torture_global_report_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[torture-cruel-treatment-detention-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/torture-cruel-treatment-detention-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
