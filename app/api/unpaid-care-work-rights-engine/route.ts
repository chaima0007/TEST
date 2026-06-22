import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[unpaid-care-work-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Unpaid Care Work Rights Engine Agent",
  domain: "unpaid_care_work_rights",
  total_entities: 8,
  avg_composite: 61.5,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { domestic_care_burden_gender_gap: 3, economic_recognition_unpaid_work_absence: 2, childcare_eldercare_infrastructure_gap: 2, pension_social_protection_care_exclusion: 1 },
  top_risk_entities: [
    "Inde — Femmes 5h/Jour Travail Care Non Rémunéré, Zéro Reconnaissance Légale & Retraite Nulle",
    "Afrique Sub-Saharienne — 6h Care Quotidien Non Comptabilisé, PIB Shadow Economy 40% & Exclusion Sociale",
    "Moyen-Orient — Travail Domestique Féminin Obligatoire, Zéro Politique Parentalité & Retraite Conditionnelle",
  ],
  critical_alerts: [
    "Inde: domestic_care_burden_gender_gap",
    "Afrique Sub-Saharienne: economic_recognition_unpaid_work_absence",
    "Moyen-Orient: childcare_eldercare_infrastructure_gap",
    "Asie du Sud-Est: domestic_care_burden_gender_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_unpaid_care_work_rights_index: 6.15,
  data_sources: [
    "oxfam_time_to_care_unpaid_work_gender_global_report",
    "ilo_global_estimates_unpaid_care_work_wcms_report",
    "un_women_care_economy_invest_now_policy_brief",
  ],
  entities: [
    { id: "UCW-001", name: "Inde — Femmes 5h/Jour Travail Care Non Rémunéré, Zéro Reconnaissance Légale & Retraite Nulle", country: "Inde", composite_score: 92.55, domestic_care_burden_gender_gap_score: 96.0, economic_recognition_unpaid_work_absence_score: 92.0, childcare_eldercare_infrastructure_gap_score: 91.0, pension_social_protection_care_exclusion_score: 90.0, risk_level: "critique", primary_pattern: "domestic_care_burden_gender_gap", estimated_unpaid_care_work_rights_index: 9.26, last_updated: "2026-06-21" },
    { id: "UCW-002", name: "Afrique Sub-Saharienne — 6h Care Quotidien Non Comptabilisé, PIB Shadow Economy 40% & Exclusion Sociale", country: "Afrique Sub-Saharienne", composite_score: 89.85, domestic_care_burden_gender_gap_score: 93.0, economic_recognition_unpaid_work_absence_score: 89.0, childcare_eldercare_infrastructure_gap_score: 90.0, pension_social_protection_care_exclusion_score: 86.0, risk_level: "critique", primary_pattern: "economic_recognition_unpaid_work_absence", estimated_unpaid_care_work_rights_index: 8.99, last_updated: "2026-06-21" },
    { id: "UCW-003", name: "Moyen-Orient — Travail Domestique Féminin Obligatoire, Zéro Politique Parentalité & Retraite Conditionnelle", country: "Moyen-Orient", composite_score: 87.85, domestic_care_burden_gender_gap_score: 91.0, economic_recognition_unpaid_work_absence_score: 87.0, childcare_eldercare_infrastructure_gap_score: 88.0, pension_social_protection_care_exclusion_score: 84.0, risk_level: "critique", primary_pattern: "childcare_eldercare_infrastructure_gap", estimated_unpaid_care_work_rights_index: 8.79, last_updated: "2026-06-21" },
    { id: "UCW-004", name: "Asie du Sud-Est — Gap Care Genré 4:1, Infantilisation Travail Domestique & Pensions Familles Monoparentales", country: "Asie du Sud-Est", composite_score: 85.85, domestic_care_burden_gender_gap_score: 89.0, economic_recognition_unpaid_work_absence_score: 85.0, childcare_eldercare_infrastructure_gap_score: 86.0, pension_social_protection_care_exclusion_score: 82.0, risk_level: "critique", primary_pattern: "domestic_care_burden_gender_gap", estimated_unpaid_care_work_rights_index: 8.59, last_updated: "2026-06-21" },
    { id: "UCW-005", name: "USA — 32h/Semaine Care Non Rémunéré Femmes, Congé Parental Insuffisant & Retraite Care Gap", country: "États-Unis", composite_score: 53.15, domestic_care_burden_gender_gap_score: 55.0, economic_recognition_unpaid_work_absence_score: 53.0, childcare_eldercare_infrastructure_gap_score: 52.0, pension_social_protection_care_exclusion_score: 52.0, risk_level: "élevé", primary_pattern: "pension_social_protection_care_exclusion", estimated_unpaid_care_work_rights_index: 5.32, last_updated: "2026-06-21" },
    { id: "UCW-006", name: "France/UE — Inégalité Care Résiduelle, Réforme Retraites Pénalise Carrières Interrompues & Crèches Insuffisantes", country: "France/UE", composite_score: 51.95, domestic_care_burden_gender_gap_score: 54.0, economic_recognition_unpaid_work_absence_score: 51.0, childcare_eldercare_infrastructure_gap_score: 52.0, pension_social_protection_care_exclusion_score: 50.0, risk_level: "élevé", primary_pattern: "childcare_eldercare_infrastructure_gap", estimated_unpaid_care_work_rights_index: 5.2, last_updated: "2026-06-21" },
    { id: "UCW-007", name: "ILO/Oxfam — Care Economy 10,8 Trilliards $/An, Politique Redistribution Travail & Plaidoyer Rémunération", country: "Global", composite_score: 26.35, domestic_care_burden_gender_gap_score: 22.0, economic_recognition_unpaid_work_absence_score: 28.0, childcare_eldercare_infrastructure_gap_score: 27.0, pension_social_protection_care_exclusion_score: 30.0, risk_level: "modéré", primary_pattern: "economic_recognition_unpaid_work_absence", estimated_unpaid_care_work_rights_index: 2.64, last_updated: "2026-06-21" },
    { id: "UCW-008", name: "ONU/CEDAW — Convention Discrimination Femmes, Résolution Care Economy & Recommandation Politique Sociale", country: "Global", composite_score: 4.45, domestic_care_burden_gender_gap_score: 4.0, economic_recognition_unpaid_work_absence_score: 5.0, childcare_eldercare_infrastructure_gap_score: 4.0, pension_social_protection_care_exclusion_score: 5.0, risk_level: "faible", primary_pattern: "domestic_care_burden_gender_gap", estimated_unpaid_care_work_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/unpaid-care-work-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
