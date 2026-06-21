import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Transitional Justice Truth Commission Engine Agent",
  domain: "transitional_justice_truth_commission",
  total_entities: 8, avg_composite: 57.49, confidence_score: 0.87,
  avg_estimated_transitional_justice_truth_commission_index: 5.75,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ictj_transitional_justice_report_2023","un_ohchr_truth_commissions_2022","amnesty_reparations_2023","icc_transitional_justice_2023"],
  critical_alerts: [], entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[transitional-justice-truth-commission-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/transitional-justice-truth-commission-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
