import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Witch Hunt Accusation Persecution Engine Agent",
  domain: "witch_hunt_accusation_persecution",
  total_entities: 8, avg_composite: 56.34, confidence_score: 0.87,
  avg_estimated_witch_hunt_accusation_persecution_index: 5.63,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_ohchr_witchcraft_accusations_2022","belief_based_abuse_global_report_2023","harmful_traditional_practices_un_2023","human_rights_watch_witchcraft_2022"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[witch-hunt-accusation-persecution-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/witch-hunt-accusation-persecution-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
