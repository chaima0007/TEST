import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-eviction-homelessness-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "housing_eviction_homelessness_rights_engine",
  domain: "housing_eviction_homelessness_rights",
  total_entities: 8,
  avg_composite: 60.12,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    expulsions_forcees_minorites: 2,
    evictions_slums_projets_infra: 1,
    criminalisation_sdf_anti_camping: 1,
    insecurite_fonciere_gentrification: 2,
    protection_droit_logement: 2,
  },
  top_risk_entities: [
    "Inde/Bulldozer Justice — Démolitions Maisons Minorités Musulmanes, Expulsions Slums Pré-Olympiques & 15M Déplacés Projets Infra",
    "Kenya/Nairobi — Bidonvilles Kibera Expulsions Répétées, Police Violence Squatters, Tenure Informelle 70% Population & Nairobi Expressway",
    "Brésil/Rio — Favela Expulsions Coupe Monde/JO, Milice Propriété, Cadastre Exclu Pauvres & Réforme Foncière Bloquée",
    "USA — Sans-Abri 580 000, Anti-Camping Lois 23 États, Sweeps Camps & Loyers San Francisco/NY Inaccessibles",
  ],
  critical_alerts: [
    "Inde/Bulldozer Justice — Démolitions Maisons Minorités Musulmanes, Expulsions Slums Pré-Olympiques & 15M Déplacés Projets Infra: expulsions forcees minorites",
    "Kenya/Nairobi — Bidonvilles Kibera Expulsions Répétées, Police Violence Squatters, Tenure Informelle 70% Population & Nairobi Expressway: expulsions forcees minorites",
    "Brésil/Rio — Favela Expulsions Coupe Monde/JO, Milice Propriété, Cadastre Exclu Pauvres & Réforme Foncière Bloquée: evictions slums projets infra",
    "USA — Sans-Abri 580 000, Anti-Camping Lois 23 États, Sweeps Camps & Loyers San Francisco/NY Inaccessibles: criminalisation sdf anti camping",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_housing_eviction_homelessness_rights_index: 6.01,
  data_sources: [
    "un_habitat_forced_eviction_global_report",
    "cohre_housing_rights_violations_database",
    "feantsa_european_homelessness_monitoring_report",
  ],
  entities: [
    {
      id: "HEH-001",
      name: "Inde/Bulldozer Justice — Démolitions Maisons Minorités Musulmanes, Expulsions Slums Pré-Olympiques & 15M Déplacés Projets Infra",
      country: "Inde",
      composite_score: 91.8,
      forced_eviction_displacement_severity_score: 96.0,
      homelessness_criminalization_scale_score: 88.0,
      land_tenure_insecurity_indigenous_score: 92.0,
      affordable_housing_right_enforcement_deficit_gap_score: 90.0,
      risk_level: "critique",
      primary_pattern: "expulsions_forcees_minorites",
      estimated_housing_eviction_homelessness_rights_index: 9.18,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-002",
      name: "Kenya/Nairobi — Bidonvilles Kibera Expulsions Répétées, Police Violence Squatters, Tenure Informelle 70% Population & Nairobi Expressway",
      country: "Kenya",
      composite_score: 88.35,
      forced_eviction_displacement_severity_score: 90.0,
      homelessness_criminalization_scale_score: 85.0,
      land_tenure_insecurity_indigenous_score: 90.0,
      affordable_housing_right_enforcement_deficit_gap_score: 88.0,
      risk_level: "critique",
      primary_pattern: "expulsions_forcees_minorites",
      estimated_housing_eviction_homelessness_rights_index: 8.84,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-003",
      name: "Brésil/Rio — Favela Expulsions Coupe Monde/JO, Milice Propriété, Cadastre Exclu Pauvres & Réforme Foncière Bloquée",
      country: "Brésil",
      composite_score: 85.15,
      forced_eviction_displacement_severity_score: 88.0,
      homelessness_criminalization_scale_score: 82.0,
      land_tenure_insecurity_indigenous_score: 85.0,
      affordable_housing_right_enforcement_deficit_gap_score: 85.0,
      risk_level: "critique",
      primary_pattern: "evictions_slums_projets_infra",
      estimated_housing_eviction_homelessness_rights_index: 8.52,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-004",
      name: "USA — Sans-Abri 580 000, Anti-Camping Lois 23 États, Sweeps Camps & Loyers San Francisco/NY Inaccessibles",
      country: "États-Unis",
      composite_score: 80.25,
      forced_eviction_displacement_severity_score: 75.0,
      homelessness_criminalization_scale_score: 88.0,
      land_tenure_insecurity_indigenous_score: 75.0,
      affordable_housing_right_enforcement_deficit_gap_score: 85.0,
      risk_level: "critique",
      primary_pattern: "criminalisation_sdf_anti_camping",
      estimated_housing_eviction_homelessness_rights_index: 8.03,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-005",
      name: "Philippines — Évacuations Forcées Duterte/Marcos, 4M SDF Estimés, Anti-Squatter Laws & DMCI Gentrification",
      country: "Philippines",
      composite_score: 54.15,
      forced_eviction_displacement_severity_score: 58.0,
      homelessness_criminalization_scale_score: 52.0,
      land_tenure_insecurity_indigenous_score: 55.0,
      affordable_housing_right_enforcement_deficit_gap_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "insecurite_fonciere_gentrification",
      estimated_housing_eviction_homelessness_rights_index: 5.42,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-006",
      name: "France/UE — Squats Expulsés Hiver, DALO Droit Non Opposable, Migrants Tentes Évacuées Paris & Loi Anti-Squat",
      country: "France/Union Européenne",
      composite_score: 51.5,
      forced_eviction_displacement_severity_score: 50.0,
      homelessness_criminalization_scale_score: 55.0,
      land_tenure_insecurity_indigenous_score: 47.0,
      affordable_housing_right_enforcement_deficit_gap_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "insecurite_fonciere_gentrification",
      estimated_housing_eviction_homelessness_rights_index: 5.15,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-007",
      name: "UN-Habitat/HIC — Monitoring Expulsions Forcées, Principes Pinheiro, Campagnes Sécurité Tenure & Rapports Fonciers",
      country: "International",
      composite_score: 25.8,
      forced_eviction_displacement_severity_score: 25.0,
      homelessness_criminalization_scale_score: 26.0,
      land_tenure_insecurity_indigenous_score: 28.0,
      affordable_housing_right_enforcement_deficit_gap_score: 24.0,
      risk_level: "modéré",
      primary_pattern: "protection_droit_logement",
      estimated_housing_eviction_homelessness_rights_index: 2.58,
      last_updated: "2026-06-21",
    },
    {
      id: "HEH-008",
      name: "ONU/Art.11 DESC — Droit Logement Convenable, Comité DESC Observation Générale 4 & SDG 11.1 Habitat",
      country: "International",
      composite_score: 3.95,
      forced_eviction_displacement_severity_score: 4.0,
      homelessness_criminalization_scale_score: 3.0,
      land_tenure_insecurity_indigenous_score: 4.0,
      affordable_housing_right_enforcement_deficit_gap_score: 5.0,
      risk_level: "faible",
      primary_pattern: "protection_droit_logement",
      estimated_housing_eviction_homelessness_rights_index: 0.4,
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
      `${process.env.SWARM_API_URL}/housing-eviction-homelessness-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
