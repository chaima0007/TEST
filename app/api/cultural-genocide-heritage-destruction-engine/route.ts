import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cultural-genocide-heritage-destruction-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Cultural Genocide Heritage Destruction Engine Agent",
  domain: "cultural_genocide_heritage_destruction",
  total_entities: 8,
  avg_composite: 69.62,
  confidence_score: 0.88,
  avg_estimated_cultural_genocide_heritage_destruction_index: 6.96,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unesco_heritage_destruction_2023",
    "icc_cultural_property_war_crimes_2022",
    "un_sr_cultural_rights_2023",
    "blue_shield_international_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cultural-genocide-heritage-destruction-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
