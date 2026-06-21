import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Climate Justice Loss Damage Rights Engine Agent",
  domain: "climate_justice_loss_damage_rights",
  total_entities: 8,
  avg_composite: 57.65,
  confidence_score: 0.86,
  avg_estimated_climate_justice_loss_damage_rights_index: 5.77,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unfccc_loss_damage_mechanism_cop27_cop28_reports",
    "ipcc_sixth_assessment_report_impacts_adaptation",
    "hrw_climate_justice_human_rights_documentation",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[climate-justice-loss-damage-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-justice-loss-damage-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
