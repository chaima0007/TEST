import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Media Freedom Journalist Protection Engine Agent",
  domain: "media_freedom_journalist_protection",
  total_entities: 8,
  avg_composite: 62.29,
  confidence_score: 0.91,
  avg_estimated_media_freedom_journalist_protection_index: 6.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "rsf_world_press_freedom_index_2023",
    "cpj_journalist_killed_imprisoned_2023",
    "ifj_press_freedom_report_2023",
    "freedom_house_freedom_of_the_press_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "ERI", name: "Érythrée", composite_score: 89.35, risk_level: "critique", estimated_media_freedom_journalist_protection_index: 8.93 },
    { entity_id: "PRK", name: "Corée du Nord", composite_score: 91.0, risk_level: "critique", estimated_media_freedom_journalist_protection_index: 9.1 },
    { entity_id: "TKM", name: "Turkménistan", composite_score: 86.15, risk_level: "critique", estimated_media_freedom_journalist_protection_index: 8.62 },
    { entity_id: "RUS", name: "Russie", composite_score: 82.85, risk_level: "critique", estimated_media_freedom_journalist_protection_index: 8.28 },
    { entity_id: "CHN", name: "Chine", composite_score: 59.65, risk_level: "élevé", estimated_media_freedom_journalist_protection_index: 5.96 },
    { entity_id: "MMR", name: "Myanmar", composite_score: 54.15, risk_level: "élevé", estimated_media_freedom_journalist_protection_index: 5.42 },
    { entity_id: "MEX", name: "Mexique", composite_score: 31.25, risk_level: "modéré", estimated_media_freedom_journalist_protection_index: 3.12 },
    { entity_id: "FIN", name: "Finlande", composite_score: 3.95, risk_level: "faible", estimated_media_freedom_journalist_protection_index: 0.4 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[media-freedom-journalist-protection-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/media-freedom-journalist-protection-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
