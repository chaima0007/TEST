import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Antipersonnel Mines Victim Rights Engine Agent",
  domain: "antipersonnel_mines_victim_rights",
  total_entities: 8, avg_composite: 57.26, confidence_score: 0.87,
  avg_estimated_antipersonnel_mines_victim_rights_index: 5.73,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["icbl_landmine_monitor_2023","mine_action_review_2023","icrc_mine_ban_treaty_2022","un_mine_action_service_2023"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[antipersonnel-mines-victim-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/antipersonnel-mines-victim-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
