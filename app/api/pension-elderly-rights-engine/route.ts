import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pension-elderly-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[pension-elderly-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "pension_elderly_rights_engine",
  domain: "pension_elderly_rights",
  total_entities: 8,
  avg_composite: 61.77,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    { id: "PER-001", name: "Somalia — Absence totale système retraite, vieillards sans filet", score: 94.55, risk: "critique" },
    { id: "PER-002", name: "Afghanistan — Retraites inexistantes, personnes âgées dépendantes", score: 90.10, risk: "critique" },
    { id: "PER-003", name: "Yemen — Crise pensions fonctionnaires, aînés en famine", score: 87.85, risk: "critique" },
  ],
  critical_alerts: [
    "PER-001: Somalia — Absence totale système retraite — composite 94.55",
    "PER-002: Afghanistan — Retraites inexistantes, personnes âgées dépendantes — composite 90.10",
    "PER-003: Yemen — Crise pensions fonctionnaires, aînés en famine — composite 87.85",
    "PER-004: Haiti — Effondrement système retraite, personnes âgées abandonnées — composite 82.40",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_pension_elderly_rights_index: 6.18,
  data_sources: [
    "ilo_world_social_protection_report_2024",
    "helpage_global_agewatch_index_2023",
    "who_ageing_health_report_2023",
    "un_desa_ageing_population_data_2024",
  ],
  entities: [
    {
      id: "PER-001",
      name: "Somalia — Absence totale système retraite, vieillards sans filet",
      country: "Somalia",
      pension_coverage_adequacy_score: 96.0,
      elderly_healthcare_access_deficit_score: 94.0,
      age_discrimination_employment_score: 93.0,
      state_social_protection_elderly_deficit_score: 95.0,
      composite_score: 94.55,
      risk_level: "critique",
      primary_pattern: "Aucun système de retraite formel, 97% personnes âgées sans pension, dépendance totale famille",
      estimated_pension_elderly_rights_index: 9.46,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-002",
      name: "Afghanistan — Retraites inexistantes, personnes âgées dépendantes",
      country: "Afghanistan",
      pension_coverage_adequacy_score: 91.0,
      elderly_healthcare_access_deficit_score: 90.0,
      age_discrimination_employment_score: 89.0,
      state_social_protection_elderly_deficit_score: 90.0,
      composite_score: 90.10,
      risk_level: "critique",
      primary_pattern: "Taliban suspend pensions fonctionnaires, femmes âgées exclues, système santé effondré",
      estimated_pension_elderly_rights_index: 9.01,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-003",
      name: "Yemen — Crise pensions fonctionnaires, aînés en famine",
      country: "Yemen",
      pension_coverage_adequacy_score: 89.0,
      elderly_healthcare_access_deficit_score: 88.0,
      age_discrimination_employment_score: 86.0,
      state_social_protection_elderly_deficit_score: 88.0,
      composite_score: 87.85,
      risk_level: "critique",
      primary_pattern: "Pensions non versées depuis 2016, 21M en insécurité alimentaire incluant aînés, hôpitaux détruits",
      estimated_pension_elderly_rights_index: 8.79,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-004",
      name: "Haiti — Effondrement système retraite, personnes âgées abandonnées",
      country: "Haiti",
      pension_coverage_adequacy_score: 83.0,
      elderly_healthcare_access_deficit_score: 82.0,
      age_discrimination_employment_score: 81.0,
      state_social_protection_elderly_deficit_score: 83.0,
      composite_score: 82.40,
      risk_level: "critique",
      primary_pattern: "ONA (retraite) insolvable, gangs contrôlent accès soins, aînés victimes violence",
      estimated_pension_elderly_rights_index: 8.24,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-005",
      name: "India — Couverture pension fragmentée, 90% sans protection formelle",
      country: "India",
      pension_coverage_adequacy_score: 53.0,
      elderly_healthcare_access_deficit_score: 52.0,
      age_discrimination_employment_score: 51.0,
      state_social_protection_elderly_deficit_score: 53.0,
      composite_score: 52.40,
      risk_level: "élevé",
      primary_pattern: "90% travailleurs informels sans retraite, Ayushman Bharat limité, discrimination âge marché emploi",
      estimated_pension_elderly_rights_index: 5.24,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-006",
      name: "Nigeria — Pensions impayées, fonctionnaires retraités sans revenus",
      country: "Nigeria",
      pension_coverage_adequacy_score: 52.0,
      elderly_healthcare_access_deficit_score: 51.0,
      age_discrimination_employment_score: 52.0,
      state_social_protection_elderly_deficit_score: 52.0,
      composite_score: 51.90,
      risk_level: "élevé",
      primary_pattern: "Pensions fonctionnaires impayées 14 États, Contributory Pension Scheme exclu informel",
      estimated_pension_elderly_rights_index: 5.19,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-007",
      name: "USA — Inégalités retraite raciales, Medicare gaps, pauvreté seniors",
      country: "USA",
      pension_coverage_adequacy_score: 30.0,
      elderly_healthcare_access_deficit_score: 31.0,
      age_discrimination_employment_score: 29.0,
      state_social_protection_elderly_deficit_score: 30.0,
      composite_score: 30.00,
      risk_level: "modéré",
      primary_pattern: "Écart pension racial 40%, Medicare lacunes soins dentaires/vision, ADEA sous-appliqué",
      estimated_pension_elderly_rights_index: 3.00,
      last_updated: "2026-06-22",
    },
    {
      id: "PER-008",
      name: "Denmark — Modèle pension universel, protection seniors exemplaire",
      country: "Denmark",
      pension_coverage_adequacy_score: 5.0,
      elderly_healthcare_access_deficit_score: 5.0,
      age_discrimination_employment_score: 5.0,
      state_social_protection_elderly_deficit_score: 5.0,
      composite_score: 5.00,
      risk_level: "faible",
      primary_pattern: "Folkepension universel, Ældrebolig soins seniors, taux pauvreté personnes âgées 3%",
      estimated_pension_elderly_rights_index: 0.50,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const upstream = await fetch(`${SWARM_API_URL}/pension-elderly-rights-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`upstream ${upstream.status}`);
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }));
  }
}
