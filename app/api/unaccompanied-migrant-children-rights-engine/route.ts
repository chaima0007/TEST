import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Unaccompanied Migrant Children Rights Engine Agent",
  domain: "unaccompanied_migrant_children_rights",
  total_entities: 8,
  avg_composite: 63.20,
  confidence_score: 0.88,
  avg_estimated_unaccompanied_migrant_children_rights_index: 6.32,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unhcr_unaccompanied_children_report_2023",
    "unicef_migration_children_2023",
    "human_rights_watch_child_detention_2023",
    "eu_asylum_procedures_regulation_2024",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[unaccompanied-migrant-children-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/unaccompanied-migrant-children-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
