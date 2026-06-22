import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[seafarers-maritime-labor-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Seafarers Maritime Labor Rights Engine Agent",
  domain: "seafarers_maritime_labor_rights",
  total_entities: 8,
  avg_composite: 61.44,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { flag_state_labor_standard_evasion_scale: 3, ship_abandonment_wage_theft_severity: 3, unsafe_working_conditions_fatality_risk: 1, repatriation_recruitment_fee_exploitation_gap: 1 },
  top_risk_entities: [
    "Panama/Liberia Flag Convenience — 40% Flotte Mondiale Sous Standards ITF Non Respectés, Salaires Volés & Abandons en Mer",
    "Golfe/Méditerranée — Marins Asiatiques Abandonnés Ports Grecs/Turcs, Passeports Confisqués & Frais Recrutement 15 000$",
    "Chine/Asie SE Chantiers — Conditions Mortelles Constructions Navales, 500+ Décès/An & Syndicats Interdits",
  ],
  critical_alerts: [
    "Panama/Liberia Flag Convenience: flag_state_labor_standard_evasion_scale",
    "Golfe/Méditerranée: ship_abandonment_wage_theft_severity",
    "Chine/Asie SE Chantiers: unsafe_working_conditions_fatality_risk",
    "Méditerranée Migrants: ship_abandonment_wage_theft_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_seafarers_maritime_labor_rights_index: 6.14,
  data_sources: [
    "ilo_maritime_labour_convention_mlc2006_reports",
    "itf_seafarers_abandonment_database",
    "imo_flag_state_compliance_audit_reports",
  ],
  entities: [
    { id: "SML-001", name: "Panama/Liberia Flag Convenience — 40% Flotte Mondiale Sous Standards ITF Non Respectés, Salaires Volés & Abandons en Mer", country: "Panama/Liberia", composite_score: 92.95, ship_abandonment_wage_theft_severity_score: 95.0, flag_state_labor_standard_evasion_scale_score: 93.0, unsafe_working_conditions_fatality_risk_score: 92.0, repatriation_recruitment_fee_exploitation_gap_score: 91.0, risk_level: "critique", primary_pattern: "flag_state_labor_standard_evasion_scale", estimated_seafarers_maritime_labor_rights_index: 9.30, last_updated: "2026-06-21" },
    { id: "SML-002", name: "Golfe/Méditerranée — Marins Asiatiques Abandonnés Ports Grecs/Turcs, Passeports Confisqués & Frais Recrutement 15 000$", country: "Méditerranée", composite_score: 89.85, ship_abandonment_wage_theft_severity_score: 92.0, flag_state_labor_standard_evasion_scale_score: 89.0, unsafe_working_conditions_fatality_risk_score: 88.0, repatriation_recruitment_fee_exploitation_gap_score: 90.0, risk_level: "critique", primary_pattern: "ship_abandonment_wage_theft_severity", estimated_seafarers_maritime_labor_rights_index: 8.99, last_updated: "2026-06-21" },
    { id: "SML-003", name: "Chine/Asie SE Chantiers — Conditions Mortelles Constructions Navales, 500+ Décès/An & Syndicats Interdits", country: "Chine/Asie SE", composite_score: 86.90, ship_abandonment_wage_theft_severity_score: 89.0, flag_state_labor_standard_evasion_scale_score: 87.0, unsafe_working_conditions_fatality_risk_score: 85.0, repatriation_recruitment_fee_exploitation_gap_score: 86.0, risk_level: "critique", primary_pattern: "unsafe_working_conditions_fatality_risk", estimated_seafarers_maritime_labor_rights_index: 8.69, last_updated: "2026-06-21" },
    { id: "SML-004", name: "Méditerranée Migrants — Marins Forcés Transporter Migrants Sous Menace, Criminalisation Sauvetage & Abandons", country: "Méditerranée", composite_score: 83.85, ship_abandonment_wage_theft_severity_score: 86.0, flag_state_labor_standard_evasion_scale_score: 83.0, unsafe_working_conditions_fatality_risk_score: 82.0, repatriation_recruitment_fee_exploitation_gap_score: 84.0, risk_level: "critique", primary_pattern: "ship_abandonment_wage_theft_severity", estimated_seafarers_maritime_labor_rights_index: 8.39, last_updated: "2026-06-21" },
    { id: "SML-005", name: "Philippines — 1/3 Marins Monde Filipino, Agences Recrutement Frais Illégaux, Contrats Substitués & Plaintes Ignorées", country: "Philippines", composite_score: 54.85, ship_abandonment_wage_theft_severity_score: 57.0, flag_state_labor_standard_evasion_scale_score: 54.0, unsafe_working_conditions_fatality_risk_score: 53.0, repatriation_recruitment_fee_exploitation_gap_score: 55.0, risk_level: "élevé", primary_pattern: "repatriation_recruitment_fee_exploitation_gap", estimated_seafarers_maritime_labor_rights_index: 5.49, last_updated: "2026-06-21" },
    { id: "SML-006", name: "Marins COVID — 400 000 Bloqués Bateaux 2020-21, Rotations Refusées, Santé Mentale & Suicides en Haute Mer", country: "Global", composite_score: 51.85, ship_abandonment_wage_theft_severity_score: 54.0, flag_state_labor_standard_evasion_scale_score: 51.0, unsafe_working_conditions_fatality_risk_score: 50.0, repatriation_recruitment_fee_exploitation_gap_score: 52.0, risk_level: "élevé", primary_pattern: "ship_abandonment_wage_theft_severity", estimated_seafarers_maritime_labor_rights_index: 5.19, last_updated: "2026-06-21" },
    { id: "SML-007", name: "ITF/International Transport Workers Federation — Campagnes Abandonment, Standards MLC 2006 & Fonds Secours Marins", country: "Global", composite_score: 27.05, ship_abandonment_wage_theft_severity_score: 28.0, flag_state_labor_standard_evasion_scale_score: 26.0, unsafe_working_conditions_fatality_risk_score: 27.0, repatriation_recruitment_fee_exploitation_gap_score: 27.0, risk_level: "modéré", primary_pattern: "flag_state_labor_standard_evasion_scale", estimated_seafarers_maritime_labor_rights_index: 2.71, last_updated: "2026-06-21" },
    { id: "SML-008", name: "OIT/MLC 2006 — Maritime Labour Convention 2006, Certificats Conformité & SDG 14 Océans Travail Décent", country: "Global", composite_score: 4.25, ship_abandonment_wage_theft_severity_score: 4.0, flag_state_labor_standard_evasion_scale_score: 4.0, unsafe_working_conditions_fatality_risk_score: 5.0, repatriation_recruitment_fee_exploitation_gap_score: 4.0, risk_level: "faible", primary_pattern: "flag_state_labor_standard_evasion_scale", estimated_seafarers_maritime_labor_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/seafarers-maritime-labor-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
