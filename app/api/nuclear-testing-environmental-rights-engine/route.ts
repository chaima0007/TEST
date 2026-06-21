import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Nuclear Testing Environmental Rights Engine Agent",
  domain: "nuclear_testing_environmental_rights",
  total_entities: 8,
  avg_composite: 62.11,
  confidence_score: 0.86,
  avg_estimated_nuclear_testing_environmental_rights_index: 6.21,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "icrc_nuclear_weapons_humanitarian_law_2023",
    "un_special_rapporteur_toxic_substances_nuclear_2023",
    "ippnw_nuclear_testing_health_effects_2023",
    "ican_humanitarian_impact_nuclear_testing_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[nuclear-testing-environmental-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-testing-environmental-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
