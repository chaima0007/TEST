import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Reparations Genocide Victims Engine Agent",
  domain: "reparations_genocide_victims",
  total_entities: 8, avg_composite: 56.34, confidence_score: 0.87,
  avg_estimated_reparations_genocide_victims_index: 5.63,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["un_genocide_convention_implementation_2022","icc_reparations_framework_2023","redress_genocide_reparations_2023","ictj_reparations_2022"],
  critical_alerts: [], entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[reparations-genocide-victims-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/reparations-genocide-victims-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
