import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Colonial Reparations Transitional Justice Engine Agent",
  domain: "colonial_reparations_transitional_justice",
  total_entities: 8,
  avg_composite: 57.83,
  confidence_score: 0.86,
  avg_estimated_colonial_reparations_transitional_justice_index: 5.78,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "caricom_reparations_commission_ten_point_plan_2014",
    "un_special_rapporteur_contemporary_forms_racism_reparations_2023",
    "international_center_transitional_justice_colonial_harm_2023",
    "truth_reconciliation_commission_canada_94_calls_action_2015",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[colonial-reparations-transitional-justice-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/colonial-reparations-transitional-justice-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
