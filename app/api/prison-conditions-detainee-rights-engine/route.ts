import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Prison Conditions Detainee Rights Engine Agent",
  domain: "prison_conditions_detainee_rights",
  total_entities: 8,
  avg_composite: 60.66,
  confidence_score: 0.89,
  avg_estimated_prison_conditions_detainee_rights_index: 6.07,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_subcommittee_prevention_torture_2023",
    "human_rights_watch_prisons_2023",
    "amnesty_international_detention_2022",
    "penal_reform_international_global_prison_trends_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "VEN", name: "Venezuela", composite_score: 89.1, risk_level: "critique", estimated_prison_conditions_detainee_rights_index: 8.91 },
    { entity_id: "LBY", name: "Libye", composite_score: 87.9, risk_level: "critique", estimated_prison_conditions_detainee_rights_index: 8.79 },
    { entity_id: "RUS", name: "Russie", composite_score: 81.75, risk_level: "critique", estimated_prison_conditions_detainee_rights_index: 8.18 },
    { entity_id: "ETH", name: "Éthiopie", composite_score: 81.6, risk_level: "critique", estimated_prison_conditions_detainee_rights_index: 8.16 },
    { entity_id: "SLV", name: "El Salvador", composite_score: 54.15, risk_level: "élevé", estimated_prison_conditions_detainee_rights_index: 5.42 },
    { entity_id: "PHL", name: "Philippines", composite_score: 51.0, risk_level: "élevé", estimated_prison_conditions_detainee_rights_index: 5.1 },
    { entity_id: "USA", name: "États-Unis", composite_score: 35.15, risk_level: "modéré", estimated_prison_conditions_detainee_rights_index: 3.51 },
    { entity_id: "DNK", name: "Danemark", composite_score: 4.65, risk_level: "faible", estimated_prison_conditions_detainee_rights_index: 0.47 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[prison-conditions-detainee-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-conditions-detainee-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
