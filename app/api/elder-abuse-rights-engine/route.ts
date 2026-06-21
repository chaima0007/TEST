import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[elder-abuse-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Elder Abuse Rights Engine Agent",
  domain: "elder_abuse_rights",
  total_entities: 8,
  avg_composite: 61.17,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { legal_protection_framework_gap: 3, financial_exploitation_scale: 1, institutional_abuse_prevalence: 2, autonomy_dignity_violation: 2 },
  top_risk_entities: [
    "Inde — Maltraitance 32% Personnes Âgées, Abandon Familial Systémique & Loi 2007 Non Appliquée",
    "Chine — Abandon Parents Âgés, Abus Financiers Répandus & Loi Filiale Controversée 2013",
    "USA — 5M Seniors Maltraités/An, COVID Maisons Retraite 40% Décès & FFAM Défaillance",
  ],
  critical_alerts: [
    "Inde: legal_protection_framework_gap",
    "Chine: financial_exploitation_scale",
    "USA: institutional_abuse_prevalence",
    "Mexique/LATAM: legal_protection_framework_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_elder_abuse_rights_index: 6.12,
  data_sources: [
    "who_global_report_ageism_elder_abuse_prevalence",
    "helpage_international_mipaa_review_elder_rights_monitoring",
    "un_open_ended_working_group_ageing_convention_proposal",
  ],
  entities: [
    { id: "EA-001", name: "Inde — Maltraitance 32% Personnes Âgées, Abandon Familial Systémique & Loi 2007 Non Appliquée", country: "Asie du Sud", composite_score: 93.25, institutional_abuse_prevalence_score: 95.0, financial_exploitation_scale_score: 92.0, legal_protection_framework_gap_score: 95.0, autonomy_dignity_violation_score: 90.0, risk_level: "critique", primary_pattern: "legal_protection_framework_gap", estimated_elder_abuse_rights_index: 9.33, last_updated: "2026-06-21" },
    { id: "EA-002", name: "Chine — Abandon Parents Âgés, Abus Financiers Répandus & Loi Filiale Controversée 2013", country: "Asie de l'Est", composite_score: 90.0, institutional_abuse_prevalence_score: 90.0, financial_exploitation_scale_score: 92.0, legal_protection_framework_gap_score: 88.0, autonomy_dignity_violation_score: 90.0, risk_level: "critique", primary_pattern: "financial_exploitation_scale", estimated_elder_abuse_rights_index: 9.0, last_updated: "2026-06-21" },
    { id: "EA-003", name: "USA — 5M Seniors Maltraités/An, COVID Maisons Retraite 40% Décès & FFAM Défaillance", country: "Amérique du Nord", composite_score: 87.75, institutional_abuse_prevalence_score: 88.0, financial_exploitation_scale_score: 90.0, legal_protection_framework_gap_score: 85.0, autonomy_dignity_violation_score: 88.0, risk_level: "critique", primary_pattern: "institutional_abuse_prevalence", estimated_elder_abuse_rights_index: 8.78, last_updated: "2026-06-21" },
    { id: "EA-004", name: "Mexique/LATAM — Isolation Institutionnelle, Droits Confisqués & Protection Sociale Absente", country: "Amérique Latine", composite_score: 85.0, institutional_abuse_prevalence_score: 85.0, financial_exploitation_scale_score: 82.0, legal_protection_framework_gap_score: 88.0, autonomy_dignity_violation_score: 85.0, risk_level: "critique", primary_pattern: "legal_protection_framework_gap", estimated_elder_abuse_rights_index: 8.5, last_updated: "2026-06-21" },
    { id: "EA-005", name: "France — Scandale EHPAD Orpea 2022, Maltraitance Systémique & Contrôles ARS Insuffisants", country: "Europe", composite_score: 53.65, institutional_abuse_prevalence_score: 55.0, financial_exploitation_scale_score: 52.0, legal_protection_framework_gap_score: 55.0, autonomy_dignity_violation_score: 52.0, risk_level: "élevé", primary_pattern: "institutional_abuse_prevalence", estimated_elder_abuse_rights_index: 5.37, last_updated: "2026-06-21" },
    { id: "EA-006", name: "Australie — Royal Commission 2021, 14 800 Incidents Signalés, Staffing Crisis & Réforme Partielle", country: "Océanie", composite_score: 49.5, institutional_abuse_prevalence_score: 50.0, financial_exploitation_scale_score: 48.0, legal_protection_framework_gap_score: 50.0, autonomy_dignity_violation_score: 50.0, risk_level: "élevé", primary_pattern: "autonomy_dignity_violation", estimated_elder_abuse_rights_index: 4.95, last_updated: "2026-06-21" },
    { id: "EA-007", name: "HelpAge International/OMS — MIPAA Madrid 2002, Rapport Global Âgisme & Standards Protection", country: "Global", composite_score: 25.85, institutional_abuse_prevalence_score: 22.0, financial_exploitation_scale_score: 28.0, legal_protection_framework_gap_score: 25.0, autonomy_dignity_violation_score: 30.0, risk_level: "modéré", primary_pattern: "autonomy_dignity_violation", estimated_elder_abuse_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "EA-008", name: "ONU/Madrid & CDPH — Convention Droits Personnes Âgées Proposée, Art.12 Capacité Autonomie", country: "Global", composite_score: 4.4, institutional_abuse_prevalence_score: 4.0, financial_exploitation_scale_score: 5.0, legal_protection_framework_gap_score: 3.0, autonomy_dignity_violation_score: 6.0, risk_level: "faible", primary_pattern: "legal_protection_framework_gap", estimated_elder_abuse_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elder-abuse-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
