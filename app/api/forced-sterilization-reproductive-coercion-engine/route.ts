import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Forced Sterilization Reproductive Coercion Engine Agent",
  domain: "forced_sterilization_reproductive_coercion",
  total_entities: 8,
  avg_composite: 59.67,
  confidence_score: 0.87,
  avg_estimated_forced_sterilization_reproductive_coercion_index: 5.97,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "who_forced_sterilization_report_2014",
    "un_ohchr_reproductive_coercion_2022",
    "cedh_sterilization_judgments_2011",
    "amnesty_international_reproductive_rights_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[forced-sterilization-reproductive-coercion-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-sterilization-reproductive-coercion-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
