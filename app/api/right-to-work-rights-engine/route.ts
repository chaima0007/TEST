import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-work-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Work Rights Engine Agent",
  domain: "right_to_work_rights",
  total_entities: 8,
  avg_composite: 60.51,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Qatar — Kafala système, 6 500 morts Coupe du Monde construction, passeports confisqués",
    "Corée du Nord — Travail forcé État, exportation main d'oeuvre Russie/Chine, zéro syndicats",
    "Éthiopie/Bangladesh — Textile sweatshops, salaire 40$/mois, heures illimitées, feux Rana Plaza",
  ],
  critical_alerts: [
    "Qatar: forced_labor_conditions",
    "Corée du Nord: forced_labor_conditions",
    "Éthiopie/Bangladesh: decent_work_denial",
    "Arabie Saoudite: union_access_denial",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_work_rights_index: 6.05,
  entities: [
    {
      entity_id: "RTW-001",
      name: "Qatar — Kafala système, 6 500 morts Coupe du Monde construction, passeports confisqués",
      country: "Qatar",
      decent_work_denial_score: 97.0,
      forced_labor_conditions_score: 96.0,
      union_access_denial_score: 95.0,
      precarious_employment_score: 94.0,
      composite_score: 95.65,
      risk_level: "critique",
      primary_pattern: "forced_labor_conditions",
      estimated_right_to_work_rights_index: 9.57,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-002",
      name: "Corée du Nord — Travail forcé État, exportation main d'oeuvre Russie/Chine, zéro syndicats",
      country: "Corée du Nord",
      decent_work_denial_score: 91.0,
      forced_labor_conditions_score: 93.0,
      union_access_denial_score: 92.0,
      precarious_employment_score: 89.0,
      composite_score: 91.35,
      risk_level: "critique",
      primary_pattern: "forced_labor_conditions",
      estimated_right_to_work_rights_index: 9.14,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-003",
      name: "Éthiopie/Bangladesh — Textile sweatshops, salaire 40$/mois, heures illimitées, feux Rana Plaza",
      country: "Éthiopie/Bangladesh",
      decent_work_denial_score: 85.0,
      forced_labor_conditions_score: 83.0,
      union_access_denial_score: 84.0,
      precarious_employment_score: 87.0,
      composite_score: 84.65,
      risk_level: "critique",
      primary_pattern: "decent_work_denial",
      estimated_right_to_work_rights_index: 8.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-004",
      name: "Arabie Saoudite — Travailleurs migrants kafala, 12M sans droits, licenciements arbitraires",
      country: "Arabie Saoudite",
      decent_work_denial_score: 77.0,
      forced_labor_conditions_score: 79.0,
      union_access_denial_score: 78.0,
      precarious_employment_score: 75.0,
      composite_score: 77.35,
      risk_level: "critique",
      primary_pattern: "union_access_denial",
      estimated_right_to_work_rights_index: 7.74,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-005",
      name: "USA — Gig economy 60M, Uber/Amazon workers' rights, syndicats 10%, salaire minimum 7.25$",
      country: "USA",
      decent_work_denial_score: 54.0,
      forced_labor_conditions_score: 52.0,
      union_access_denial_score: 56.0,
      precarious_employment_score: 58.0,
      composite_score: 54.8,
      risk_level: "élevé",
      primary_pattern: "precarious_employment",
      estimated_right_to_work_rights_index: 5.48,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-006",
      name: "Inde — 90% économie informelle, MGNREGA insuffisant, bonded labour 23M",
      country: "Inde",
      decent_work_denial_score: 46.0,
      forced_labor_conditions_score: 48.0,
      union_access_denial_score: 44.0,
      precarious_employment_score: 50.0,
      composite_score: 46.8,
      risk_level: "élevé",
      primary_pattern: "precarious_employment",
      estimated_right_to_work_rights_index: 4.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-007",
      name: "France — Ubérisation, auto-entrepreneurs sans protection, réforme retraites contestée",
      country: "France",
      decent_work_denial_score: 28.0,
      forced_labor_conditions_score: 26.0,
      union_access_denial_score: 24.0,
      precarious_employment_score: 30.0,
      composite_score: 26.9,
      risk_level: "modéré",
      primary_pattern: "precarious_employment",
      estimated_right_to_work_rights_index: 2.69,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTW-008",
      name: "Allemagne/Danemark — Co-gestion syndicale, salaire min 12€+, protection chômage universelle",
      country: "Allemagne/Danemark",
      decent_work_denial_score: 7.0,
      forced_labor_conditions_score: 6.0,
      union_access_denial_score: 8.0,
      precarious_employment_score: 5.0,
      composite_score: 6.6,
      risk_level: "faible",
      primary_pattern: "union_access_denial",
      estimated_right_to_work_rights_index: 0.66,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-work-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
