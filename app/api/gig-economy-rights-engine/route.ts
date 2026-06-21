import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gig-economy-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Gig Economy Rights Engine Agent",
  domain: "gig_economy_rights",
  total_entities: 8,
  avg_composite: 60.97,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { algorithmic_wage_theft_control_severity: 4, platform_misclassification_labor_rights_gap: 2, social_protection_gig_worker_exclusion: 2 },
  top_risk_entities: [
    "UK/Deliveroo-Uber — 5,5M Travailleurs Plateforme, Algorithme Salaire, Zéro Congés Payés & Accidents Non Couverts",
    "India/Ola-Swiggy — 7,7M Livreurs Sans Statut, Désactivation Arbitraire & Absence Sécurité Sociale",
    "USA/Amazon-DoorDash — Prop 22 Californie, Déclassification Délibérée & Accidentés Sans Indemnisation",
  ],
  critical_alerts: [
    "UK/Deliveroo-Uber: algorithmic_wage_theft_control_severity",
    "India/Ola-Swiggy: platform_misclassification_labor_rights_gap",
    "USA/Amazon-DoorDash: platform_misclassification_labor_rights_gap",
    "Afrique Sub-Saharienne: social_protection_gig_worker_exclusion",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_gig_economy_rights_index: 6.10,
  data_sources: [
    "ilo_platform_work_and_decent_work_report",
    "ituc_gig_economy_workers_rights_survey",
    "oxford_internet_institute_platform_labour_index",
  ],
  entities: [
    { id: "GER-001", name: "UK/Deliveroo-Uber — 5,5M Travailleurs Plateforme, Algorithme Salaire, Zéro Congés Payés & Accidents Non Couverts", country: "Royaume-Uni", composite_score: 92.95, algorithmic_wage_theft_control_severity_score: 95.0, zero_hours_contract_precarity_scale_score: 93.0, social_protection_gig_worker_exclusion_score: 92.0, platform_misclassification_labor_rights_gap_score: 91.0, risk_level: "critique", primary_pattern: "algorithmic_wage_theft_control_severity", estimated_gig_economy_rights_index: 9.30, last_updated: "2026-06-21" },
    { id: "GER-002", name: "India/Ola-Swiggy — 7,7M Livreurs Sans Statut, Désactivation Arbitraire & Absence Sécurité Sociale", country: "Inde", composite_score: 89.95, algorithmic_wage_theft_control_severity_score: 92.0, zero_hours_contract_precarity_scale_score: 90.0, social_protection_gig_worker_exclusion_score: 89.0, platform_misclassification_labor_rights_gap_score: 88.0, risk_level: "critique", primary_pattern: "platform_misclassification_labor_rights_gap", estimated_gig_economy_rights_index: 9.00, last_updated: "2026-06-21" },
    { id: "GER-003", name: "USA/Amazon-DoorDash — Prop 22 Californie, Déclassification Délibérée & Accidentés Sans Indemnisation", country: "États-Unis", composite_score: 86.95, algorithmic_wage_theft_control_severity_score: 89.0, zero_hours_contract_precarity_scale_score: 87.0, social_protection_gig_worker_exclusion_score: 86.0, platform_misclassification_labor_rights_gap_score: 85.0, risk_level: "critique", primary_pattern: "platform_misclassification_labor_rights_gap", estimated_gig_economy_rights_index: 8.70, last_updated: "2026-06-21" },
    { id: "GER-004", name: "Afrique Sub-Saharienne — Jumia/SafeBoda, Zéro Protection Légale, Risques Sécurité Routière & Exploitation", country: "Afrique Sub-Saharienne", composite_score: 83.95, algorithmic_wage_theft_control_severity_score: 86.0, zero_hours_contract_precarity_scale_score: 84.0, social_protection_gig_worker_exclusion_score: 83.0, platform_misclassification_labor_rights_gap_score: 82.0, risk_level: "critique", primary_pattern: "social_protection_gig_worker_exclusion", estimated_gig_economy_rights_index: 8.40, last_updated: "2026-06-21" },
    { id: "GER-005", name: "EU/Directive Plateforme — Directive 2024 Implémentation Lente, États Résistants & Protection Partielle", country: "Union Européenne", composite_score: 52.95, algorithmic_wage_theft_control_severity_score: 55.0, zero_hours_contract_precarity_scale_score: 53.0, social_protection_gig_worker_exclusion_score: 52.0, platform_misclassification_labor_rights_gap_score: 51.0, risk_level: "élevé", primary_pattern: "algorithmic_wage_theft_control_severity", estimated_gig_economy_rights_index: 5.30, last_updated: "2026-06-21" },
    { id: "GER-006", name: "Asie du Sud-Est/Grab — Reclassification Refusée, Heures Excessives & Discrimination Algorithme", country: "Asie du Sud-Est", composite_score: 50.95, algorithmic_wage_theft_control_severity_score: 53.0, zero_hours_contract_precarity_scale_score: 51.0, social_protection_gig_worker_exclusion_score: 50.0, platform_misclassification_labor_rights_gap_score: 49.0, risk_level: "élevé", primary_pattern: "algorithmic_wage_theft_control_severity", estimated_gig_economy_rights_index: 5.10, last_updated: "2026-06-21" },
    { id: "GER-007", name: "ITUC/UNI Global — Droits Travailleurs Plateforme, Campagne Justice Numérique & Standards OIT", country: "Global", composite_score: 26.05, algorithmic_wage_theft_control_severity_score: 27.0, zero_hours_contract_precarity_scale_score: 26.0, social_protection_gig_worker_exclusion_score: 25.0, platform_misclassification_labor_rights_gap_score: 26.0, risk_level: "modéré", primary_pattern: "social_protection_gig_worker_exclusion", estimated_gig_economy_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "GER-008", name: "OIT/Recommandation — R198 Relation Travail, Platerforme Work Directive & SDG 8.8 Droits Travailleurs", country: "Global", composite_score: 4.0, algorithmic_wage_theft_control_severity_score: 4.0, zero_hours_contract_precarity_scale_score: 4.0, social_protection_gig_worker_exclusion_score: 4.0, platform_misclassification_labor_rights_gap_score: 4.0, risk_level: "faible", primary_pattern: "algorithmic_wage_theft_control_severity", estimated_gig_economy_rights_index: 0.40, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/gig-economy-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
