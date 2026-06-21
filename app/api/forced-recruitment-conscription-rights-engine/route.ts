import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Forced Recruitment Conscription Rights Engine Agent",
  domain: "forced_recruitment_conscription_rights",
  total_entities: 8, avg_composite: 64.37, confidence_score: 0.88,
  avg_estimated_forced_recruitment_conscription_rights_index: 6.44,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["child_soldiers_international_2023","un_secretary_general_children_armed_conflict_2023","amnesty_conscription_rights_2022","human_rights_watch_conscientious_objectors_2023"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[forced-recruitment-conscription-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-recruitment-conscription-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
