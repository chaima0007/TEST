import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[period-poverty-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Period Poverty Rights Engine Agent",
  domain: "period_poverty_rights",
  total_entities: 8,
  avg_composite: 61.88,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { social_stigma_menstrual_taboo_pattern: 2, school_absenteeism_dropout_menstrual_scale: 2, menstrual_product_access_denial_severity: 2, sanitation_hygiene_infrastructure_gap: 2 },
  top_risk_entities: [
    "Népal/Inde Rurale — Chhaupadi (Exil Cabane), 70% Filles Sans Produits & Infections Fatales",
    "Afrique Sub-Sah. — 1/10 Filles Échange Sex Contre Produits, 50% Sans Toilettes École",
    "Bangladesh/Pakistan — 73% Filles Absentéisme, Chiffons Non Stériles & Zéro Programme Scolaire",
  ],
  critical_alerts: [
    "Népal/Inde Rurale: social_stigma_menstrual_taboo_pattern",
    "Afrique Sub-Sah.: school_absenteeism_dropout_menstrual_scale",
    "Bangladesh/Pakistan: menstrual_product_access_denial_severity",
    "Afrique de l'Est/Kenya: sanitation_hygiene_infrastructure_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_period_poverty_rights_index: 6.19,
  data_sources: [
    "plan_international_girls_report_menstrual_health_period_poverty_2023",
    "unfpa_menstrual_hygiene_management_sdg6_global_review",
    "wash_united_menstrual_health_school_absenteeism_global_study",
  ],
  entities: [
    { id: "PPR-001", name: "Népal/Inde Rurale — Chhaupadi (Exil Cabane), 70% Filles Sans Produits & Infections Fatales", country: "Asie du Sud", composite_score: 93.65, menstrual_product_access_denial_severity_score: 95.0, school_absenteeism_dropout_menstrual_scale_score: 92.0, social_stigma_menstrual_taboo_pattern_score: 95.0, sanitation_hygiene_infrastructure_gap_score: 92.0, risk_level: "critique", primary_pattern: "social_stigma_menstrual_taboo_pattern", estimated_period_poverty_rights_index: 9.37, last_updated: "2026-06-21" },
    { id: "PPR-002", name: "Afrique Sub-Sah. — 1/10 Filles Échange Sex Contre Produits, 50% Sans Toilettes École", country: "Afrique", composite_score: 91.75, menstrual_product_access_denial_severity_score: 92.0, school_absenteeism_dropout_menstrual_scale_score: 95.0, social_stigma_menstrual_taboo_pattern_score: 88.0, sanitation_hygiene_infrastructure_gap_score: 92.0, risk_level: "critique", primary_pattern: "school_absenteeism_dropout_menstrual_scale", estimated_period_poverty_rights_index: 9.18, last_updated: "2026-06-21" },
    { id: "PPR-003", name: "Bangladesh/Pakistan — 73% Filles Absentéisme, Chiffons Non Stériles & Zéro Programme Scolaire", country: "Asie du Sud", composite_score: 88.5, menstrual_product_access_denial_severity_score: 88.0, school_absenteeism_dropout_menstrual_scale_score: 90.0, social_stigma_menstrual_taboo_pattern_score: 88.0, sanitation_hygiene_infrastructure_gap_score: 88.0, risk_level: "critique", primary_pattern: "menstrual_product_access_denial_severity", estimated_period_poverty_rights_index: 8.85, last_updated: "2026-06-21" },
    { id: "PPR-004", name: "Afrique de l'Est/Kenya — Serviettes Luxe Inaccessibles, Tabou Rural & Filles Quittent École M3", country: "Afrique de l'Est", composite_score: 87.25, menstrual_product_access_denial_severity_score: 88.0, school_absenteeism_dropout_menstrual_scale_score: 88.0, social_stigma_menstrual_taboo_pattern_score: 85.0, sanitation_hygiene_infrastructure_gap_score: 88.0, risk_level: "critique", primary_pattern: "sanitation_hygiene_infrastructure_gap", estimated_period_poverty_rights_index: 8.73, last_updated: "2026-06-21" },
    { id: "PPR-005", name: "UK/USA — 1/10 Filles Sans Produits Menstruels Adéquats, Tax Tampon 2015 & Sans-Abri", country: "Europe/Amérique du Nord", composite_score: 52.1, menstrual_product_access_denial_severity_score: 52.0, school_absenteeism_dropout_menstrual_scale_score: 52.0, social_stigma_menstrual_taboo_pattern_score: 50.0, sanitation_hygiene_infrastructure_gap_score: 55.0, risk_level: "élevé", primary_pattern: "sanitation_hygiene_infrastructure_gap", estimated_period_poverty_rights_index: 5.21, last_updated: "2026-06-21" },
    { id: "PPR-006", name: "France — 4M Femmes En Précarité Menstruelle, Étudiantes 49% Concernées & Honte Scolaire", country: "Europe", composite_score: 51.5, menstrual_product_access_denial_severity_score: 52.0, school_absenteeism_dropout_menstrual_scale_score: 50.0, social_stigma_menstrual_taboo_pattern_score: 52.0, sanitation_hygiene_infrastructure_gap_score: 52.0, risk_level: "élevé", primary_pattern: "menstrual_product_access_denial_severity", estimated_period_poverty_rights_index: 5.15, last_updated: "2026-06-21" },
    { id: "PPR-007", name: "Plan International/Days for Girls — Kits Menstruels, Éducation MHM & Plaidoyer Taxe", country: "Global", composite_score: 25.85, menstrual_product_access_denial_severity_score: 22.0, school_absenteeism_dropout_menstrual_scale_score: 28.0, social_stigma_menstrual_taboo_pattern_score: 25.0, sanitation_hygiene_infrastructure_gap_score: 30.0, risk_level: "modéré", primary_pattern: "school_absenteeism_dropout_menstrual_scale", estimated_period_poverty_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "PPR-008", name: "ONU/UNFPA — MHM Menstrual Hygiene Management, SDG 6 Eau/Assainissement & CEDAW", country: "Global", composite_score: 4.4, menstrual_product_access_denial_severity_score: 4.0, school_absenteeism_dropout_menstrual_scale_score: 5.0, social_stigma_menstrual_taboo_pattern_score: 3.0, sanitation_hygiene_infrastructure_gap_score: 6.0, risk_level: "faible", primary_pattern: "social_stigma_menstrual_taboo_pattern", estimated_period_poverty_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/period-poverty-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
