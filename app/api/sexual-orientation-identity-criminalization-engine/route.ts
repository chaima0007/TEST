import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Sexual Orientation Identity Criminalization Engine Agent",
  domain: "sexual_orientation_identity_criminalization",
  total_entities: 8,
  avg_composite: 58.78,
  confidence_score: 0.88,
  avg_estimated_sexual_orientation_identity_criminalization_index: 5.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilga_world_state_sponsored_homophobia_2023",
    "human_rights_watch_lgbtq_report_2023",
    "amnesty_sexual_orientation_criminalization_2022",
    "un_ohchr_sogi_discrimination_2022",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[sexual-orientation-identity-criminalization-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-orientation-identity-criminalization-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
