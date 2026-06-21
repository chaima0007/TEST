import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Human Trafficking Modern Slavery Engine Agent",
  domain: "human_trafficking_modern_slavery",
  total_entities: 8,
  avg_composite: 62.02,
  confidence_score: 0.89,
  avg_estimated_human_trafficking_modern_slavery_index: 6.20,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "ilo_global_estimates_modern_slavery_2022",
    "unodc_global_trafficking_report_2023",
    "walk_free_global_slavery_index_2023",
    "polaris_project_national_human_trafficking_hotline",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[human_trafficking_modern_slavery-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-trafficking-modern-slavery-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
