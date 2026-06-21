import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Arms Trade Civilian Harm Engine Agent",
  domain: "arms_trade_civilian_harm",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.88,
  avg_estimated_arms_trade_civilian_harm_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["sipri_arms_transfers_database_2023","action_on_armed_violence_ewipa_report_2023","amnesty_international_arms_trade_report_2023","arms_control_association_att_implementation_2023"],
  critical_alerts: [],
  entities: []
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[arms-trade-civilian-harm-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arms-trade-civilian-harm-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
