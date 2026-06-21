import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[austerity-social-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Austerity Social Rights Engine Agent",
  domain: "austerity_social_rights",
  total_entities: 8,
  avg_composite: 61.22,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { essential_services_dismantlement: 2, social_protection_withdrawal: 2, healthcare_education_access_collapse: 1, democratic_conditionality_breach: 3 },
  top_risk_entities: [
    "Grèce — Mémorandum Troïka 2010-18, -30% Santé Publique, Pauvreté 36% & CESCR Violations",
    "UK — 12 Ans Austérité Cameron/Sunak, Banques Alimentaires ×10 & CRPD Violations Systémiques",
    "Argentine — FMI 57 Milliards 2018, Pauvreté 60%+ Milei 2024 & Démantèlement Social Accéléré",
  ],
  critical_alerts: [
    "Grèce: essential_services_dismantlement",
    "UK: social_protection_withdrawal",
    "Argentine: healthcare_education_access_collapse",
    "Zambie: democratic_conditionality_breach",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_austerity_social_rights_index: 6.12,
  data_sources: [
    "imf_conditionality_social_impact_assessment_database",
    "un_cescr_austerity_measures_retrogression_reports",
    "oxfam_austerity_poverty_inequality_global_report",
  ],
  entities: [
    { id: "AU-001", name: "Grèce — Mémorandum Troïka 2010-18, -30% Santé Publique, Pauvreté 36% & CESCR Violations", country: "Europe du Sud", composite_score: 93.25, essential_services_dismantlement_score: 95.0, healthcare_education_access_collapse_score: 95.0, social_protection_withdrawal_score: 92.0, democratic_conditionality_breach_score: 90.0, risk_level: "critique", primary_pattern: "essential_services_dismantlement", estimated_austerity_social_rights_index: 9.33, last_updated: "2026-06-21" },
    { id: "AU-002", name: "UK — 12 Ans Austérité Cameron/Sunak, Banques Alimentaires ×10 & CRPD Violations Systémiques", country: "Europe", composite_score: 89.6, essential_services_dismantlement_score: 90.0, healthcare_education_access_collapse_score: 88.0, social_protection_withdrawal_score: 92.0, democratic_conditionality_breach_score: 88.0, risk_level: "critique", primary_pattern: "social_protection_withdrawal", estimated_austerity_social_rights_index: 8.96, last_updated: "2026-06-21" },
    { id: "AU-003", name: "Argentine — FMI 57 Milliards 2018, Pauvreté 60%+ Milei 2024 & Démantèlement Social Accéléré", country: "Amérique Latine", composite_score: 88.5, essential_services_dismantlement_score: 88.0, healthcare_education_access_collapse_score: 90.0, social_protection_withdrawal_score: 88.0, democratic_conditionality_breach_score: 88.0, risk_level: "critique", primary_pattern: "healthcare_education_access_collapse", estimated_austerity_social_rights_index: 8.85, last_updated: "2026-06-21" },
    { id: "AU-004", name: "Zambie — Restructuration Dette FMI 2022, Services Publics Effondrés & Conditionnalités Inhumaines", country: "Afrique Australe", composite_score: 85.0, essential_services_dismantlement_score: 85.0, healthcare_education_access_collapse_score: 85.0, social_protection_withdrawal_score: 85.0, democratic_conditionality_breach_score: 85.0, risk_level: "critique", primary_pattern: "democratic_conditionality_breach", estimated_austerity_social_rights_index: 8.5, last_updated: "2026-06-21" },
    { id: "AU-005", name: "Brésil — PEC 55 Plafond Dépenses 20 Ans, -40% Investissement Social & Droits Gelés", country: "Amérique Latine", composite_score: 53.65, essential_services_dismantlement_score: 55.0, healthcare_education_access_collapse_score: 52.0, social_protection_withdrawal_score: 55.0, democratic_conditionality_breach_score: 52.0, risk_level: "élevé", primary_pattern: "social_protection_withdrawal", estimated_austerity_social_rights_index: 5.37, last_updated: "2026-06-21" },
    { id: "AU-006", name: "Portugal — Troïka 2011-14, Chômage 17%, Émigration 300K & Régression Droits Sociaux", country: "Europe du Sud", composite_score: 49.5, essential_services_dismantlement_score: 50.0, healthcare_education_access_collapse_score: 50.0, social_protection_withdrawal_score: 48.0, democratic_conditionality_breach_score: 50.0, risk_level: "élevé", primary_pattern: "essential_services_dismantlement", estimated_austerity_social_rights_index: 4.95, last_updated: "2026-06-21" },
    { id: "AU-007", name: "CETIM/ESCR-Net — Rapport Impact Austérité Droits Sociaux, Monitoring Conditionnalités FMI", country: "Global", composite_score: 25.85, essential_services_dismantlement_score: 22.0, healthcare_education_access_collapse_score: 28.0, social_protection_withdrawal_score: 25.0, democratic_conditionality_breach_score: 30.0, risk_level: "modéré", primary_pattern: "democratic_conditionality_breach", estimated_austerity_social_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "AU-008", name: "ONU/CESCR — Observation Générale 19 Sécurité Sociale, Obligation Non-Régression Droits PIDESC", country: "Global", composite_score: 4.4, essential_services_dismantlement_score: 4.0, healthcare_education_access_collapse_score: 5.0, social_protection_withdrawal_score: 3.0, democratic_conditionality_breach_score: 6.0, risk_level: "faible", primary_pattern: "democratic_conditionality_breach", estimated_austerity_social_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/austerity-social-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
