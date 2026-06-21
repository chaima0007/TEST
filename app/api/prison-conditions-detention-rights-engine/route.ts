import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-conditions-detention-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Conditions Detention Rights Engine Agent",
  domain: "prison_conditions_detention_rights",
  total_entities: 8,
  avg_composite: 62.08,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { overcrowding_inhumane_conditions_scale: 2, torture_ill_treatment_detention_severity: 2, solitary_confinement_isolation_abuse: 2, prison_healthcare_legal_access_deficit_gap: 2 },
  top_risk_entities: [
    "Libye/Prisons Milices — Torture Généralisée, Détention Arbitraire & Absence Contrôle Judiciaire",
    "Philippines/Guerre Drogues — Prisons 800% Capacité, Torture Systématique & Morts en Détention",
    "Égypte/Prisons Politiques — Tortures Al-Aqrab, Isolement Prolongé & Détention Sans Procès",
  ],
  critical_alerts: [
    "Libye/Prisons Milices: torture_ill_treatment_detention_severity",
    "Philippines/Guerre Drogues: overcrowding_inhumane_conditions_scale",
    "Égypte/Prisons Politiques: solitary_confinement_isolation_abuse",
    "El Salvador/Bukele Méga-Prison: overcrowding_inhumane_conditions_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_conditions_detention_rights_index: 6.21,
  data_sources: [
    "un_special_rapporteur_torture_report_detention_conditions_global",
    "amnesty_international_cpt_annual_report_prison_overcrowding_ill_treatment",
    "un_standard_minimum_rules_treatment_prisoners_nelson_mandela_rules_2015",
  ],
  entities: [
    { id: "PCDR-001", name: "Philippines/Guerre Drogues — Prisons 800% Capacité, Torture Systématique & Morts en Détention", country: "Asie du Sud-Est", composite_score: 90.6, torture_ill_treatment_detention_severity_score: 92.0, overcrowding_inhumane_conditions_scale_score: 95.0, solitary_confinement_isolation_abuse_score: 85.0, prison_healthcare_legal_access_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "overcrowding_inhumane_conditions_scale", estimated_prison_conditions_detention_rights_index: 9.06, last_updated: "2026-06-21" },
    { id: "PCDR-002", name: "Libye/Prisons Milices — Torture Généralisée, Détention Arbitraire & Absence Contrôle Judiciaire", country: "Afrique du Nord", composite_score: 91.4, torture_ill_treatment_detention_severity_score: 95.0, overcrowding_inhumane_conditions_scale_score: 88.0, solitary_confinement_isolation_abuse_score: 90.0, prison_healthcare_legal_access_deficit_gap_score: 92.0, risk_level: "critique", primary_pattern: "torture_ill_treatment_detention_severity", estimated_prison_conditions_detention_rights_index: 9.14, last_updated: "2026-06-21" },
    { id: "PCDR-003", name: "Égypte/Prisons Politiques — Tortures Al-Aqrab, Isolement Prolongé & Détention Sans Procès", country: "Afrique du Nord", composite_score: 88.85, torture_ill_treatment_detention_severity_score: 90.0, overcrowding_inhumane_conditions_scale_score: 85.0, solitary_confinement_isolation_abuse_score: 92.0, prison_healthcare_legal_access_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "solitary_confinement_isolation_abuse", estimated_prison_conditions_detention_rights_index: 8.89, last_updated: "2026-06-21" },
    { id: "PCDR-004", name: "El Salvador/Bukele Méga-Prison — 40k Détenus CECOT, Surpopulation Extrême & Droits Bafoués", country: "Amérique Centrale", composite_score: 86.9, torture_ill_treatment_detention_severity_score: 85.0, overcrowding_inhumane_conditions_scale_score: 92.0, solitary_confinement_isolation_abuse_score: 88.0, prison_healthcare_legal_access_deficit_gap_score: 82.0, risk_level: "critique", primary_pattern: "overcrowding_inhumane_conditions_scale", estimated_prison_conditions_detention_rights_index: 8.69, last_updated: "2026-06-21" },
    { id: "PCDR-005", name: "USA/Comté Prisons — Surpopulation Chronique, Isolement & Accès Soins Mentaux Déficient", country: "Amérique du Nord", composite_score: 56.6, torture_ill_treatment_detention_severity_score: 52.0, overcrowding_inhumane_conditions_scale_score: 58.0, solitary_confinement_isolation_abuse_score: 62.0, prison_healthcare_legal_access_deficit_gap_score: 55.0, risk_level: "élevé", primary_pattern: "solitary_confinement_isolation_abuse", estimated_prison_conditions_detention_rights_index: 5.66, last_updated: "2026-06-21" },
    { id: "PCDR-006", name: "Russie/Colonies Pénales Arctique — Conditions Extrêmes, Privations & Travail Forcé Sibérie", country: "Europe de l'Est", composite_score: 53.1, torture_ill_treatment_detention_severity_score: 55.0, overcrowding_inhumane_conditions_scale_score: 48.0, solitary_confinement_isolation_abuse_score: 52.0, prison_healthcare_legal_access_deficit_gap_score: 58.0, risk_level: "élevé", primary_pattern: "prison_healthcare_legal_access_deficit_gap", estimated_prison_conditions_detention_rights_index: 5.31, last_updated: "2026-06-21" },
    { id: "PCDR-007", name: "CPT/APT — Comité Prévention Torture, Inspections & Mécanismes Nationaux Monitoring Détention", country: "Global", composite_score: 23.6, torture_ill_treatment_detention_severity_score: 25.0, overcrowding_inhumane_conditions_scale_score: 22.0, solitary_confinement_isolation_abuse_score: 20.0, prison_healthcare_legal_access_deficit_gap_score: 28.0, risk_level: "modéré", primary_pattern: "prison_healthcare_legal_access_deficit_gap", estimated_prison_conditions_detention_rights_index: 2.36, last_updated: "2026-06-21" },
    { id: "PCDR-008", name: "ONU/Règles Nelson Mandela 2015 — Standards Minima Traitement Détenus & Réforme Pénitentiaire", country: "Global", composite_score: 5.6, torture_ill_treatment_detention_severity_score: 5.0, overcrowding_inhumane_conditions_scale_score: 6.0, solitary_confinement_isolation_abuse_score: 4.0, prison_healthcare_legal_access_deficit_gap_score: 8.0, risk_level: "faible", primary_pattern: "torture_ill_treatment_detention_severity", estimated_prison_conditions_detention_rights_index: 0.56, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-conditions-detention-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
