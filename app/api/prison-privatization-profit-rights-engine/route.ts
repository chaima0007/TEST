import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Prison Privatization Profit Rights Engine Agent",
  domain: "prison_privatization_profit_rights",
  total_entities: 8,
  avg_composite: 58.54,
  confidence_score: 0.86,
  avg_estimated_prison_privatization_profit_rights_index: 5.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "aclu_private_prison_abuses_report_2023",
    "un_special_rapporteur_torture_detention_2023",
    "prison_policy_initiative_private_incarceration_2023",
    "justice_policy_institute_private_prison_lobbying_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[prison-privatization-profit-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-privatization-profit-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
