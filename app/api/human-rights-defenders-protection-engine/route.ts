import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Human Rights Defenders Protection Engine Agent",
  domain: "human_rights_defenders_protection",
  total_entities: 8,
  avg_composite: 61.46,
  confidence_score: 0.85,
  avg_estimated_human_rights_defenders_protection_index: 6.15,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "front_line_defenders_annual_report_hrd_killings",
    "global_witness_hrd_murders_tracking_database",
    "civicus_ngo_restriction_closing_space_monitor",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[human-rights-defenders-protection-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-defenders-protection-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
