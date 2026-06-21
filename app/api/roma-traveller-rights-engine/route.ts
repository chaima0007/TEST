import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Roma Traveller Rights Engine Agent",
  domain: "roma_traveller_rights",
  total_entities: 8, avg_composite: 56.77, confidence_score: 0.87,
  avg_estimated_roma_traveller_rights_index: 5.68,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["errc_roma_rights_2023","council_europe_roma_strategy_2030","european_roma_rights_centre_2022","fra_roma_survey_2021"],
  critical_alerts: [], entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[roma-traveller-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/roma-traveller-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
