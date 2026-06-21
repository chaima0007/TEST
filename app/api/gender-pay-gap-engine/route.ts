import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-pay-gap-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Gender Pay Gap Engine Agent",
  domain: "gender_pay_gap",
  total_entities: 8,
  avg_composite: 60.82,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { unpaid_care_work_burden: 2, occupational_segregation: 2, wage_discrimination_scale: 2, legal_enforcement_transparency_gap: 2 },
  top_risk_entities: [
    "Pakistan/Asie Sud — Écart 51%, Exclusion Marché Travail & Travail Domestique Non Rémunéré",
    "Afrique Sub-Saharienne — Secteur Informel Féminin 90%, Zéro Protection Sociale & Écarts Massifs",
    "Moyen-Orient — Participation Féminine 20%, Gardiennage Masculin & Discriminations Légales",
  ],
  critical_alerts: [
    "Pakistan/Asie Sud: unpaid_care_work_burden",
    "Afrique Sub-Saharienne: unpaid_care_work_burden",
    "Moyen-Orient: occupational_segregation",
    "Corée du Sud/Japon: occupational_segregation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_gender_pay_gap_index: 6.08,
  data_sources: [
    "ilo_global_wage_report_gender_pay_gap_analysis",
    "world_economic_forum_global_gender_gap_report",
    "eu_directive_pay_transparency_implementation_review_2024",
  ],
  entities: [
    { id: "GP-001", name: "Pakistan/Asie Sud — Écart 51%, Exclusion Marché Travail & Travail Domestique Non Rémunéré", country: "Asie du Sud", composite_score: 93.25, wage_discrimination_scale_score: 95.0, occupational_segregation_score: 92.0, unpaid_care_work_burden_score: 95.0, legal_enforcement_transparency_gap_score: 90.0, risk_level: "critique", primary_pattern: "unpaid_care_work_burden", estimated_gender_pay_gap_index: 9.33, last_updated: "2026-06-21" },
    { id: "GP-002", name: "Afrique Sub-Saharienne — Secteur Informel Féminin 90%, Zéro Protection Sociale & Écarts Massifs", country: "Afrique Sub-Saharienne", composite_score: 89.6, wage_discrimination_scale_score: 90.0, occupational_segregation_score: 88.0, unpaid_care_work_burden_score: 92.0, legal_enforcement_transparency_gap_score: 88.0, risk_level: "critique", primary_pattern: "unpaid_care_work_burden", estimated_gender_pay_gap_index: 8.96, last_updated: "2026-06-21" },
    { id: "GP-003", name: "Moyen-Orient — Participation Féminine 20%, Gardiennage Masculin & Discriminations Légales", country: "Moyen-Orient", composite_score: 87.75, wage_discrimination_scale_score: 88.0, occupational_segregation_score: 90.0, unpaid_care_work_burden_score: 85.0, legal_enforcement_transparency_gap_score: 88.0, risk_level: "critique", primary_pattern: "occupational_segregation", estimated_gender_pay_gap_index: 8.78, last_updated: "2026-06-21" },
    { id: "GP-004", name: "Corée du Sud/Japon — Écart 30-31%, Plafond Verre Corporate & Démission Mariage Culturelle", country: "Asie du Nord-Est", composite_score: 82.35, wage_discrimination_scale_score: 82.0, occupational_segregation_score: 85.0, unpaid_care_work_burden_score: 82.0, legal_enforcement_transparency_gap_score: 80.0, risk_level: "critique", primary_pattern: "occupational_segregation", estimated_gender_pay_gap_index: 8.24, last_updated: "2026-06-21" },
    { id: "GP-005", name: "USA — Écart 18%, Motherhood Penalty, Négociation Salariale Biaisée & Secteurs Ségrégués", country: "Amérique du Nord", composite_score: 53.85, wage_discrimination_scale_score: 52.0, occupational_segregation_score: 55.0, unpaid_care_work_burden_score: 58.0, legal_enforcement_transparency_gap_score: 50.0, risk_level: "élevé", primary_pattern: "wage_discrimination_scale", estimated_gender_pay_gap_index: 5.39, last_updated: "2026-06-21" },
    { id: "GP-006", name: "UE — Directive Transparence Salariale 2023, Écart Moyen 13% & Application Inégale États", country: "Europe", composite_score: 49.5, wage_discrimination_scale_score: 48.0, occupational_segregation_score: 52.0, unpaid_care_work_burden_score: 50.0, legal_enforcement_transparency_gap_score: 48.0, risk_level: "élevé", primary_pattern: "legal_enforcement_transparency_gap", estimated_gender_pay_gap_index: 4.95, last_updated: "2026-06-21" },
    { id: "GP-007", name: "Equal Pay International Coalition — OIT/ONU/ONU Femmes, Objectif 2030 & Plaidoyer Global", country: "Global", composite_score: 25.85, wage_discrimination_scale_score: 22.0, occupational_segregation_score: 25.0, unpaid_care_work_burden_score: 28.0, legal_enforcement_transparency_gap_score: 30.0, risk_level: "modéré", primary_pattern: "wage_discrimination_scale", estimated_gender_pay_gap_index: 2.59, last_updated: "2026-06-21" },
    { id: "GP-008", name: "ONU/CEDAW — Convention Élimination Discriminations Femmes, Comité & Protocole Facultatif", country: "Global", composite_score: 4.4, wage_discrimination_scale_score: 4.0, occupational_segregation_score: 5.0, unpaid_care_work_burden_score: 3.0, legal_enforcement_transparency_gap_score: 6.0, risk_level: "faible", primary_pattern: "legal_enforcement_transparency_gap", estimated_gender_pay_gap_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/gender-pay-gap-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
