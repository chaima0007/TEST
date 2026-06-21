import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Digital Divide Internet Access Rights Engine Agent",
  domain: "digital_divide_internet_access_rights",
  total_entities: 8,
  avg_composite: 54.56,
  confidence_score: 0.86,
  avg_estimated_digital_divide_internet_access_rights_index: 5.46,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["itu_digital_inclusion_2023","un_sr_extreme_poverty_digital_2022","alliance_for_affordable_internet_2023","web_foundation_digital_rights_2022"],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[digital-divide-internet-access-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-divide-internet-access-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
