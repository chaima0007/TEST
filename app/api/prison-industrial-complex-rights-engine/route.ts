import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-industrial-complex-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  agent: "prison_industrial_complex_rights_engine",
  domain: "prison_industrial_complex_rights",
  generated_at: new Date().toISOString(),
  accent: "#b45309",
  total_entities: 8,
  avg_composite: 60.71,
  confidence_score: 0.92,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  top_risk_entities: [
    { id: "PIC-001", name: "États-Unis — 2.1M Détenus, CoreCivic GEO Group Profit Racial", score: 95.1, risk: "critique" },
    { id: "PIC-003", name: "Chine — Xinjiang Travail Forcé, Rééducation Industrielle Ouïghours", score: 93.85, risk: "critique" },
    { id: "PIC-002", name: "Brésil — 830k Détenus, Gangs Contrôlent Prisons, Esclavage Carcéral", score: 86.45, risk: "critique" },
  ],
  critical_alerts: [
    "PIC-001: États-Unis — 2.1M Détenus, CoreCivic GEO Group Profit Racial — composite 95.1",
    "PIC-002: Brésil — 830k Détenus, Gangs Contrôlent Prisons, Esclavage Carcéral — composite 86.45",
    "PIC-003: Chine — Xinjiang Travail Forcé, Rééducation Industrielle Ouïghours — composite 93.85",
    "PIC-004: Russie — Colonies Pénales Sibérie, Opposition Politique Incarcérée — composite 82.25",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_industrial_complex_index: 6.07,
  data_sources: [
    "prison_policy_initiative_mass_incarceration_2023",
    "aclu_private_prisons_profit_report_2023",
    "un_standard_minimum_rules_treatment_prisoners",
    "sentencing_project_racial_disparities_2024",
  ],
  entities: [
    {
      id: "PIC-001",
      name: "États-Unis — 2.1M Détenus, CoreCivic GEO Group Profit Racial",
      country: "États-Unis",
      mass_incarceration_racial_disparity_score: 97.0,
      private_prison_profit_incentive_score: 95.0,
      labor_exploitation_incarcerated_score: 93.0,
      rehabilitation_access_denial_score: 91.0,
      composite_score: 95.1,
      risk_level: "critique",
      primary_pattern: "2.1M détenus, Noirs 5× surreprésentés, CoreCivic $2Mds profits, travail $0.25/h",
      estimated_prison_industrial_complex_index: 9.51,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-002",
      name: "Brésil — 830k Détenus, Gangs Contrôlent Prisons, Esclavage Carcéral",
      country: "Brésil",
      mass_incarceration_racial_disparity_score: 88.0,
      private_prison_profit_incentive_score: 82.0,
      labor_exploitation_incarcerated_score: 87.0,
      rehabilitation_access_denial_score: 89.0,
      composite_score: 86.45,
      risk_level: "critique",
      primary_pattern: "830k détenus, Noirs brésiliens 67% détenus, PCC/CV contrôlent cellules, torture systémique",
      estimated_prison_industrial_complex_index: 8.65,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-003",
      name: "Chine — Xinjiang Travail Forcé, Rééducation Industrielle Ouïghours",
      country: "Chine",
      mass_incarceration_racial_disparity_score: 95.0,
      private_prison_profit_incentive_score: 90.0,
      labor_exploitation_incarcerated_score: 96.0,
      rehabilitation_access_denial_score: 93.0,
      composite_score: 93.85,
      risk_level: "critique",
      primary_pattern: "1M+ Ouïghours camps rééducation, travail forcé chaînes production, zéro recours juridique",
      estimated_prison_industrial_complex_index: 9.39,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-004",
      name: "Russie — Colonies Pénales Sibérie, Opposition Politique Incarcérée",
      country: "Russie",
      mass_incarceration_racial_disparity_score: 82.0,
      private_prison_profit_incentive_score: 75.0,
      labor_exploitation_incarcerated_score: 85.0,
      rehabilitation_access_denial_score: 88.0,
      composite_score: 82.25,
      risk_level: "critique",
      primary_pattern: "Colonies IK travail forcé industries militaires, opposants politiques Navalny, droits niés",
      estimated_prison_industrial_complex_index: 8.23,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-005",
      name: "Royaume-Uni — Serco Detention Centers, Migrants Indéfinis Retenus",
      country: "Royaume-Uni",
      mass_incarceration_racial_disparity_score: 50.0,
      private_prison_profit_incentive_score: 57.0,
      labor_exploitation_incarcerated_score: 48.0,
      rehabilitation_access_denial_score: 52.0,
      composite_score: 51.65,
      risk_level: "élevé",
      primary_pattern: "Serco G4S profits centres détention migrants, rétention indéfinie illégale CEDH",
      estimated_prison_industrial_complex_index: 5.17,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-006",
      name: "Australie — Nauru Offshore Processing, Trauma Psychologique Réfugiés",
      country: "Australie",
      mass_incarceration_racial_disparity_score: 45.0,
      private_prison_profit_incentive_score: 52.0,
      labor_exploitation_incarcerated_score: 42.0,
      rehabilitation_access_denial_score: 55.0,
      composite_score: 47.45,
      risk_level: "élevé",
      primary_pattern: "Centres offshore Nauru Manus, Broadspectrum profits, trauma enfants réfugiés documenté",
      estimated_prison_industrial_complex_index: 4.75,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-007",
      name: "France — Surpopulation Carcérale 145%, Maison Centrale Travail Sous-Payé",
      country: "France",
      mass_incarceration_racial_disparity_score: 26.0,
      private_prison_profit_incentive_score: 23.0,
      labor_exploitation_incarcerated_score: 28.0,
      rehabilitation_access_denial_score: 22.0,
      composite_score: 24.95,
      risk_level: "modéré",
      primary_pattern: "145% surpopulation, travail Gepsa €5/h, quartiers pauvres et issus immigration surreprésentés",
      estimated_prison_industrial_complex_index: 2.5,
      last_updated: "2026-06-21",
    },
    {
      id: "PIC-008",
      name: "Norvège — Halden Prison Modèle, Réhabilitation Taux Récidive 20%",
      country: "Norvège",
      mass_incarceration_racial_disparity_score: 5.0,
      private_prison_profit_incentive_score: 4.0,
      labor_exploitation_incarcerated_score: 5.0,
      rehabilitation_access_denial_score: 4.0,
      composite_score: 4.55,
      risk_level: "faible",
      primary_pattern: "Halden prison humaniste, 20% récidive vs 76% USA, éducation complète, zéro privatisation",
      estimated_prison_industrial_complex_index: 0.46,
      last_updated: "2026-06-21",
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-industrial-complex-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
