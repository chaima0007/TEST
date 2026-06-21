import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Witchcraft Accusation Persecution Engine Agent",
  domain: "witchcraft_accusation_persecution",
  total_entities: 8,
  avg_composite: 60.60,
  confidence_score: 0.86,
  avg_estimated_witchcraft_accusation_persecution_index: 6.06,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_ohchr_witchcraft_accusations_2023",
    "human_rights_watch_witchcraft_persecution_2022",
    "amnesty_international_witch_camps_2023",
    "unicef_child_witchcraft_accusations_africa_2022",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[witchcraft-accusation-persecution-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/witchcraft-accusation-persecution-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
