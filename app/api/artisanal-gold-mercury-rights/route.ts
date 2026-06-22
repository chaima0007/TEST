import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[artisanal-gold-mercury-rights] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "artisanal_gold_mercury_rights_engine",
  domain: "artisanal_gold_mercury_rights",
  total_entities: 8,
  avg_composite: 62.16,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    mercury_poisoning_exposure: 3,
    illegal_mining_enforcement_gap: 2,
    health_environment_nexus: 2,
    minamata_compliance_deficit: 1,
  },
  top_risk_entities: [
    { id: "AGM-001", name: "Congo/DRC — Orpailleurs Artisanaux, Mercure Rivières & Communautés Empoisonnées", score: 96.1, risk: "critique" },
    { id: "AGM-002", name: "Pérou — Madre de Dios, Mercure Amazonie & 40 000 Mineurs ASGM", score: 89.9, risk: "critique" },
    { id: "AGM-003", name: "Ghana — Galamsey Illégal, Mercure Cours d&apos;Eau & Droits Communautés", score: 81.45, risk: "critique" },
  ],
  critical_alerts: [
    "AGM-001: DRC — Orpailleurs Artisanaux, Mercure Rivières & Communautés Empoisonnées — composite 96.1",
    "AGM-002: Pérou — Madre de Dios, Mercure Amazonie & 40 000 Mineurs ASGM — composite 89.9",
    "AGM-003: Ghana — Galamsey Illégal, Mercure Cours d'Eau & Droits Communautés — composite 81.45",
    "AGM-004: Brésil — Garimpeiros Yanomami, Mercure Sang 100x OMS & Génocide Silencieux — composite 76.55",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_artisanal_gold_mercury_index: 6.21,
  data_sources: [
    "unep_global_mercury_assessment_2023",
    "minamata_convention_national_action_plans_asgm",
    "human_rights_watch_gold_mercury_report_2023",
    "artisanal_gold_council_mercury_reduction_reports",
  ],
  entities: [
    {
      id: "AGM-001",
      name: "Congo/DRC — Orpailleurs Artisanaux, Mercure Rivières & Communautés Empoisonnées",
      country: "RDC",
      mercury_poisoning_prevalence_health_impact_score: 99.0,
      illegal_mining_enforcement_gap_score: 97.0,
      community_rights_displacement_score: 95.0,
      minamata_convention_compliance_deficit_score: 93.0,
      composite_score: 96.1,
      risk_level: "critique",
      primary_pattern: "Orpailleurs artisanaux Maniema/Ituri, rivières contaminées mercure, communautés pêche intoxiquées",
      estimated_artisanal_gold_mercury_index: 9.61,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-002",
      name: "Pérou — Madre de Dios, Mercure Amazonie & 40 000 Mineurs ASGM",
      country: "Pérou",
      mercury_poisoning_prevalence_health_impact_score: 93.0,
      illegal_mining_enforcement_gap_score: 90.0,
      community_rights_displacement_score: 88.0,
      minamata_convention_compliance_deficit_score: 86.0,
      composite_score: 89.9,
      risk_level: "critique",
      primary_pattern: "40 000 mineurs ASGM Madre de Dios, 70% poissons Amazonie contaminés mercure OMS dépassé",
      estimated_artisanal_gold_mercury_index: 8.99,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-003",
      name: "Ghana — Galamsey Illégal, Mercure Cours d’Eau & Droits Communautés",
      country: "Ghana",
      mercury_poisoning_prevalence_health_impact_score: 85.0,
      illegal_mining_enforcement_gap_score: 82.0,
      community_rights_displacement_score: 80.0,
      minamata_convention_compliance_deficit_score: 78.0,
      composite_score: 81.45,
      risk_level: "critique",
      primary_pattern: "Galamsey illégal rivières Offin/Pra contaminées, 60% eau potable zones minières mercure dépassé",
      estimated_artisanal_gold_mercury_index: 8.15,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-004",
      name: "Brésil — Garimpeiros Yanomami, Mercure Sang 100x OMS & Génocide Silencieux",
      country: "Brésil",
      mercury_poisoning_prevalence_health_impact_score: 80.0,
      illegal_mining_enforcement_gap_score: 77.0,
      community_rights_displacement_score: 75.0,
      minamata_convention_compliance_deficit_score: 73.0,
      composite_score: 76.55,
      risk_level: "critique",
      primary_pattern: "Garimpeiros Territoire Yanomami, taux mercure sang 100x norme OMS, génocide sanitaire documenté",
      estimated_artisanal_gold_mercury_index: 7.66,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-005",
      name: "Colombie — ASGM Chocó, Groupes Armés & Mercure Rivière Atrato",
      country: "Colombie",
      mercury_poisoning_prevalence_health_impact_score: 61.0,
      illegal_mining_enforcement_gap_score: 58.0,
      community_rights_displacement_score: 56.0,
      minamata_convention_compliance_deficit_score: 54.0,
      composite_score: 57.55,
      risk_level: "élevé",
      primary_pattern: "ASGM Chocó sous contrôle FARC/ELN, rivière Atrato contaminée, Cour Constitutionnelle droits",
      estimated_artisanal_gold_mercury_index: 5.76,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-006",
      name: "Mongolie — Ninjas Orpailleurs, Mercure Steppe & Réglementation Partielle",
      country: "Mongolie",
      mercury_poisoning_prevalence_health_impact_score: 51.0,
      illegal_mining_enforcement_gap_score: 48.0,
      community_rights_displacement_score: 46.0,
      minamata_convention_compliance_deficit_score: 44.0,
      composite_score: 47.55,
      risk_level: "élevé",
      primary_pattern: "Ninjas orpailleurs 60 000 personnes, mercure steppe mongole, plan national ASGM incomplet",
      estimated_artisanal_gold_mercury_index: 4.76,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-007",
      name: "Philippines — Région Davao ASGM, Contrôle Partiel & DENR Inspections",
      country: "Philippines",
      mercury_poisoning_prevalence_health_impact_score: 32.0,
      illegal_mining_enforcement_gap_score: 29.0,
      community_rights_displacement_score: 27.0,
      minamata_convention_compliance_deficit_score: 25.0,
      composite_score: 28.6,
      risk_level: "modéré",
      primary_pattern: "ASGM Compostela Valley, DENR inspections renforcées, transition technologies sans mercure partielle",
      estimated_artisanal_gold_mercury_index: 2.86,
      last_updated: "2026-06-22",
    },
    {
      id: "AGM-008",
      name: "Convention Minamata / PNUE — Cadre Normatif, Plans ASGM & 140 Ratifications",
      country: "Global",
      mercury_poisoning_prevalence_health_impact_score: 13.0,
      illegal_mining_enforcement_gap_score: 11.0,
      community_rights_displacement_score: 9.0,
      minamata_convention_compliance_deficit_score: 7.0,
      composite_score: 10.3,
      risk_level: "faible",
      primary_pattern: "Convention Minamata 140 ratifications, plans nationaux ASGM obligatoires, fonds GEF transition",
      estimated_artisanal_gold_mercury_index: 1.03,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/artisanal_gold_mercury_rights_engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
