import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[tobacco-child-labor-rights] SWARM_API_URL non défini — mode mock activé");
}

const MOCK = {
  agent: "tobacco_child_labor_rights_engine",
  domain: "tobacco_child_labor_rights",
  total_entities: 8,
  avg_composite: 62.16,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    child_labor_exploitation: 3,
    hazardous_work_exposure: 2,
    enforcement_deficit: 2,
    corporate_accountability: 1,
  },
  top_risk_entities: [
    { id: "TBL-001", name: "Zimbabwe — 1.5M Enfants Tabac, Nicotine Absorption Cutanée & Impunité Totale", score: 96.1, risk: "critique" },
    { id: "TBL-003", name: "Malawi — 78% PIB Tabac, Travail Enfant Systémique & Pauvreté Rurale", score: 81.45, risk: "critique" },
    { id: "TBL-002", name: "Tanzanie — Enfants Dès 5 Ans Plantations, Green Tobacco Sickness & Absence Loi", score: 89.9, risk: "critique" },
  ],
  critical_alerts: [
    "TBL-001: Zimbabwe — 1.5M Enfants Tabac, Nicotine Absorption Cutanée & Impunité Totale — composite 96.1",
    "TBL-002: Tanzanie — Enfants Dès 5 Ans Plantations, Green Tobacco Sickness & Absence Loi — composite 89.9",
    "TBL-003: Malawi — 78% PIB Tabac, Travail Enfant Systémique & Pauvreté Rurale — composite 81.45",
    "TBL-004: Inde — 1.2M Enfants Bidi & Champs Tabac, Bonded Labor & Dettes Héréditaires — composite 76.55",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_tobacco_child_labor_index: 6.21,
  data_sources: [
    "ilo_child_labour_global_estimates_2022",
    "human_rights_watch_tobacco_child_labor_report",
    "plan_international_child_labor_tobacco_fields",
    "who_green_tobacco_sickness_occupational_health",
  ],
  entities: [
    {
      id: "TBL-001",
      name: "Zimbabwe — 1.5M Enfants Tabac, Nicotine Absorption Cutanée & Impunité Totale",
      country: "Zimbabwe",
      child_labor_prevalence_hazard_score: 99.0,
      green_tobacco_sickness_health_impact_score: 97.0,
      enforcement_legal_protection_deficit_score: 95.0,
      corporate_accountability_supply_chain_score: 93.0,
      composite_score: 96.1,
      risk_level: "critique",
      primary_pattern: "1,5M enfants plantations tabac, absorption nicotine cutanée, aucune protection légale effective",
      estimated_tobacco_child_labor_index: 9.61,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-002",
      name: "Tanzanie — Enfants Dès 5 Ans Plantations, Green Tobacco Sickness & Absence Loi",
      country: "Tanzanie",
      child_labor_prevalence_hazard_score: 93.0,
      green_tobacco_sickness_health_impact_score: 90.0,
      enforcement_legal_protection_deficit_score: 88.0,
      corporate_accountability_supply_chain_score: 86.0,
      composite_score: 89.9,
      risk_level: "critique",
      primary_pattern: "Enfants dès 5 ans champs tabac, green tobacco sickness non traitée, loi inappliquée",
      estimated_tobacco_child_labor_index: 8.99,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-003",
      name: "Malawi — 78% PIB Tabac, Travail Enfant Systémique & Pauvreté Rurale",
      country: "Malawi",
      child_labor_prevalence_hazard_score: 85.0,
      green_tobacco_sickness_health_impact_score: 82.0,
      enforcement_legal_protection_deficit_score: 80.0,
      corporate_accountability_supply_chain_score: 78.0,
      composite_score: 81.45,
      risk_level: "critique",
      primary_pattern: "78% PIB tabac, 1,4M enfants travailleurs agricoles, poverty trap intergénérationnel",
      estimated_tobacco_child_labor_index: 8.15,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-004",
      name: "Inde — 1.2M Enfants Bidi & Champs Tabac, Bonded Labor & Dettes Héréditaires",
      country: "Inde",
      child_labor_prevalence_hazard_score: 80.0,
      green_tobacco_sickness_health_impact_score: 77.0,
      enforcement_legal_protection_deficit_score: 75.0,
      corporate_accountability_supply_chain_score: 73.0,
      composite_score: 76.55,
      risk_level: "critique",
      primary_pattern: "1,2M enfants industrie bidi et champs tabac Andhra Pradesh, bonded labor héréditaire",
      estimated_tobacco_child_labor_index: 7.66,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-005",
      name: "Brésil — Plantation Tabac Sud, Contrôle Partiel & Lacunes Application",
      country: "Brésil",
      child_labor_prevalence_hazard_score: 61.0,
      green_tobacco_sickness_health_impact_score: 58.0,
      enforcement_legal_protection_deficit_score: 56.0,
      corporate_accountability_supply_chain_score: 54.0,
      composite_score: 57.55,
      risk_level: "élevé",
      primary_pattern: "Plantations tabac Rio Grande do Sul, contrôle MTE partiel, filières non certifiées",
      estimated_tobacco_child_labor_index: 5.76,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-006",
      name: "Philippines — Région Ilocos, Travail Saisonnier Enfants & BAT Supply Chain",
      country: "Philippines",
      child_labor_prevalence_hazard_score: 51.0,
      green_tobacco_sickness_health_impact_score: 48.0,
      enforcement_legal_protection_deficit_score: 46.0,
      corporate_accountability_supply_chain_score: 44.0,
      composite_score: 47.55,
      risk_level: "élevé",
      primary_pattern: "Région Ilocos Norte travail saisonnier enfants, présence BAT & Philip Morris sans audit",
      estimated_tobacco_child_labor_index: 4.76,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-007",
      name: "USA — Exemption Agricole Tabac, Mineurs 12 Ans Légaux & FLSA Gap",
      country: "États-Unis",
      child_labor_prevalence_hazard_score: 32.0,
      green_tobacco_sickness_health_impact_score: 29.0,
      enforcement_legal_protection_deficit_score: 27.0,
      corporate_accountability_supply_chain_score: 25.0,
      composite_score: 28.6,
      risk_level: "modéré",
      primary_pattern: "Exemption agricole FLSA autorise mineurs 12 ans tabac Kentucky/NC sans limite heures",
      estimated_tobacco_child_labor_index: 2.86,
      last_updated: "2026-06-22",
    },
    {
      id: "TBL-008",
      name: "UE / Directive Travail des Enfants — Cadre Normatif, Due Diligence & CSDDD",
      country: "Union Européenne",
      child_labor_prevalence_hazard_score: 13.0,
      green_tobacco_sickness_health_impact_score: 11.0,
      enforcement_legal_protection_deficit_score: 9.0,
      corporate_accountability_supply_chain_score: 7.0,
      composite_score: 10.3,
      risk_level: "faible",
      primary_pattern: "CSDDD 2024 due diligence obligatoire, interdiction importation travail forcé enfants UE",
      estimated_tobacco_child_labor_index: 1.03,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/tobacco_child_labor_rights_engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
