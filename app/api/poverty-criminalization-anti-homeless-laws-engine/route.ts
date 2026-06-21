import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Poverty Criminalization Anti Homeless Laws Engine Agent",
  domain: "poverty_criminalization_anti_homeless_laws",
  total_entities: 8,
  avg_composite: 53.29,
  confidence_score: 0.89,
  avg_estimated_poverty_criminalization_anti_homeless_laws_index: 5.33,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["nlchp_criminalizing_homelessness_2023","aclu_poverty_criminalization_2022","human_rights_watch_homelessness_2023","un_housing_rapporteur_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[poverty-criminalization-anti-homeless-laws-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/poverty-criminalization-anti-homeless-laws-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
