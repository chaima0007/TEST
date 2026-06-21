import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Organ Trafficking Body Autonomy Rights Engine Agent",
  domain: "organ_trafficking_body_autonomy_rights",
  total_entities: 8,
  avg_composite: 59.41,
  confidence_score: 0.87,
  avg_estimated_organ_trafficking_body_autonomy_rights_index: 5.94,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "china_tribunal_2019_report",
    "who_global_observatory_transplantation",
    "declaration_of_istanbul_custodian_group",
    "interpol_trafficking_human_beings_reports",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[organ-trafficking-body-autonomy-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/organ-trafficking-body-autonomy-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
