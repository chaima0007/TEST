import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-justice-environmental-defenders-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Justice Environmental Defenders Engine Agent",
  domain: "climate_justice_environmental_defenders",
  total_entities: 8,
  avg_composite: 60.86,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    environmental_defender_killing_criminalization_severity: 4,
    climate_loss_damage_vulnerable_population_scale: 1,
    fossil_fuel_corporate_impunity: 2,
    climate_litigation_access_justice_deficit_gap: 1,
  },
  top_risk_entities: [
    "Philippines/Honduras — Berta Cáceres Assassinée, Île Nations Submersion, Défenseurs Environnement #1 Tués Monde & Impunité Totale",
    "Amazonie Brésil — 300+ Défenseurs Tués Bolsonaro Era, Terres Indigènes Déforestées, Garimpeiros Violents & Lula Réforme Lente",
    "Pakistan/Bangladesh — Inondations Catastrophiques 33M Déplacés, Pertes Économiques Irréparables, Emprunt FMI Climate & Pollueurs Non Responsables",
  ],
  critical_alerts: [
    "Philippines/Honduras: environmental_defender_killing_criminalization_severity",
    "Amazonie Brésil: environmental_defender_killing_criminalization_severity",
    "Pakistan/Bangladesh: climate_loss_damage_vulnerable_population_scale",
    "Afrique Subsaharienne: fossil_fuel_corporate_impunity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_climate_justice_environmental_defenders_index: 6.09,
  data_sources: [
    "global_witness_environmental_defenders_annual_report",
    "ipcc_climate_loss_damage_vulnerable_populations",
    "frontline_defenders_at_risk_global_database",
  ],
  entities: [
    {
      id: "CJE-001",
      name: "Philippines/Honduras — Berta Cáceres Assassinée, Île Nations Submersion, Défenseurs Environnement #1 Tués Monde & Impunité Totale",
      country: "Philippines/Honduras",
      environmental_defender_killing_criminalization_severity_score: 93.0,
      climate_loss_damage_vulnerable_population_scale_score: 91.0,
      fossil_fuel_corporate_impunity_score: 90.0,
      climate_litigation_access_justice_deficit_gap_score: 92.0,
      composite_score: 91.55,
      risk_level: "critique",
      primary_pattern: "environmental_defender_killing_criminalization_severity",
      estimated_climate_justice_environmental_defenders_index: 9.16,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-002",
      name: "Amazonie Brésil — 300+ Défenseurs Tués Bolsonaro Era, Terres Indigènes Déforestées, Garimpeiros Violents & Lula Réforme Lente",
      country: "Brésil",
      environmental_defender_killing_criminalization_severity_score: 90.0,
      climate_loss_damage_vulnerable_population_scale_score: 88.0,
      fossil_fuel_corporate_impunity_score: 89.0,
      climate_litigation_access_justice_deficit_gap_score: 91.0,
      composite_score: 89.45,
      risk_level: "critique",
      primary_pattern: "environmental_defender_killing_criminalization_severity",
      estimated_climate_justice_environmental_defenders_index: 8.95,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-003",
      name: "Pakistan/Bangladesh — Inondations Catastrophiques 33M Déplacés, Pertes Économiques Irréparables, Emprunt FMI Climate & Pollueurs Non Responsables",
      country: "Pakistan/Bangladesh",
      environmental_defender_killing_criminalization_severity_score: 87.0,
      climate_loss_damage_vulnerable_population_scale_score: 85.0,
      fossil_fuel_corporate_impunity_score: 86.0,
      climate_litigation_access_justice_deficit_gap_score: 88.0,
      composite_score: 86.45,
      risk_level: "critique",
      primary_pattern: "climate_loss_damage_vulnerable_population_scale",
      estimated_climate_justice_environmental_defenders_index: 8.65,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-004",
      name: "Afrique Subsaharienne — Sécheresse Corne Afrique 36M, Lac Tchad Disparu 90%, Cyclones Mozambique & Multinationales Extractives Immunisées",
      country: "Afrique Subsaharienne",
      environmental_defender_killing_criminalization_severity_score: 84.0,
      climate_loss_damage_vulnerable_population_scale_score: 82.0,
      fossil_fuel_corporate_impunity_score: 83.0,
      climate_litigation_access_justice_deficit_gap_score: 85.0,
      composite_score: 83.45,
      risk_level: "critique",
      primary_pattern: "fossil_fuel_corporate_impunity",
      estimated_climate_justice_environmental_defenders_index: 8.35,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-005",
      name: "Indonésie/PNG — Déforestation Palmier Huile, Communautés Indigènes Expulsées, Forêts Tourbe Brûlées & Licences Sans FPIC",
      country: "Indonésie/PNG",
      environmental_defender_killing_criminalization_severity_score: 55.0,
      climate_loss_damage_vulnerable_population_scale_score: 53.0,
      fossil_fuel_corporate_impunity_score: 54.0,
      climate_litigation_access_justice_deficit_gap_score: 56.0,
      composite_score: 54.45,
      risk_level: "élevé",
      primary_pattern: "environmental_defender_killing_criminalization_severity",
      estimated_climate_justice_environmental_defenders_index: 5.45,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-006",
      name: "USA/Australie — Greenwashing Légal, Climate SLAPP Contre Activistes, Fossil Fuel Subsidies 7T$/An & Lobbying Anti-Climate",
      country: "USA/Australie",
      environmental_defender_killing_criminalization_severity_score: 52.0,
      climate_loss_damage_vulnerable_population_scale_score: 50.0,
      fossil_fuel_corporate_impunity_score: 51.0,
      climate_litigation_access_justice_deficit_gap_score: 53.0,
      composite_score: 51.45,
      risk_level: "élevé",
      primary_pattern: "fossil_fuel_corporate_impunity",
      estimated_climate_justice_environmental_defenders_index: 5.15,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-007",
      name: "Global Witness/Frontline Defenders — Rapports Défenseurs Environnement, Cartographie Meurtres & Mécanismes Protection",
      country: "Global",
      environmental_defender_killing_criminalization_severity_score: 27.0,
      climate_loss_damage_vulnerable_population_scale_score: 25.0,
      fossil_fuel_corporate_impunity_score: 26.0,
      climate_litigation_access_justice_deficit_gap_score: 26.0,
      composite_score: 26.05,
      risk_level: "modéré",
      primary_pattern: "environmental_defender_killing_criminalization_severity",
      estimated_climate_justice_environmental_defenders_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      id: "CJE-008",
      name: "ONU/Accord Paris + Aarhus — Droits Humains Climate Change, Rapporteur Spécial & SDG 13 Action Climatique",
      country: "Global",
      environmental_defender_killing_criminalization_severity_score: 5.0,
      climate_loss_damage_vulnerable_population_scale_score: 3.0,
      fossil_fuel_corporate_impunity_score: 4.0,
      climate_litigation_access_justice_deficit_gap_score: 4.0,
      composite_score: 4.05,
      risk_level: "faible",
      primary_pattern: "climate_litigation_access_justice_deficit_gap",
      estimated_climate_justice_environmental_defenders_index: 0.41,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/climate-justice-environmental-defenders-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
