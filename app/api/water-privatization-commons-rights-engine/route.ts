import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[water-privatization-commons-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  agent: "water_privatization_commons_rights_engine",
  domain: "water_privatization_commons_rights",
  generated_at: new Date().toISOString(),
  accent: "#0e7490",
  total_entities: 8,
  avg_composite: 60.00,
  confidence_score: 0.91,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  top_risk_entities: [
    { id: "WPC-001", name: "Bolivie — Guerre de l'Eau Cochabamba, Bechtel Confiscation", score: 91.75, risk: "critique" },
    { id: "WPC-002", name: "Afrique du Sud — Flint Africain, Detroit Water Shutoffs Raciales", score: 88.25, risk: "critique" },
    { id: "WPC-003", name: "Pakistan — Nestlé Extraction Aquifère, Communautés Asséchées", score: 85.65, risk: "critique" },
  ],
  critical_alerts: [
    "WPC-001: Bolivie — Guerre de l'Eau Cochabamba, Bechtel Confiscation — composite 91.75",
    "WPC-002: Afrique du Sud — Flint Africain, Detroit Water Shutoffs Raciales — composite 88.25",
    "WPC-003: Pakistan — Nestlé Extraction Aquifère, Communautés Asséchées — composite 85.65",
    "WPC-004: Inde — Coca-Cola Kerala Épuisement Nappe, Villages Sans Eau — composite 82.4",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_water_privatization_commons_index: 6.00,
  data_sources: [
    "un_special_rapporteur_right_to_water_2023",
    "corporate_accountability_water_report_2023",
    "blue_planet_project_water_commons_2024",
    "transnational_institute_privatisation_report_2023",
  ],
  entities: [
    {
      id: "WPC-001",
      name: "Bolivie — Guerre de l'Eau Cochabamba, Bechtel Confiscation",
      country: "Bolivie",
      corporate_water_capture_score: 93.0,
      access_denial_marginalized_communities_score: 91.0,
      commodification_human_right_violation_score: 94.0,
      regulatory_capture_accountability_score: 88.0,
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "Bechtel privatise eau, prix ×10, révolte populaire 2000, droits paysans niés",
      estimated_water_privatization_commons_index: 9.18,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-002",
      name: "Afrique du Sud — Flint Africain, Detroit Water Shutoffs Raciales",
      country: "Afrique du Sud",
      corporate_water_capture_score: 88.0,
      access_denial_marginalized_communities_score: 90.0,
      commodification_human_right_violation_score: 89.0,
      regulatory_capture_accountability_score: 85.0,
      composite_score: 88.25,
      risk_level: "critique",
      primary_pattern: "Townships sans eau potable, coupures racialisées, corporatisation Suez/Veolia townships",
      estimated_water_privatization_commons_index: 8.83,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-003",
      name: "Pakistan — Nestlé Extraction Aquifère, Communautés Asséchées",
      country: "Pakistan",
      corporate_water_capture_score: 86.0,
      access_denial_marginalized_communities_score: 88.0,
      commodification_human_right_violation_score: 85.0,
      regulatory_capture_accountability_score: 82.0,
      composite_score: 85.65,
      risk_level: "critique",
      primary_pattern: "Nestlé Pure Life épuise nappes phréatiques, villages ruraux sans accès, corruption régulatoire",
      estimated_water_privatization_commons_index: 8.57,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-004",
      name: "Inde — Coca-Cola Kerala Épuisement Nappe, Villages Sans Eau",
      country: "Inde",
      corporate_water_capture_score: 83.0,
      access_denial_marginalized_communities_score: 85.0,
      commodification_human_right_violation_score: 82.0,
      regulatory_capture_accountability_score: 79.0,
      composite_score: 82.45,
      risk_level: "critique",
      primary_pattern: "Usine Coca-Cola Plachimada épuise nappe, 1000 familles sans eau, tribunal condamne 2010",
      estimated_water_privatization_commons_index: 8.25,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-005",
      name: "Royaume-Uni — Thames Water Faillite, Rejets Égouts Sans Pénalité",
      country: "Royaume-Uni",
      corporate_water_capture_score: 52.0,
      access_denial_marginalized_communities_score: 48.0,
      commodification_human_right_violation_score: 55.0,
      regulatory_capture_accountability_score: 58.0,
      composite_score: 52.85,
      risk_level: "élevé",
      primary_pattern: "Thames Water endettée rejette eaux usées rivières, dividendes versés, régulateur inefficace",
      estimated_water_privatization_commons_index: 5.29,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-006",
      name: "États-Unis — Flint Michigan, Plomb Eau Communauté Noire Pauvre",
      country: "États-Unis",
      corporate_water_capture_score: 45.0,
      access_denial_marginalized_communities_score: 53.0,
      commodification_human_right_violation_score: 50.0,
      regulatory_capture_accountability_score: 48.0,
      composite_score: 48.85,
      risk_level: "élevé",
      primary_pattern: "Austérité impose eau Flint River, plomb intoxique enfants noirs, État dissimule 2015",
      estimated_water_privatization_commons_index: 4.89,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-007",
      name: "Chili — Constitution 1980 Eau Marchandise, Droits Eau Vendus",
      country: "Chili",
      corporate_water_capture_score: 25.0,
      access_denial_marginalized_communities_score: 28.0,
      commodification_human_right_violation_score: 30.0,
      regulatory_capture_accountability_score: 22.0,
      composite_score: 26.45,
      risk_level: "modéré",
      primary_pattern: "Code eau Pinochet privatise rivières, droits eau négociables, réforme constitutionnelle 2022",
      estimated_water_privatization_commons_index: 2.65,
      last_updated: "2026-06-21",
    },
    {
      id: "WPC-008",
      name: "Finlande — Eau Bien Commun Public, Droit Constitutionnel",
      country: "Finlande",
      corporate_water_capture_score: 4.0,
      access_denial_marginalized_communities_score: 4.0,
      commodification_human_right_violation_score: 4.0,
      regulatory_capture_accountability_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Eau service public non privatisable, tarifs réglementés, accès universel garanti constitutionnellement",
      estimated_water_privatization_commons_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-privatization-commons-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
