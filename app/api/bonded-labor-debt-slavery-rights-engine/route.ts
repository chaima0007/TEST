import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const MOCK = {
  agent: "Bonded Labor Debt Slavery Rights Engine Agent",
  domain: "bonded_labor_debt_slavery_rights",
  total_entities: 8, avg_composite: 63.32, confidence_score: 0.88,
  avg_estimated_bonded_labor_debt_slavery_rights_index: 6.33,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["ilo_forced_labour_global_estimates_2022","walk_free_global_slavery_index_2023","anti_slavery_international_2023","un_special_rapporteur_slavery_2022"],
  critical_alerts: [], entities: [],
};
export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[bonded-labor-debt-slavery-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/bonded-labor-debt-slavery-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
