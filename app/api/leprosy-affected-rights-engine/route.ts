import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Leprosy Affected Rights Engine Agent",
  domain: "leprosy_affected_rights",
  total_entities: 8,
  avg_composite: 60.12,
  confidence_score: 0.89,
  avg_estimated_leprosy_affected_rights_index: 6.01,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["who_leprosy_report_2023","ilep_leprosy_stigma_2023","human_rights_watch_leprosy_2022","un_special_rapporteur_leprosy_2021"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[leprosy-affected-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/leprosy-affected-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
