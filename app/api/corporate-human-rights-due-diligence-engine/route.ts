import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Corporate Human Rights Due Diligence Engine Agent",
  domain: "corporate_human_rights_due_diligence",
  total_entities: 8,
  avg_composite: 59.74,
  confidence_score: 0.91,
  avg_estimated_corporate_human_rights_due_diligence_index: 5.97,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_guiding_principles_business_human_rights_2011",
    "eu_csddd_directive_2024",
    "business_human_rights_resource_centre_2023",
    "oecd_due_diligence_guidance_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "COD_cobalt_ev_batteries", name: "RDC — Cobalt chaînes batteries EV", composite_score: 88.65, risk_level: "critique", estimated_corporate_human_rights_due_diligence_index: 8.87 },
    { entity_id: "BGD_fast_fashion", name: "Bangladesh — Fast fashion (travail forcé)", composite_score: 82.35, risk_level: "critique", estimated_corporate_human_rights_due_diligence_index: 8.23 },
    { entity_id: "CIV_cocoa_child_labor", name: "Côte d'Ivoire — Cacao et travail enfants", composite_score: 79.6, risk_level: "critique", estimated_corporate_human_rights_due_diligence_index: 7.96 },
    { entity_id: "IDN_palm_oil", name: "Indonésie — Huile de palme déforestation", composite_score: 80.0, risk_level: "critique", estimated_corporate_human_rights_due_diligence_index: 8.0 },
    { entity_id: "THA_fishing_slavery", name: "Thaïlande — Esclavage dans la pêche", composite_score: 51.1, risk_level: "élevé", estimated_corporate_human_rights_due_diligence_index: 5.11 },
    { entity_id: "SLE_diamonds_conflict", name: "Sierra Leone — Diamants conflits", composite_score: 48.15, risk_level: "élevé", estimated_corporate_human_rights_due_diligence_index: 4.81 },
    { entity_id: "CHL_ARG_lithium", name: "Chili/Argentine — Lithium et communautés", composite_score: 34.1, risk_level: "modéré", estimated_corporate_human_rights_due_diligence_index: 3.41 },
    { entity_id: "APPLE_NIKE_compliance", name: "Apple/Nike — Conformité CSDDD/UNGPs", composite_score: 14.0, risk_level: "faible", estimated_corporate_human_rights_due_diligence_index: 1.4 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[corporate-human-rights-due-diligence-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-human-rights-due-diligence-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
