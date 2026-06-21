import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Minority Language Cultural Rights Engine Agent",
  domain: "minority_language_cultural_rights",
  total_entities: 8,
  avg_composite: 56.40,
  confidence_score: 0.89,
  avg_estimated_minority_language_cultural_rights_index: 5.64,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_declaration_minority_rights_implementation_2023",
    "minority_rights_group_world_directory_2023",
    "ethnologue_endangered_languages_2023",
    "un_sr_minority_issues_reports_2022",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "CN", name: "Chine (Ouïghours/Tibétains)", composite_score: 85.2, risk_level: "critique", estimated_minority_language_cultural_rights_index: 8.52 },
    { entity_id: "MM", name: "Myanmar (Rohingyas)", composite_score: 81.6, risk_level: "critique", estimated_minority_language_cultural_rights_index: 8.16 },
    { entity_id: "TR", name: "Turquie (Kurdes)", composite_score: 72.8, risk_level: "critique", estimated_minority_language_cultural_rights_index: 7.28 },
    { entity_id: "IR", name: "Iran (Kurdes/Baloutches)", composite_score: 70.3, risk_level: "critique", estimated_minority_language_cultural_rights_index: 7.03 },
    { entity_id: "RU", name: "Russie (peuples indigènes)", composite_score: 52.6, risk_level: "élevé", estimated_minority_language_cultural_rights_index: 5.26 },
    { entity_id: "IN", name: "Inde (minorités du nord-est)", composite_score: 47.8, risk_level: "élevé", estimated_minority_language_cultural_rights_index: 4.78 },
    { entity_id: "FR", name: "France (langues régionales)", composite_score: 28.85, risk_level: "modéré", estimated_minority_language_cultural_rights_index: 2.89 },
    { entity_id: "CA", name: "Canada (langues autochtones en rétablissement)", composite_score: 12.05, risk_level: "faible", estimated_minority_language_cultural_rights_index: 1.21 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[minority-language-cultural-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/minority-language-cultural-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
