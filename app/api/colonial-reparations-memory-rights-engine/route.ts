import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[colonial-reparations-memory-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Colonial Reparations Memory Rights Engine Agent",
  domain: "colonial_reparations_memory_rights",
  total_entities: 8,
  avg_composite: 61.58,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    colonial_genocide_crime_denial_severity: 2,
    reparations_financial_compensation_denial: 3,
    indigenous_colonial_trauma_acknowledgment_deficit_gap: 2,
    cultural_patrimony_restitution_refusal_scale: 1,
  },
  top_risk_entities: [
    "France/Algérie — Guerre Algérie 1.5M Morts Déniés, Massacres Mai 1945 Non Reconnus, Archives Fermées & Harkis Abandonés",
    "Belgique/RDC — Léopold II 10M Morts Congo Reconnu 2020 Pas Réparations, Pillage Or/Caoutchouc & Patrice Lumumba",
    "UK/Caraïbes — Esclavage Indemnisation 2023 Debat, Plantation Profits Familles Royales, CARICOM 14 Points & Windrush",
  ],
  critical_alerts: [
    "France/Algérie: colonial_genocide_crime_denial_severity",
    "Belgique/RDC: reparations_financial_compensation_denial",
    "UK/Caraïbes: reparations_financial_compensation_denial",
    "Pays-Bas/Indonésie: colonial_genocide_crime_denial_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_colonial_reparations_memory_rights_index: 6.16,
  data_sources: [
    "caricom_reparations_commission_10_point_plan",
    "un_special_rapporteur_racism_reparations_report",
    "icom_restitution_cultural_heritage_global_review",
  ],
  entities: [
    {
      id: "CRM-001",
      name: "France/Algérie — Guerre Algérie 1.5M Morts Déniés, Massacres Mai 1945 Non Reconnus, Archives Fermées & Harkis Abandonés",
      country: "France/Algérie",
      colonial_genocide_crime_denial_severity_score: 95.0,
      cultural_patrimony_restitution_refusal_scale_score: 93.0,
      reparations_financial_compensation_denial_score: 93.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 91.0,
      composite_score: 93.2,
      risk_level: "critique",
      primary_pattern: "colonial_genocide_crime_denial_severity",
      estimated_colonial_reparations_memory_rights_index: 9.32,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-002",
      name: "Belgique/RDC — Léopold II 10M Morts Congo Reconnu 2020 Pas Réparations, Pillage Or/Caoutchouc & Patrice Lumumba",
      country: "Belgique/RDC",
      colonial_genocide_crime_denial_severity_score: 92.0,
      cultural_patrimony_restitution_refusal_scale_score: 90.0,
      reparations_financial_compensation_denial_score: 90.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 88.0,
      composite_score: 90.2,
      risk_level: "critique",
      primary_pattern: "reparations_financial_compensation_denial",
      estimated_colonial_reparations_memory_rights_index: 9.02,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-003",
      name: "UK/Caraïbes — Esclavage Indemnisation 2023 Debat, Plantation Profits Familles Royales, CARICOM 14 Points & Windrush",
      country: "UK/Caraïbes",
      colonial_genocide_crime_denial_severity_score: 89.0,
      cultural_patrimony_restitution_refusal_scale_score: 87.0,
      reparations_financial_compensation_denial_score: 87.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 85.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "reparations_financial_compensation_denial",
      estimated_colonial_reparations_memory_rights_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-004",
      name: "Pays-Bas/Indonésie — Reconnaissance Partielle 2022, Archives Torture Décolonisation, Westerling Massacres & Comores",
      country: "Pays-Bas/Indonésie",
      colonial_genocide_crime_denial_severity_score: 86.0,
      cultural_patrimony_restitution_refusal_scale_score: 84.0,
      reparations_financial_compensation_denial_score: 84.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 82.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "colonial_genocide_crime_denial_severity",
      estimated_colonial_reparations_memory_rights_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-005",
      name: "Allemagne/Namibie — Héreros-Namas Génocide Reconnu 2021, 1.1B€ Aide Pas Réparations, OvaHerero Négociations & Crânes Restitués",
      country: "Allemagne/Namibie",
      colonial_genocide_crime_denial_severity_score: 57.0,
      cultural_patrimony_restitution_refusal_scale_score: 55.0,
      reparations_financial_compensation_denial_score: 55.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 53.0,
      composite_score: 55.2,
      risk_level: "élevé",
      primary_pattern: "indigenous_colonial_trauma_acknowledgment_deficit_gap",
      estimated_colonial_reparations_memory_rights_index: 5.52,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-006",
      name: "USA/Afro-Américains — Slavery Reparations H.R.40 Bloqué 30 Ans, Juneteenth Sans Réparations, Redlining Wealth Gap & Jim Crow",
      country: "USA",
      colonial_genocide_crime_denial_severity_score: 54.0,
      cultural_patrimony_restitution_refusal_scale_score: 52.0,
      reparations_financial_compensation_denial_score: 52.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 50.0,
      composite_score: 52.2,
      risk_level: "élevé",
      primary_pattern: "reparations_financial_compensation_denial",
      estimated_colonial_reparations_memory_rights_index: 5.22,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-007",
      name: "ICOM/UNESCO — Principes Restitution Patrimoine, Convention 1970, Restitution Objets & Mécanisme Biens Culturels",
      country: "Global",
      colonial_genocide_crime_denial_severity_score: 27.0,
      cultural_patrimony_restitution_refusal_scale_score: 26.0,
      reparations_financial_compensation_denial_score: 26.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 25.0,
      composite_score: 26.1,
      risk_level: "modéré",
      primary_pattern: "cultural_patrimony_restitution_refusal_scale",
      estimated_colonial_reparations_memory_rights_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      id: "CRM-008",
      name: "ONU/DDRIP — Droit Réparation Peuples Autochtones, CERD Recommandations Réparations & SDG 10 Inégalités Réduction",
      country: "Global",
      colonial_genocide_crime_denial_severity_score: 5.0,
      cultural_patrimony_restitution_refusal_scale_score: 4.0,
      reparations_financial_compensation_denial_score: 4.0,
      indigenous_colonial_trauma_acknowledgment_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "indigenous_colonial_trauma_acknowledgment_deficit_gap",
      estimated_colonial_reparations_memory_rights_index: 0.43,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/colonial-reparations-memory-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
