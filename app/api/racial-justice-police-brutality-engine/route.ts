import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Racial Justice Police Brutality Engine Agent",
  domain: "racial_justice_police_brutality",
  total_entities: 8,
  avg_composite: 63.41,
  confidence_score: 0.88,
  avg_estimated_racial_justice_police_brutality_index: 6.34,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "mapping_police_violence_database_2023",
    "human_rights_watch_racial_justice_2023",
    "amnesty_international_police_brutality_2023",
    "un_special_rapporteur_racism_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[racial-justice-police-brutality-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/racial-justice-police-brutality-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
