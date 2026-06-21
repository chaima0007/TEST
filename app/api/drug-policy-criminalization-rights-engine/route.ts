import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Drug Policy Criminalization Rights Engine Agent",
  domain: "drug_policy_criminalization_rights",
  total_entities: 8,
  avg_composite: 60.15,
  confidence_score: 0.86,
  avg_estimated_drug_policy_criminalization_rights_index: 6.02,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "harm_reduction_international_drug_policy_2023",
    "human_rights_watch_drug_policy_rights_2023",
    "idpc_drug_policy_guide_2023",
    "amnesty_international_death_penalty_drugs_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[drug-policy-criminalization-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/drug-policy-criminalization-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
