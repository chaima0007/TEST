import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Solitary Confinement Isolation Rights Engine Agent",
  domain: "solitary_confinement_isolation_rights",
  total_entities: 8,
  avg_composite: 59.51,
  confidence_score: 0.87,
  avg_estimated_solitary_confinement_isolation_rights_index: 5.95,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_nelson_mandela_rules_2015",
    "cpt_council_europe_reports",
    "hrw_solitary_confinement_investigations",
    "cglpl_france_rapports_annuels",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[solitary-confinement-isolation-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/solitary-confinement-isolation-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
