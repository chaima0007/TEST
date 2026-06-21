import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[economic-austerity-social-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Economic Austerity Social Rights Engine Agent",
  domain: "economic_austerity_social_rights",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { healthcare_education_cuts_severity: 2, imf_structural_adjustment_conditionality: 3, pension_social_security_dismantlement_scale: 2, progressive_taxation_wealth_redistribution_deficit_gap: 1 },
  top_risk_entities: ["Grèce 2010-18 — Troïka Mémorandums, Salaires -40%, Hôpitaux Fermés 30%, Suicides +35% & Enfants Malnutrition Retour", "Argentine/FMI — Prêt 57Mds 2018, Coupes Sociales Macri, Pauvreté 40% & Milei Chainsaw 30% Budget État", "Zimbabwe/SAP — ESAP 1990s FMI Désastre, Santé Effondrée, Inflation 500% & Pauvreté 80% Post-Ajustement"],
  critical_alerts: ["Grèce 2010-18: healthcare_education_cuts_severity", "Argentine/FMI: imf_structural_adjustment_conditionality", "Zimbabwe/SAP: imf_structural_adjustment_conditionality", "UK/Austerité Cameron: pension_social_security_dismantlement_scale"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_economic_austerity_social_rights_index: 6.13,
  data_sources: ["cesr_economic_social_rights_austerity_report", "oxfam_inequality_austerity_report", "un_desc_structural_adjustment_report"],
  entities: [
    { id: "EAS-001", name: "Grèce 2010-18 — Troïka Mémorandums, Salaires -40%, Hôpitaux Fermés 30%, Suicides +35% & Enfants Malnutrition Retour", country: "Grèce", composite_score: 93.55, healthcare_education_cuts_severity_score: 95.0, pension_social_security_dismantlement_scale_score: 93.0, imf_structural_adjustment_conditionality_score: 92.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "healthcare_education_cuts_severity", estimated_economic_austerity_social_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "EAS-002", name: "Argentine/FMI — Prêt 57Mds 2018, Coupes Sociales Macri, Pauvreté 40% & Milei Chainsaw 30% Budget État", country: "Argentine", composite_score: 89.65, healthcare_education_cuts_severity_score: 91.0, pension_social_security_dismantlement_scale_score: 89.0, imf_structural_adjustment_conditionality_score: 90.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "imf_structural_adjustment_conditionality", estimated_economic_austerity_social_rights_index: 8.96, last_updated: "2026-06-21" },
    { id: "EAS-003", name: "Zimbabwe/SAP — ESAP 1990s FMI Désastre, Santé Effondrée, Inflation 500% & Pauvreté 80% Post-Ajustement", country: "Zimbabwe", composite_score: 86.45, healthcare_education_cuts_severity_score: 87.0, pension_social_security_dismantlement_scale_score: 86.0, imf_structural_adjustment_conditionality_score: 85.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "imf_structural_adjustment_conditionality", estimated_economic_austerity_social_rights_index: 8.64, last_updated: "2026-06-21" },
    { id: "EAS-004", name: "UK/Austerité Cameron — NHS Coupes 2010-19, Universal Credit Pauvreté, Banques Alimentaires +400% & Espérance Vie Stagnée Pauvres", country: "UK", composite_score: 82.6, healthcare_education_cuts_severity_score: 83.0, pension_social_security_dismantlement_scale_score: 82.0, imf_structural_adjustment_conditionality_score: 84.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 81.0, risk_level: "critique", primary_pattern: "pension_social_security_dismantlement_scale", estimated_economic_austerity_social_rights_index: 8.26, last_updated: "2026-06-21" },
    { id: "EAS-005", name: "Brésil/EC 95 — Amendement Constitutionnel Plafond Dépenses 20 Ans, SUS Santé Sous-Financé, Bolsonaro Privatisations & Familles Faim Retour", country: "Brésil", composite_score: 55.45, healthcare_education_cuts_severity_score: 56.0, pension_social_security_dismantlement_scale_score: 54.0, imf_structural_adjustment_conditionality_score: 55.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "healthcare_education_cuts_severity", estimated_economic_austerity_social_rights_index: 5.54, last_updated: "2026-06-21" },
    { id: "EAS-006", name: "France/Retraites — Réforme 64 Ans Contestée, CFDT/CGT Résistance, Décret Article 49.3 & Droits Sociaux Érodés", country: "France", composite_score: 52.45, healthcare_education_cuts_severity_score: 52.0, pension_social_security_dismantlement_scale_score: 51.0, imf_structural_adjustment_conditionality_score: 54.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "pension_social_security_dismantlement_scale", estimated_economic_austerity_social_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "EAS-007", name: "CESR/Oxfam — Center Economic Social Rights, Oxfam Inégalités Rapport, Alternative Budget & Mécanismes DESC", country: "Global", composite_score: 26.55, healthcare_education_cuts_severity_score: 27.0, pension_social_security_dismantlement_scale_score: 25.0, imf_structural_adjustment_conditionality_score: 28.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "progressive_taxation_wealth_redistribution_deficit_gap", estimated_economic_austerity_social_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "EAS-008", name: "ONU/PIDESC Art.2 — Réalisation Progressive DESC, Comité DESC Observation 2 Ressources Max, SDG 1 Pauvreté & Standards Minimum Core", country: "Global", composite_score: 4.0, healthcare_education_cuts_severity_score: 4.0, pension_social_security_dismantlement_scale_score: 4.0, imf_structural_adjustment_conditionality_score: 4.0, progressive_taxation_wealth_redistribution_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "imf_structural_adjustment_conditionality", estimated_economic_austerity_social_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/economic-austerity-social-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
