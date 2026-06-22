import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[anti-corruption-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "anti_corruption_accountability_engine",
  domain: "anti_corruption_accountability",
  total_entities: 8,
  avg_composite: 62.08,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    state_capture: 3,
    judicial_bribery: 2,
    kleptocracy_procurement: 2,
    whistleblower_deficit: 1,
  },
  top_risk_entities: [
    { id: "ACA-001", name: "Somalie — CPI 11/100, Corruption Systémique", score: 93.95, risk: "critique" },
    { id: "ACA-002", name: "Syrie — CPI 13/100, Kleptocracie Assad", score: 91.95, risk: "critique" },
    { id: "ACA-003", name: "Corée du Nord — CPI 17/100, Corruption d'État", score: 89.95, risk: "critique" },
  ],
  critical_alerts: [
    "ACA-001: Somalie — CPI 11/100, Corruption Systémique — composite 93.95",
    "ACA-002: Syrie — CPI 13/100, Kleptocracie Assad — composite 91.95",
    "ACA-003: Corée du Nord — CPI 17/100, Corruption d'État — composite 89.95",
    "ACA-004: Yémen — CPI 16/100, Fragmentation Pouvoir — composite 87.95",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_anti_corruption_accountability_index: 6.21,
  data_sources: [
    "transparency_international_cpi_2023",
    "u4_anti_corruption_resource_centre_2023",
    "basel_aml_index_2023",
    "un_uncac_review_mechanism_2023",
  ],
  entities: [
    {
      id: "ACA-001",
      name: "Somalie — CPI 11/100, Corruption Systémique",
      country: "Somalie",
      grand_corruption_state_capture_severity_score: 96.0,
      judicial_police_bribery_impunity_scale_score: 93.0,
      public_procurement_kleptocracy_scale_score: 94.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 92.0,
      composite_score: 93.95,
      risk_level: "critique",
      primary_pattern: "État capturé clans, aide humanitaire détournée, impunité totale",
      estimated_anti_corruption_accountability_index: 9.39,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-002",
      name: "Syrie — CPI 13/100, Kleptocracie Assad",
      country: "Syrie",
      grand_corruption_state_capture_severity_score: 94.0,
      judicial_police_bribery_impunity_scale_score: 91.0,
      public_procurement_kleptocracy_scale_score: 92.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 90.0,
      composite_score: 91.95,
      risk_level: "critique",
      primary_pattern: "Kleptocracie familiale Assad, reconstruction corruption, sanctions contournées",
      estimated_anti_corruption_accountability_index: 9.2,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-003",
      name: "Corée du Nord — CPI 17/100, Corruption d'État",
      country: "Corée du Nord",
      grand_corruption_state_capture_severity_score: 92.0,
      judicial_police_bribery_impunity_scale_score: 89.0,
      public_procurement_kleptocracy_scale_score: 90.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "Corruption État institutionnalisée, économie parallèle Donju, siphonnage fonds militaires",
      estimated_anti_corruption_accountability_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-004",
      name: "Yémen — CPI 16/100, Fragmentation Pouvoir",
      country: "Yémen",
      grand_corruption_state_capture_severity_score: 90.0,
      judicial_police_bribery_impunity_scale_score: 87.0,
      public_procurement_kleptocracy_scale_score: 88.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 86.0,
      composite_score: 87.95,
      risk_level: "critique",
      primary_pattern: "Fragmentation pouvoir, corruption factions armées, aide détournée",
      estimated_anti_corruption_accountability_index: 8.79,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-005",
      name: "Venezuela — CPI 14/100, Corruption Pétrolière",
      country: "Venezuela",
      grand_corruption_state_capture_severity_score: 55.0,
      judicial_police_bribery_impunity_scale_score: 52.0,
      public_procurement_kleptocracy_scale_score: 53.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 51.0,
      composite_score: 52.95,
      risk_level: "élevé",
      primary_pattern: "PDVSA pillé, Maduro kleptocrates, opposition emprisonnée",
      estimated_anti_corruption_accountability_index: 5.3,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-006",
      name: "Afghanistan — CPI 20/100, Retour Taliban",
      country: "Afghanistan",
      grand_corruption_state_capture_severity_score: 52.0,
      judicial_police_bribery_impunity_scale_score: 49.0,
      public_procurement_kleptocracy_scale_score: 50.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 48.0,
      composite_score: 49.95,
      risk_level: "élevé",
      primary_pattern: "Retour Taliban, corruption endémique, trafic opium financement",
      estimated_anti_corruption_accountability_index: 5.0,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-007",
      name: "Kenya — CPI 31/100, Réformes Partielles Ruto",
      country: "Kenya",
      grand_corruption_state_capture_severity_score: 28.0,
      judicial_police_bribery_impunity_scale_score: 25.0,
      public_procurement_kleptocracy_scale_score: 26.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 24.0,
      composite_score: 25.95,
      risk_level: "modéré",
      primary_pattern: "Ruto réformes partielles, marchés publics détournés, EACC limité",
      estimated_anti_corruption_accountability_index: 2.6,
      last_updated: "2026-06-21",
    },
    {
      id: "ACA-008",
      name: "Danemark — CPI 90/100, Modèle Mondial Anti-Corruption",
      country: "Danemark",
      grand_corruption_state_capture_severity_score: 4.0,
      judicial_police_bribery_impunity_scale_score: 4.0,
      public_procurement_kleptocracy_scale_score: 4.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Transparence institutionnelle, protection lanceurs d&apos;alerte solide, OCDE modèle",
      estimated_anti_corruption_accountability_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-corruption-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
