import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Medical Experimentation Ethics Rights Engine Agent",
  domain: "medical_experimentation_ethics_rights",
  total_entities: 8,
  avg_composite: 61.06,
  confidence_score: 0.87,
  avg_estimated_medical_experimentation_ethics_rights_index: 6.11,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "world_medical_association_declaration_helsinki_2023",
    "nuremberg_code_legacy_report_2023",
    "who_clinical_trials_ethics_2022",
    "human_rights_watch_medical_coercion_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[medical-experimentation-ethics-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/medical-experimentation-ethics-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
