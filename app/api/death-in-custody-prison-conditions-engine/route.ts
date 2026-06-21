import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Death In Custody Prison Conditions Engine Agent",
  domain: "death_in_custody_prison_conditions",
  total_entities: 8,
  avg_composite: 62.28,
  confidence_score: 0.88,
  avg_estimated_death_in_custody_prison_conditions_index: 6.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_special_rapporteur_torture_detention_2023",
    "penal_reform_international_global_prison_trends_2023",
    "amnesty_international_death_in_custody_2023",
    "human_rights_watch_prison_conditions_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[death-in-custody-prison-conditions-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/death-in-custody-prison-conditions-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
