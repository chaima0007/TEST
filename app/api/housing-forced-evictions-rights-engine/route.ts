import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-forced-evictions-rights-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  agent: "Housing Forced Evictions Rights Engine Agent",
  domain: "housing_forced_evictions_rights",
  total_entities: 8,
  avg_composite: 58.81,
  confidence_score: 0.86,
  avg_estimated_housing_rights_index: 5.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_habitat_world_cities_report_2022",
    "cohre_global_survey_forced_evictions_2023",
    "amnesty_international_housing_rights_report_2023",
    "feantsa_ethos_homelessness_europe_2023",
  ],
  entities: [
    {
      id: "HFE-001",
      name: "Inde — 100M+ Sans Logement Adéquat, Démolitions Bidonvilles Massives, Dalit Ciblés",
      country: "Inde",
      composite_score: 90.75,
      risk_level: "critique",
      forced_eviction_rate_score: 93.0,
      housing_affordability_crisis_score: 90.0,
      legal_protection_enforcement_deficit_score: 91.0,
      homelessness_state_response_score: 88.0,
      estimated_housing_rights_index: 9.08,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-002",
      name: "Kenya/Nairobi — Kibera 250 000 Expulsés Décennie, Récupération Terrain État sans Indemnité",
      country: "Kenya",
      composite_score: 85.75,
      risk_level: "critique",
      forced_eviction_rate_score: 88.0,
      housing_affordability_crisis_score: 84.0,
      legal_protection_enforcement_deficit_score: 87.0,
      homelessness_state_response_score: 83.0,
      estimated_housing_rights_index: 8.58,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-003",
      name: "Philippines/Manille — 100 000 Expulsions/An Urban Poor, Duterte Reclaiming Land Programme",
      country: "Philippines",
      composite_score: 81.45,
      risk_level: "critique",
      forced_eviction_rate_score: 84.0,
      housing_affordability_crisis_score: 79.0,
      legal_protection_enforcement_deficit_score: 82.0,
      homelessness_state_response_score: 80.0,
      estimated_housing_rights_index: 8.15,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-004",
      name: "Brésil/Favelas — 170 000 Expulsés JO Rio 2016, Spéculation Immobilière Porto Maravilha",
      country: "Brésil",
      composite_score: 76.95,
      risk_level: "critique",
      forced_eviction_rate_score: 79.0,
      housing_affordability_crisis_score: 77.0,
      legal_protection_enforcement_deficit_score: 76.0,
      homelessness_state_response_score: 75.0,
      estimated_housing_rights_index: 7.70,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-005",
      name: "USA — 600 000 Sans-Abri/Nuit, Anti-Camping Laws, Gentrification Côtes & Criminalisation SDF",
      country: "USA",
      composite_score: 54.45,
      risk_level: "élevé",
      forced_eviction_rate_score: 52.0,
      housing_affordability_crisis_score: 58.0,
      legal_protection_enforcement_deficit_score: 55.0,
      homelessness_state_response_score: 53.0,
      estimated_housing_rights_index: 5.45,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-006",
      name: "France — 300 000 Sans Domicile, DAL Contesté, Expulsions Hivernales Trêve Contournée",
      country: "France",
      composite_score: 46.35,
      risk_level: "élevé",
      forced_eviction_rate_score: 44.0,
      housing_affordability_crisis_score: 50.0,
      legal_protection_enforcement_deficit_score: 45.0,
      homelessness_state_response_score: 47.0,
      estimated_housing_rights_index: 4.64,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-007",
      name: "Pays-Bas — Réforme Logement Social: 170 000 Logements Vendus Secteur Privé, Liste Attente 15 Ans",
      country: "Pays-Bas",
      composite_score: 28.9,
      risk_level: "modéré",
      forced_eviction_rate_score: 28.0,
      housing_affordability_crisis_score: 32.0,
      legal_protection_enforcement_deficit_score: 26.0,
      homelessness_state_response_score: 30.0,
      estimated_housing_rights_index: 2.89,
      last_updated: "2026-06-21",
    },
    {
      id: "HFE-008",
      name: "Finlande — Modèle Housing First: Sans-Abrisme Réduit 85%, Y-Foundation Référence Mondiale",
      country: "Finlande",
      composite_score: 5.85,
      risk_level: "faible",
      forced_eviction_rate_score: 6.0,
      housing_affordability_crisis_score: 8.0,
      legal_protection_enforcement_deficit_score: 5.0,
      homelessness_state_response_score: 4.0,
      estimated_housing_rights_index: 0.59,
      last_updated: "2026-06-21",
    },
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-forced-evictions-rights-engine`, {
      next: { revalidate: 30 },
    });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
