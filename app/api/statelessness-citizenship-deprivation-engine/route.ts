import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Statelessness Citizenship Deprivation Engine Agent",
  domain: "statelessness_citizenship_deprivation",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.90,
  avg_estimated_statelessness_citizenship_deprivation_index: 6.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "unhcr_global_trends_statelessness_2023",
    "institute_statelessness_inclusion_2023",
    "un_1954_convention_stateless_persons",
    "human_rights_watch_statelessness_2022",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "MMR_rohingya", name: "Myanmar — Rohingyas (800k apatrides)", composite_score: 93.0, risk_level: "critique", estimated_statelessness_citizenship_deprivation_index: 9.3 },
    { entity_id: "KWT_bidoun", name: "Koweït — Bidouns sans nationalité", composite_score: 83.35, risk_level: "critique", estimated_statelessness_citizenship_deprivation_index: 8.33 },
    { entity_id: "DOM_haitian_origin", name: "République Dominicaine — Dominicains d'origine haïtienne", composite_score: 80.9, risk_level: "critique", estimated_statelessness_citizenship_deprivation_index: 8.09 },
    { entity_id: "BTN_nepali_bhutanese", name: "Bhoutan — Bhoutanais népalais expulsés", composite_score: 78.4, risk_level: "critique", estimated_statelessness_citizenship_deprivation_index: 7.84 },
    { entity_id: "KEN_nubians", name: "Kenya — Nubiens et reconnaissance citoyenneté", composite_score: 59.85, risk_level: "élevé", estimated_statelessness_citizenship_deprivation_index: 5.99 },
    { entity_id: "SAH_sahel_undocumented", name: "Sahel — Populations sans-papiers transfrontalières", composite_score: 59.0, risk_level: "élevé", estimated_statelessness_citizenship_deprivation_index: 5.9 },
    { entity_id: "LVA_non_citizens", name: "Lettonie — Non-citoyens (statut résiduel post-URSS)", composite_score: 30.95, risk_level: "modéré", estimated_statelessness_citizenship_deprivation_index: 3.09 },
    { entity_id: "UNHCR_reduction_model", name: "UNHCR — Modèle de réduction de l'apatridie", composite_score: 9.0, risk_level: "faible", estimated_statelessness_citizenship_deprivation_index: 0.9 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[statelessness-citizenship-deprivation-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-citizenship-deprivation-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
