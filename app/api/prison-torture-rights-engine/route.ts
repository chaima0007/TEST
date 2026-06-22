import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-torture-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Torture Rights Engine Agent",
  domain: "prison_torture_rights",
  total_entities: 8,
  avg_composite: 61.38,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { torture_cruel_treatment_custodial_severity: 2, solitary_confinement_prolonged_abuse: 3, prison_overcrowding_inhuman_conditions_scale: 1, accountability_impunity_custodial_deaths_gap: 2 },
  top_risk_entities: [
    "Mexique/Amérique Centrale — Torture Systématique Police, Prisons Surpeuplées 300%, Disparitions Custodiales & Narco-Corruption",
    "Chine/Xinjiang — Torture Ouïghours Camps Détention, Soins Médicaux Refusés, Disparitions & Morts Politiques Étranges",
    "Philippines/Guerre Drogue — 30 000 Tués Custodiales Duterte, Torture Arrêtés, Prisons 500% & Impunité Totale",
  ],
  critical_alerts: [
    "Mexique/Amérique Centrale: torture_cruel_treatment_custodial_severity",
    "Chine/Xinjiang: solitary_confinement_prolonged_abuse",
    "Philippines/Guerre Drogue: prison_overcrowding_inhuman_conditions_scale",
    "Arabie Saoudite/Émirats: solitary_confinement_prolonged_abuse",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_torture_rights_index: 6.14,
  data_sources: [
    "un_committee_against_torture_annual_report",
    "amnesty_international_custodial_torture_global_review",
    "human_rights_watch_prison_conditions_overcrowding_report",
  ],
  entities: [
    { id: "PTR-001", name: "Mexique/Amérique Centrale — Torture Systématique Police, Prisons Surpeuplées 300%, Disparitions Custodiales & Narco-Corruption", country: "Mexique", composite_score: 93.1, torture_cruel_treatment_custodial_severity_score: 95.0, prison_overcrowding_inhuman_conditions_scale_score: 93.0, solitary_confinement_prolonged_abuse_score: 91.0, accountability_impunity_custodial_deaths_gap_score: 93.0, risk_level: "critique", primary_pattern: "torture_cruel_treatment_custodial_severity", estimated_prison_torture_rights_index: 9.31, last_updated: "2026-06-21" },
    { id: "PTR-002", name: "Chine/Xinjiang — Torture Ouïghours Camps Détention, Soins Médicaux Refusés, Disparitions & Morts Politiques Étranges", country: "Chine", composite_score: 90.4, torture_cruel_treatment_custodial_severity_score: 92.0, prison_overcrowding_inhuman_conditions_scale_score: 89.0, solitary_confinement_prolonged_abuse_score: 91.0, accountability_impunity_custodial_deaths_gap_score: 89.0, risk_level: "critique", primary_pattern: "solitary_confinement_prolonged_abuse", estimated_prison_torture_rights_index: 9.04, last_updated: "2026-06-21" },
    { id: "PTR-003", name: "Philippines/Guerre Drogue — 30 000 Tués Custodiales Duterte, Torture Arrêtés, Prisons 500% & Impunité Totale", country: "Philippines", composite_score: 87.35, torture_cruel_treatment_custodial_severity_score: 89.0, prison_overcrowding_inhuman_conditions_scale_score: 88.0, solitary_confinement_prolonged_abuse_score: 85.0, accountability_impunity_custodial_deaths_gap_score: 87.0, risk_level: "critique", primary_pattern: "prison_overcrowding_inhuman_conditions_scale", estimated_prison_torture_rights_index: 8.74, last_updated: "2026-06-21" },
    { id: "PTR-004", name: "Arabie Saoudite/Émirats — Torture Prisonniers Politiques, Isolement, Électrochocs & Aveux Forcés Dissidents", country: "Arabie Saoudite", composite_score: 84.6, torture_cruel_treatment_custodial_severity_score: 86.0, prison_overcrowding_inhuman_conditions_scale_score: 82.0, solitary_confinement_prolonged_abuse_score: 86.0, accountability_impunity_custodial_deaths_gap_score: 84.0, risk_level: "critique", primary_pattern: "solitary_confinement_prolonged_abuse", estimated_prison_torture_rights_index: 8.46, last_updated: "2026-06-21" },
    { id: "PTR-005", name: "USA/Solitary Confinement — 80 000 Prisonniers Isolement, SHU California 10+ Ans & Violence Guards Impunie", country: "USA", composite_score: 54.15, torture_cruel_treatment_custodial_severity_score: 55.0, prison_overcrowding_inhuman_conditions_scale_score: 52.0, solitary_confinement_prolonged_abuse_score: 57.0, accountability_impunity_custodial_deaths_gap_score: 52.0, risk_level: "élevé", primary_pattern: "solitary_confinement_prolonged_abuse", estimated_prison_torture_rights_index: 5.42, last_updated: "2026-06-21" },
    { id: "PTR-006", name: "Inde/Détentions Arbitraires — Custodial Deaths 1700/An, Torture Dalits/Minorités, Prisons Surpeuplées & UAPA", country: "Inde", composite_score: 51.2, torture_cruel_treatment_custodial_severity_score: 53.0, prison_overcrowding_inhuman_conditions_scale_score: 52.0, solitary_confinement_prolonged_abuse_score: 50.0, accountability_impunity_custodial_deaths_gap_score: 49.0, risk_level: "élevé", primary_pattern: "torture_cruel_treatment_custodial_severity", estimated_prison_torture_rights_index: 5.12, last_updated: "2026-06-21" },
    { id: "PTR-007", name: "CPT/SPT/APT — Comité Prévention Torture ONU, Visites Préventives & Lignes Directrices Nelson Mandela", country: "Global", composite_score: 26.05, torture_cruel_treatment_custodial_severity_score: 27.0, prison_overcrowding_inhuman_conditions_scale_score: 26.0, solitary_confinement_prolonged_abuse_score: 25.0, accountability_impunity_custodial_deaths_gap_score: 26.0, risk_level: "modéré", primary_pattern: "accountability_impunity_custodial_deaths_gap", estimated_prison_torture_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "PTR-008", name: "ONU/CAT/OPCAT — Convention Anti-Torture 1984, Protocole Facultatif OPCAT & SDG 16.3 État de Droit", country: "Global", composite_score: 4.2, torture_cruel_treatment_custodial_severity_score: 4.0, prison_overcrowding_inhuman_conditions_scale_score: 4.0, solitary_confinement_prolonged_abuse_score: 4.0, accountability_impunity_custodial_deaths_gap_score: 5.0, risk_level: "faible", primary_pattern: "accountability_impunity_custodial_deaths_gap", estimated_prison_torture_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-torture-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
