import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Satellite Surveillance Privacy Rights Engine Agent",
  domain: "satellite_surveillance_privacy_rights",
  total_entities: 8,
  avg_composite: 61.80,
  confidence_score: 0.89,
  avg_estimated_satellite_surveillance_privacy_rights_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "privacy_international_satellite_surveillance_2023",
    "un_sr_privacy_report_2023",
    "access_now_nso_group_report_2023",
    "eu_ai_act_remote_biometric_surveillance_2024",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[satellite-surveillance-privacy-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/satellite-surveillance-privacy-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
