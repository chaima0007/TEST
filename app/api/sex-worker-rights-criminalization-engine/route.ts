import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Sex Worker Rights Criminalization Engine Agent",
  domain: "sex_worker_rights_criminalization",
  total_entities: 8,
  avg_composite: 62.10,
  confidence_score: 0.86,
  avg_estimated_sex_worker_rights_criminalization_index: 6.21,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "who_sex_work_hiv_prevention_2023",
    "amnesty_sex_work_policy_2016",
    "human_rights_watch_criminalization_2023",
    "unaids_sex_workers_report_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[sex-worker-rights-criminalization-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sex-worker-rights-criminalization-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
