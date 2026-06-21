import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Human Rights Defenders Assassination Engine Agent",
  domain: "human_rights_defenders_assassination",
  total_entities: 8,
  avg_composite: 59.87,
  confidence_score: 0.87,
  avg_estimated_human_rights_defenders_assassination_index: 5.99,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "front_line_defenders_2023",
    "global_witness_defenders_2023",
    "amnesty_hrd_report_2023",
    "ohchr_reprisals_report_2022",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[human-rights-defenders-assassination-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-rights-defenders-assassination-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
