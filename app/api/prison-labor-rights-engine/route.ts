import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-labor-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Labor Rights Engine Agent",
  domain: "prison_labor_rights",
  total_entities: 8,
  avg_composite: 61.72,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_prison_labor_coercion_severity: 4, wage_theft_below_minimum_compensation_scale: 1, unsafe_working_conditions_incarcerated: 1, legal_protection_prisoner_worker_gap: 2 },
  top_risk_entities: [
    "USA — 800 000 Détenus Forcés Travailler 0,13-0,52$/h, 13e Amendement Exception Esclavage & UNICOR Profit",
    "Chine — Laogai/Laojiao Travail Rééducatif, Camps Xinjiang Ouïghours & Production Exportation Forcée",
    "Russie — Colonies Pénitentiaires IK Travail Obligatoire, Zéro Salaire & Conditions Soviétiques Maintenues",
  ],
  critical_alerts: [
    "USA: forced_prison_labor_coercion_severity",
    "Chine: forced_prison_labor_coercion_severity",
    "Russie: wage_theft_below_minimum_compensation_scale",
    "Thaïlande/Asie SE: unsafe_working_conditions_incarcerated",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_labor_rights_index: 6.17,
  data_sources: [
    "aclu_captive_labor_exploitation_prison_workforce_report",
    "human_rights_watch_prison_labor_wages_conditions_report",
    "ilo_forced_labour_convention_c29_prison_labour_review",
  ],
  entities: [
    { entity_id: "PLR-001", name: "USA — 800 000 Détenus Forcés Travailler 0,13-0,52$/h, 13e Amendement Exception Esclavage & UNICOR Profit", country: "États-Unis", composite_score: 93.4, forced_prison_labor_coercion_severity_score: 96.0, wage_theft_below_minimum_compensation_scale_score: 93.0, unsafe_working_conditions_incarcerated_score: 91.0, legal_protection_prisoner_worker_gap_score: 93.0, risk_level: "critique", primary_pattern: "forced_prison_labor_coercion_severity", estimated_prison_labor_rights_index: 9.34, last_updated: "2026-06-21" },
    { entity_id: "PLR-002", name: "Chine — Laogai/Laojiao Travail Rééducatif, Camps Xinjiang Ouïghours & Production Exportation Forcée", country: "Chine", composite_score: 91.25, forced_prison_labor_coercion_severity_score: 94.0, wage_theft_below_minimum_compensation_scale_score: 91.0, unsafe_working_conditions_incarcerated_score: 90.0, legal_protection_prisoner_worker_gap_score: 89.0, risk_level: "critique", primary_pattern: "forced_prison_labor_coercion_severity", estimated_prison_labor_rights_index: 9.13, last_updated: "2026-06-21" },
    { entity_id: "PLR-003", name: "Russie — Colonies Pénitentiaires IK Travail Obligatoire, Zéro Salaire & Conditions Soviétiques Maintenues", country: "Russie", composite_score: 88.0, forced_prison_labor_coercion_severity_score: 91.0, wage_theft_below_minimum_compensation_scale_score: 87.0, unsafe_working_conditions_incarcerated_score: 87.0, legal_protection_prisoner_worker_gap_score: 86.0, risk_level: "critique", primary_pattern: "wage_theft_below_minimum_compensation_scale", estimated_prison_labor_rights_index: 8.8, last_updated: "2026-06-21" },
    { entity_id: "PLR-004", name: "Thaïlande/Asie SE — Détenus Loués Entreprises Privées, Usines Prison Sans EPI & Pas d'Assurance Travail", country: "Thaïlande/Asie SE", composite_score: 85.8, forced_prison_labor_coercion_severity_score: 89.0, wage_theft_below_minimum_compensation_scale_score: 85.0, unsafe_working_conditions_incarcerated_score: 85.0, legal_protection_prisoner_worker_gap_score: 83.0, risk_level: "critique", primary_pattern: "unsafe_working_conditions_incarcerated", estimated_prison_labor_rights_index: 8.58, last_updated: "2026-06-21" },
    { entity_id: "PLR-005", name: "Brésil — FUNAP Travail Pénitentiaire, Remise Peine vs Exploitation, Conditions Insalubres & Surpopulation", country: "Brésil", composite_score: 53.45, forced_prison_labor_coercion_severity_score: 56.0, wage_theft_below_minimum_compensation_scale_score: 52.0, unsafe_working_conditions_incarcerated_score: 53.0, legal_protection_prisoner_worker_gap_score: 52.0, risk_level: "élevé", primary_pattern: "forced_prison_labor_coercion_severity", estimated_prison_labor_rights_index: 5.35, last_updated: "2026-06-21" },
    { entity_id: "PLR-006", name: "UE — Travail Pénitentiaire Légal Majorité États, Salaires 10-25% SMIC & Exclusion Droit Travail Commun", country: "Union Européenne", composite_score: 51.5, forced_prison_labor_coercion_severity_score: 54.0, wage_theft_below_minimum_compensation_scale_score: 51.0, unsafe_working_conditions_incarcerated_score: 51.0, legal_protection_prisoner_worker_gap_score: 49.0, risk_level: "élevé", primary_pattern: "legal_protection_prisoner_worker_gap", estimated_prison_labor_rights_index: 5.15, last_updated: "2026-06-21" },
    { entity_id: "PLR-007", name: "PRI/Anti-Slavery Int'l — Standards Travail Pénitentiaire, Plaidoyer Salaire Minimum & Abolition Travail Forcé", country: "Global", composite_score: 25.9, forced_prison_labor_coercion_severity_score: 24.0, wage_theft_below_minimum_compensation_scale_score: 28.0, unsafe_working_conditions_incarcerated_score: 26.0, legal_protection_prisoner_worker_gap_score: 26.0, risk_level: "modéré", primary_pattern: "legal_protection_prisoner_worker_gap", estimated_prison_labor_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "PLR-008", name: "ONU/ILO — Convention C29 Travail Forcé, Protocole 2014 & Standards Minima Travail Pénitentiaire", country: "Global", composite_score: 4.45, forced_prison_labor_coercion_severity_score: 4.0, wage_theft_below_minimum_compensation_scale_score: 5.0, unsafe_working_conditions_incarcerated_score: 4.0, legal_protection_prisoner_worker_gap_score: 5.0, risk_level: "faible", primary_pattern: "forced_prison_labor_coercion_severity", estimated_prison_labor_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-labor-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
