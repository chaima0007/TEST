import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[organ-trafficking-transplant-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Organ Trafficking Transplant Rights Engine Agent",
  domain: "organ_trafficking_transplant_rights",
  total_entities: 8,
  avg_composite: 60.36,
  confidence_score: 0.88,
  avg_estimated_organ_trafficking_transplant_rights_index: 6.04,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_sr_trafficking_persons_2023",
    "who_organ_trafficking_report_2022",
    "council_of_europe_organ_trafficking_2023",
    "declaracion_istanbul_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/organ-trafficking-transplant-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
