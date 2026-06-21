import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Nuclear Victims Rights Engine Agent",
  domain: "nuclear_victims_rights",
  total_entities: 8,
  avg_composite: 55.73,
  confidence_score: 0.87,
  avg_estimated_nuclear_victims_rights_index: 5.57,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ican_nuclear_ban_monitor_2023","international_physicians_nuclear_war_2022","un_ohchr_nuclear_weapons_2022","marshal_islands_nuclear_legacy_report_2023"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[nuclear-victims-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-victims-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
