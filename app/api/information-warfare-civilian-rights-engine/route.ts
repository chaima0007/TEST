import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Information Warfare Civilian Rights Engine Agent",
  domain: "information_warfare_civilian_rights",
  total_entities: 8,
  avg_composite: 63.20,
  confidence_score: 0.88,
  avg_estimated_information_warfare_civilian_rights_index: 6.32,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "eu_disinfo_lab_report_2023",
    "freedom_house_freedom_on_net_2023",
    "stanford_internet_observatory_2023",
    "un_sr_freedom_expression_disinfo_2023",
  ],
  critical_alerts: [],
  entities: [],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[information-warfare-civilian-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/information-warfare-civilian-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
