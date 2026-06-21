import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Nomadic Pastoralist Peoples Rights Engine Agent",
  domain: "nomadic_pastoralist_peoples_rights",
  total_entities: 8,
  avg_composite: 58.76,
  confidence_score: 0.86,
  avg_estimated_nomadic_pastoralist_peoples_rights_index: 5.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_special_rapporteur_indigenous_peoples_pastoralist_2023",
    "iucn_pastoralist_land_rights_report_2023",
    "fao_nomadic_pastoral_systems_review_2023",
    "hrw_forced_sedentarization_africa_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[nomadic-pastoralist-peoples-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nomadic-pastoralist-peoples-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
