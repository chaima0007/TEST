import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[shrimp-fishing-forced-labor-rights] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "shrimp_fishing_forced_labor_rights_engine",
  domain: "shrimp_fishing_forced_labor_rights",
  total_entities: 8,
  avg_composite: 62.16,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    forced_labor_trafficking: 3,
    debt_bondage_recruitment: 2,
    flag_state_impunity: 2,
    corporate_supply_chain_complicity: 1,
  },
  top_risk_entities: [
    { id: "SFL-001", name: "Thaïlande — 'Ghost Ships', Travail Forcé Pêche Crevettes & Esclavage Maritime", score: 96.1, risk: "critique" },
    { id: "SFL-002", name: "Myanmar — Travailleurs Rohingya Bateaux Crevettes, Traite & Impunité Totale", score: 89.9, risk: "critique" },
    { id: "SFL-003", name: "Indonésie — Pêcheurs Étrangers Captifs Ambon, Traite & Dettes Forcées", score: 81.45, risk: "critique" },
  ],
  critical_alerts: [
    "SFL-001: Thaïlande — Ghost Ships, Travail Forcé Pêche Crevettes & Esclavage Maritime — composite 96.1",
    "SFL-002: Myanmar — Travailleurs Rohingya Bateaux Crevettes, Traite & Impunité Totale — composite 89.9",
    "SFL-003: Indonésie — Pêcheurs Étrangers Captifs Ambon, Traite & Dettes Forcées — composite 81.45",
    "SFL-004: Bangladesh — Enfants Pêche Baie Bengale, Cox Bazar & Absence Protection — composite 76.55",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_shrimp_fishing_forced_labor_index: 6.21,
  data_sources: [
    "ilo_forced_labour_fishing_sector_2013_updated",
    "human_rights_watch_thailand_fishing_boats_2018",
    "iuu_fishing_index_global_2023",
    "environmental_justice_foundation_seafood_slavery_report",
  ],
  entities: [
    {
      id: "SFL-001",
      name: "Thaïlande — 'Ghost Ships', Travail Forcé Pêche Crevettes & Esclavage Maritime",
      country: "Thaïlande",
      forced_labor_trafficking_prevalence_score: 99.0,
      debt_bondage_deceptive_recruitment_score: 97.0,
      flag_state_impunity_enforcement_deficit_score: 95.0,
      corporate_supply_chain_complicity_score: 93.0,
      composite_score: 96.1,
      risk_level: "critique",
      primary_pattern: "Ghost ships hors eaux territoriales, travailleurs retenus captifs années, CP Foods supply chain",
      estimated_shrimp_fishing_forced_labor_index: 9.61,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-002",
      name: "Myanmar — Travailleurs Rohingya Bateaux Crevettes, Traite & Impunité Totale",
      country: "Myanmar",
      forced_labor_trafficking_prevalence_score: 93.0,
      debt_bondage_deceptive_recruitment_score: 90.0,
      flag_state_impunity_enforcement_deficit_score: 88.0,
      corporate_supply_chain_complicity_score: 86.0,
      composite_score: 89.9,
      risk_level: "critique",
      primary_pattern: "Rohingyas fuyant persécutions recrutés frauduleusement bateaux crevettes, traite systémique",
      estimated_shrimp_fishing_forced_labor_index: 8.99,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-003",
      name: "Indonésie — Pêcheurs Étrangers Captifs Ambon, Traite & Dettes Forcées",
      country: "Indonésie",
      forced_labor_trafficking_prevalence_score: 85.0,
      debt_bondage_deceptive_recruitment_score: 82.0,
      flag_state_impunity_enforcement_deficit_score: 80.0,
      corporate_supply_chain_complicity_score: 78.0,
      composite_score: 81.45,
      risk_level: "critique",
      primary_pattern: "Pêcheurs vietnamiens/cambodgiens captifs ports Ambon, dettes fictives, aucun recours",
      estimated_shrimp_fishing_forced_labor_index: 8.15,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-004",
      name: "Bangladesh — Enfants Pêche Baie Bengale, Cox Bazar & Absence Protection",
      country: "Bangladesh",
      forced_labor_trafficking_prevalence_score: 80.0,
      debt_bondage_deceptive_recruitment_score: 77.0,
      flag_state_impunity_enforcement_deficit_score: 75.0,
      corporate_supply_chain_complicity_score: 73.0,
      composite_score: 76.55,
      risk_level: "critique",
      primary_pattern: "Enfants 8-14 ans bateaux crevettes Baie Bengale, Cox Bazar sans inspection maritime",
      estimated_shrimp_fishing_forced_labor_index: 7.66,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-005",
      name: "Vietnam — Bateaux Pêche Illegale IUU, Travailleurs Détenus & Amendes",
      country: "Vietnam",
      forced_labor_trafficking_prevalence_score: 61.0,
      debt_bondage_deceptive_recruitment_score: 58.0,
      flag_state_impunity_enforcement_deficit_score: 56.0,
      corporate_supply_chain_complicity_score: 54.0,
      composite_score: 57.55,
      risk_level: "élevé",
      primary_pattern: "Bateaux IUU pêche illégale eaux étrangères, travailleurs détenus cartons rouges UE 2017",
      estimated_shrimp_fishing_forced_labor_index: 5.76,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-006",
      name: "Équateur — Crevetticulture Esmeraldas, Conditions Travail & Surveillance Lacunaire",
      country: "Équateur",
      forced_labor_trafficking_prevalence_score: 51.0,
      debt_bondage_deceptive_recruitment_score: 48.0,
      flag_state_impunity_enforcement_deficit_score: 46.0,
      corporate_supply_chain_complicity_score: 44.0,
      composite_score: 47.55,
      risk_level: "élevé",
      primary_pattern: "Fermes crevettes Esmeraldas, travailleurs migrants mal payés, inspection insuffisante",
      estimated_shrimp_fishing_forced_labor_index: 4.76,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-007",
      name: "USA — Import Crevettes Forcées, Lacunes CBP 307 & Traçabilité Chaîne",
      country: "États-Unis",
      forced_labor_trafficking_prevalence_score: 32.0,
      debt_bondage_deceptive_recruitment_score: 29.0,
      flag_state_impunity_enforcement_deficit_score: 27.0,
      corporate_supply_chain_complicity_score: 25.0,
      composite_score: 28.6,
      risk_level: "modéré",
      primary_pattern: "CBP withhold-and-release orders insuffisants, crevettes importées travail forcé détectées",
      estimated_shrimp_fishing_forced_labor_index: 2.86,
      last_updated: "2026-06-22",
    },
    {
      id: "SFL-008",
      name: "OIT / Convention 188 Travail Pêche — Cadre Normatif & Ratifications",
      country: "Global",
      forced_labor_trafficking_prevalence_score: 13.0,
      debt_bondage_deceptive_recruitment_score: 11.0,
      flag_state_impunity_enforcement_deficit_score: 9.0,
      corporate_supply_chain_complicity_score: 7.0,
      composite_score: 10.3,
      risk_level: "faible",
      primary_pattern: "Convention OIT C188 travail pêche, 20 ratifications, cadre normatif insuffisamment universel",
      estimated_shrimp_fishing_forced_labor_index: 1.03,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/shrimp_fishing_forced_labor_rights_engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
