import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Arms Embargo Violations Rights Engine Agent",
  domain: "arms_embargo_violations_rights",
  total_entities: 8,
  avg_composite: 60.51,
  confidence_score: 0.87,
  avg_estimated_arms_embargo_violations_rights_index: 6.05,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_panel_experts_arms_embargo_reports_2023",
    "sipri_arms_transfers_database_2023",
    "amnesty_international_arms_flows_conflict_zones_2023",
    "icrc_ihl_arms_embargo_compliance_review_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[arms-embargo-violations-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arms-embargo-violations-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
