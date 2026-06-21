import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Surveillance Facial Recognition Rights Engine Agent",
  domain: "surveillance_facial_recognition_rights",
  total_entities: 8,
  avg_composite: 61.85,
  confidence_score: 0.89,
  avg_estimated_surveillance_facial_recognition_rights_index: 6.19,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ai_now_institute_facial_recognition_report_2023",
    "human_rights_watch_surveillance_state_2023",
    "amnesty_ban_facial_recognition_2023",
    "eu_ai_act_biometric_surveillance_2024",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[surveillance-facial-recognition-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/surveillance-facial-recognition-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
