import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK: Record<string, unknown> = {
  agent: "Digital Surveillance Privacy Rights Engine Agent",
  domain: "digital_surveillance_privacy_rights",
  total_entities: 8,
  avg_composite: 59.78,
  confidence_score: 0.88,
  avg_estimated_digital_surveillance_privacy_rights_index: 5.98,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [],
  critical_alerts: [],
  data_sources: [
    "freedom_house_freedom_net_2023",
    "privacy_international_surveillance_database",
    "citizen_lab_targeted_threat_lab_2023",
    "electronic_frontier_foundation_global_surveillance_2023",
  ],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[digital_surveillance_privacy_rights-engine] SWARM_API_URL not set — returning mock");
    return sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-privacy-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
