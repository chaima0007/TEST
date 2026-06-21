import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Water Sanitation Rights Engine Agent",
  domain: "water_sanitation_rights",
  total_entities: 8,
  avg_composite: 59.55,
  confidence_score: 0.91,
  avg_estimated_water_sanitation_rights_index: 5.95,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "who_unicef_jmp_wash_progress_2023",
    "un_sr_safe_drinking_water_sanitation_2023",
    "wateraid_water_sanitation_crisis_2023",
    "sdg6_monitoring_report_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "CD", name: "RDC (République démocratique du Congo)", composite_score: 86.75, risk_level: "critique", estimated_water_sanitation_rights_index: 8.68 },
    { entity_id: "NE", name: "Niger", composite_score: 83.9, risk_level: "critique", estimated_water_sanitation_rights_index: 8.39 },
    { entity_id: "HT", name: "Haïti", composite_score: 81.6, risk_level: "critique", estimated_water_sanitation_rights_index: 8.16 },
    { entity_id: "ET", name: "Éthiopie", composite_score: 75.5, risk_level: "critique", estimated_water_sanitation_rights_index: 7.55 },
    { entity_id: "NG", name: "Nigeria", composite_score: 56.75, risk_level: "élevé", estimated_water_sanitation_rights_index: 5.67 },
    { entity_id: "PK", name: "Pakistan", composite_score: 53.45, risk_level: "élevé", estimated_water_sanitation_rights_index: 5.34 },
    { entity_id: "IN", name: "Inde rurale", composite_score: 34.0, risk_level: "modéré", estimated_water_sanitation_rights_index: 3.4 },
    { entity_id: "DK", name: "Danemark (modèle WASH)", composite_score: 4.45, risk_level: "faible", estimated_water_sanitation_rights_index: 0.45 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[water-sanitation-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-sanitation-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
