import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[economic-domestic-abuse-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Economic Domestic Abuse Engine Agent",
  domain: "economic_domestic_abuse",
  total_entities: 8,
  avg_composite: 61.63,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { financial_control_coercion_severity: 2, legal_economic_protection_absence: 2, asset_debt_exploitation_scale: 2, economic_recovery_support_gap: 2 },
  top_risk_entities: [
    "Afghanistan/Taliban — Interdiction Travail Femmes, Contrôle Total Finances & Zéro Recours Légal",
    "Arabie Saoudite/MENA — Tutelle Masculine, Compte Bloqué, Divorce Économique Impossible",
    "USA — 99% Survivantes DV Subissent Abus Économique, 72% Restent Pour Raisons Financières",
  ],
  critical_alerts: [
    "Afghanistan/Taliban: financial_control_coercion_severity",
    "Arabie Saoudite/MENA: legal_economic_protection_absence",
    "USA: asset_debt_exploitation_scale",
    "Afrique Sub-Sah.: economic_recovery_support_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_economic_domestic_abuse_index: 6.16,
  data_sources: [
    "nnedv_purple_purse_financial_abuse_domestic_violence_report",
    "un_women_cedaw_economic_rights_intimate_partner_violence_review",
    "world_bank_women_property_rights_financial_inclusion_global_study",
  ],
  entities: [
    { id: "EDA-001", name: "Afghanistan/Taliban — Interdiction Travail Femmes, Contrôle Total Finances & Zéro Recours Légal", country: "Asie du Sud", composite_score: 93.65, financial_control_coercion_severity_score: 95.0, legal_economic_protection_absence_score: 95.0, asset_debt_exploitation_scale_score: 92.0, economic_recovery_support_gap_score: 92.0, risk_level: "critique", primary_pattern: "financial_control_coercion_severity", estimated_economic_domestic_abuse_index: 9.37, last_updated: "2026-06-21" },
    { id: "EDA-002", name: "Arabie Saoudite/MENA — Tutelle Masculine, Compte Bloqué, Divorce Économique Impossible", country: "Moyen-Orient", composite_score: 89.7, financial_control_coercion_severity_score: 92.0, legal_economic_protection_absence_score: 90.0, asset_debt_exploitation_scale_score: 88.0, economic_recovery_support_gap_score: 88.0, risk_level: "critique", primary_pattern: "legal_economic_protection_absence", estimated_economic_domestic_abuse_index: 8.97, last_updated: "2026-06-21" },
    { id: "EDA-003", name: "USA — 99% Survivantes DV Subissent Abus Économique, 72% Restent Pour Raisons Financières", country: "Amérique du Nord", composite_score: 88.0, financial_control_coercion_severity_score: 88.0, legal_economic_protection_absence_score: 88.0, asset_debt_exploitation_scale_score: 88.0, economic_recovery_support_gap_score: 88.0, risk_level: "critique", primary_pattern: "asset_debt_exploitation_scale", estimated_economic_domestic_abuse_index: 8.8, last_updated: "2026-06-21" },
    { id: "EDA-004", name: "Afrique Sub-Sah. — Dot Piège Économique, Terres Au Nom Mari & Zéro Recours Légal", country: "Afrique", composite_score: 86.35, financial_control_coercion_severity_score: 85.0, legal_economic_protection_absence_score: 88.0, asset_debt_exploitation_scale_score: 85.0, economic_recovery_support_gap_score: 88.0, risk_level: "critique", primary_pattern: "economic_recovery_support_gap", estimated_economic_domestic_abuse_index: 8.64, last_updated: "2026-06-21" },
    { id: "EDA-005", name: "Inde — Dot Comme Levier de Contrôle, 70% Femmes Rurales Sans Compte Bancaire Personnel", country: "Asie du Sud", composite_score: 53.1, financial_control_coercion_severity_score: 52.0, legal_economic_protection_absence_score: 55.0, asset_debt_exploitation_scale_score: 55.0, economic_recovery_support_gap_score: 50.0, risk_level: "élevé", primary_pattern: "legal_economic_protection_absence", estimated_economic_domestic_abuse_index: 5.31, last_updated: "2026-06-21" },
    { id: "EDA-006", name: "Amérique Latine/Brésil — Machisme Économique, Dépendance Forcée & Zéro Allocation Séparation", country: "Amérique Latine", composite_score: 52.0, financial_control_coercion_severity_score: 50.0, legal_economic_protection_absence_score: 52.0, asset_debt_exploitation_scale_score: 52.0, economic_recovery_support_gap_score: 55.0, risk_level: "élevé", primary_pattern: "economic_recovery_support_gap", estimated_economic_domestic_abuse_index: 5.2, last_updated: "2026-06-21" },
    { id: "EDA-007", name: "Purple Purse/NNEDV — Indépendance Financière Survivantes, Programmes Refuges Économiques", country: "Global", composite_score: 25.85, financial_control_coercion_severity_score: 22.0, legal_economic_protection_absence_score: 28.0, asset_debt_exploitation_scale_score: 25.0, economic_recovery_support_gap_score: 30.0, risk_level: "modéré", primary_pattern: "financial_control_coercion_severity", estimated_economic_domestic_abuse_index: 2.59, last_updated: "2026-06-21" },
    { id: "EDA-008", name: "ONU Femmes/CEDAW — Art.16 Égalité Mariage/Divorce, SDG 5 Autonomisation Économique", country: "Global", composite_score: 4.4, financial_control_coercion_severity_score: 4.0, legal_economic_protection_absence_score: 5.0, asset_debt_exploitation_scale_score: 3.0, economic_recovery_support_gap_score: 6.0, risk_level: "faible", primary_pattern: "asset_debt_exploitation_scale", estimated_economic_domestic_abuse_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/economic-domestic-abuse-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
