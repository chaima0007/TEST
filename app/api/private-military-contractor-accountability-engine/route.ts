import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Private Military Contractor Accountability Engine Agent",
  domain: "private_military_contractor_accountability",
  total_entities: 8,
  avg_composite: 62.50,
  confidence_score: 0.87,
  avg_estimated_private_military_contractor_accountability_index: 6.25,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_working_group_mercenaries_2023",
    "human_rights_watch_pmc_accountability_2023",
    "amnesty_wagner_group_report_2023",
    "montreux_document_icrc_pmc_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[private-military-contractor-accountability-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/private-military-contractor-accountability-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
