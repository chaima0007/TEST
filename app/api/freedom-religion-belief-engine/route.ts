import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Freedom of Religion & Belief Engine Agent",
  domain: "freedom_religion_belief",
  total_entities: 8,
  avg_composite: 61.33,
  confidence_score: 0.90,
  avg_estimated_freedom_religion_belief_index: 6.13,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "uscirf_annual_report_2023",
    "open_doors_world_watch_list_2023",
    "human_rights_watch_religion_freedom_2022",
    "un_sr_freedom_religion_belief_2023",
  ],
  critical_alerts: [],
  entities: [
    { id: "CHN", name: "Chine", composite_score: 84.15, risk_level: "critique", estimated_freedom_religion_belief_index: 8.42 },
    { id: "IRN", name: "Iran", composite_score: 83.5, risk_level: "critique", estimated_freedom_religion_belief_index: 8.35 },
    { id: "SAU", name: "Arabie Saoudite", composite_score: 81.6, risk_level: "critique", estimated_freedom_religion_belief_index: 8.16 },
    { id: "MMR", name: "Myanmar", composite_score: 80.85, risk_level: "critique", estimated_freedom_religion_belief_index: 8.09 },
    { id: "PAK", name: "Pakistan", composite_score: 58.25, risk_level: "élevé", estimated_freedom_religion_belief_index: 5.83 },
    { id: "NGA", name: "Nigeria", composite_score: 57.65, risk_level: "élevé", estimated_freedom_religion_belief_index: 5.77 },
    { id: "IND", name: "Inde", composite_score: 37.5, risk_level: "modéré", estimated_freedom_religion_belief_index: 3.75 },
    { id: "NOR", name: "Norvège", composite_score: 7.15, risk_level: "faible", estimated_freedom_religion_belief_index: 0.72 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[freedom-religion-belief-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/freedom-religion-belief-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
