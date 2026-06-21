import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Forced Disappearance Extrajudicial Killing Engine Agent",
  domain: "forced_disappearance_extrajudicial_killing",
  total_entities: 8,
  avg_composite: 59.39,
  confidence_score: 0.89,
  avg_estimated_forced_disappearance_extrajudicial_killing_index: 5.94,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "un_committee_enforced_disappearances_2023",
    "amnesty_international_extrajudicial_killings_2023",
    "human_rights_watch_disappearances_database",
    "trial_international_fight_impunity_report_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[forced-disappearance-extrajudicial-killing-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-disappearance-extrajudicial-killing-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
