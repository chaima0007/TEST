import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Street Children Rights Engine Agent",
  domain: "street_children_rights",
  total_entities: 8, avg_composite: 62.67, confidence_score: 0.88,
  avg_estimated_street_children_rights_index: 6.27,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["unicef_street_children_report_2023","consortium_street_children_2022","human_rights_watch_children_streets_2023","save_the_children_2022"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[street-children-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/street-children-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
