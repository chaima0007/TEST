import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Afrodescendant Reparations Rights Engine Agent",
  domain: "afrodescendant_reparations_rights",
  total_entities: 8,
  avg_composite: 63.10,
  confidence_score: 0.87,
  avg_estimated_afrodescendant_reparations_rights_index: 6.31,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_durban_declaration_programme_action_2001_review_2023",
    "caricom_reparations_commission_report_2023",
    "human_rights_watch_racial_justice_2023",
    "un_sr_racism_racial_discrimination_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[afrodescendant-reparations-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/afrodescendant-reparations-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
