import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[algorithmic-justice-bias-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  agent: "algorithmic_justice_bias_rights_engine",
  domain: "algorithmic_justice_bias_rights",
  generated_at: new Date().toISOString(),
  accent: "#7c3aed",
  total_entities: 8,
  avg_composite: 60.14,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  top_risk_entities: [
    { id: "AJB-002", name: "Chine — Crédit Social IA, Surveillance Citoyens Discriminatoire", score: 92.8, risk: "critique" },
    { id: "AJB-001", name: "États-Unis — COMPAS & Biais Racial Prédictif Justice Pénale", score: 90.3, risk: "critique" },
    { id: "AJB-003", name: "Royaume-Uni — Windrush Algorithme Immigration Discriminatoire", score: 85.0, risk: "critique" },
  ],
  critical_alerts: [
    "AJB-001: États-Unis — COMPAS & Biais Racial Prédictif Justice Pénale — composite 90.3",
    "AJB-002: Chine — Crédit Social IA, Surveillance Citoyens Discriminatoire — composite 92.8",
    "AJB-003: Royaume-Uni — Windrush Algorithme Immigration Discriminatoire — composite 85.0",
    "AJB-004: Inde — Aadhaar Exclusion Biométrique Castes Défavorisées — composite 82.65",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_algorithmic_justice_bias_index: 6.01,
  data_sources: [
    "propublica_compas_analysis_2016",
    "ai_now_institute_algorithmic_accountability_2023",
    "algorithmic_justice_league_report_2023",
    "eu_ai_act_impact_assessment_2024",
  ],
  entities: [
    {
      id: "AJB-001",
      name: "États-Unis — COMPAS & Biais Racial Prédictif Justice Pénale",
      country: "États-Unis",
      algorithmic_discrimination_deployment_score: 92.0,
      due_process_algorithmic_denial_score: 89.0,
      transparency_explainability_deficit_score: 91.0,
      regulatory_accountability_framework_score: 85.0,
      composite_score: 90.3,
      risk_level: "critique",
      primary_pattern: "COMPAS prédit récidive avec biais racial documenté, opacité totale, zéro droit contestation",
      estimated_algorithmic_justice_bias_index: 9.03,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-002",
      name: "Chine — Crédit Social IA, Surveillance Citoyens Discriminatoire",
      country: "Chine",
      algorithmic_discrimination_deployment_score: 95.0,
      due_process_algorithmic_denial_score: 94.0,
      transparency_explainability_deficit_score: 93.0,
      regulatory_accountability_framework_score: 88.0,
      composite_score: 92.8,
      risk_level: "critique",
      primary_pattern: "Système crédit social IA discrimine minorités, zéro due process, blacklists opaques",
      estimated_algorithmic_justice_bias_index: 9.28,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-003",
      name: "Royaume-Uni — Windrush Algorithme Immigration Discriminatoire",
      country: "Royaume-Uni",
      algorithmic_discrimination_deployment_score: 87.0,
      due_process_algorithmic_denial_score: 85.0,
      transparency_explainability_deficit_score: 83.0,
      regulatory_accountability_framework_score: 80.0,
      composite_score: 84.6,
      risk_level: "critique",
      primary_pattern: "Algorithme visa discrimine Caribbean-British, scandale Windrush amplifié par IA",
      estimated_algorithmic_justice_bias_index: 8.46,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-004",
      name: "Inde — Aadhaar Exclusion Biométrique Castes Défavorisées",
      country: "Inde",
      algorithmic_discrimination_deployment_score: 84.0,
      due_process_algorithmic_denial_score: 82.0,
      transparency_explainability_deficit_score: 80.0,
      regulatory_accountability_framework_score: 78.0,
      composite_score: 81.65,
      risk_level: "critique",
      primary_pattern: "Aadhaar échoue reconnaître empreintes travailleurs manuels, exclusion aide sociale",
      estimated_algorithmic_justice_bias_index: 8.17,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-005",
      name: "France — Parcoursup Algorithme Opaque Sélection Universitaire",
      country: "France",
      algorithmic_discrimination_deployment_score: 52.0,
      due_process_algorithmic_denial_score: 55.0,
      transparency_explainability_deficit_score: 58.0,
      regulatory_accountability_framework_score: 45.0,
      composite_score: 53.45,
      risk_level: "élevé",
      primary_pattern: "Parcoursup opaque, critères géographiques favorisent lycées privés, contestation limitée",
      estimated_algorithmic_justice_bias_index: 5.35,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-006",
      name: "Pays-Bas — SyRI Fraude Sociale Profiling Ethnique Illégal",
      country: "Pays-Bas",
      algorithmic_discrimination_deployment_score: 48.0,
      due_process_algorithmic_denial_score: 50.0,
      transparency_explainability_deficit_score: 54.0,
      regulatory_accountability_framework_score: 42.0,
      composite_score: 48.9,
      risk_level: "élevé",
      primary_pattern: "SyRI ciblait quartiers ethniques, tribunal l'a invalidé en 2020, précédent CEDH",
      estimated_algorithmic_justice_bias_index: 4.89,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-007",
      name: "Canada — MCAP Algorithme Garde Enfants Biais Autochtones",
      country: "Canada",
      algorithmic_discrimination_deployment_score: 28.0,
      due_process_algorithmic_denial_score: 30.0,
      transparency_explainability_deficit_score: 25.0,
      regulatory_accountability_framework_score: 22.0,
      composite_score: 26.65,
      risk_level: "modéré",
      primary_pattern: "Algorithme protection enfance surreprésente familles autochtones, biais systémique documenté",
      estimated_algorithmic_justice_bias_index: 2.67,
      last_updated: "2026-06-21",
    },
    {
      id: "AJB-008",
      name: "Suède — AI Act Conformité, Registre Algorithmes Public",
      country: "Suède",
      algorithmic_discrimination_deployment_score: 5.0,
      due_process_algorithmic_denial_score: 5.0,
      transparency_explainability_deficit_score: 6.0,
      regulatory_accountability_framework_score: 4.0,
      composite_score: 5.05,
      risk_level: "faible",
      primary_pattern: "Registre public algorithmes État, AI Act conforme, droit contestation garanti RGPD",
      estimated_algorithmic_justice_bias_index: 0.51,
      last_updated: "2026-06-21",
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/algorithmic-justice-bias-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
