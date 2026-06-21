import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[menopause-workplace-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Menopause Workplace Rights Engine Agent",
  domain: "menopause_workplace_rights",
  total_entities: 8,
  avg_composite: 62.0,
  confidence_score: 0.82,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { age_gender_intersectional_discrimination_scale: 2, career_penalty_forced_exit_pattern: 2, medical_recognition_menopause_disability_gap: 2, workplace_symptom_accommodation_denial: 2 },
  top_risk_entities: [
    "Japon — Ménopause Tabou Total, Femmes Poussées Vers Retraite Anticipée & Karoshi Femmes",
    "Corée du Sud — 84% Femmes Cachent Symptômes Travail, Licenciement Déguisé & Silence Médical",
    "Inde — Ménopause = Honte, Femmes Rurales Sans Accès THS, Discrimination RH & ESIC Gap",
  ],
  critical_alerts: [
    "Japon: age_gender_intersectional_discrimination_scale",
    "Corée du Sud: career_penalty_forced_exit_pattern",
    "Inde: medical_recognition_menopause_disability_gap",
    "Afrique Sub-Sah.: workplace_symptom_accommodation_denial",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_menopause_workplace_rights_index: 6.2,
  data_sources: [
    "cipd_menopause_workplace_policy_uk_survey_2023",
    "british_menopause_society_employment_discrimination_health_report",
    "un_women_cedaw_reproductive_health_employment_rights_review",
  ],
  entities: [
    { id: "MWR-001", name: "Japon — Ménopause Tabou Total, Femmes Poussées Vers Retraite Anticipée & Karoshi Femmes", country: "Asie de l'Est", composite_score: 93.65, workplace_symptom_accommodation_denial_score: 95.0, age_gender_intersectional_discrimination_scale_score: 95.0, medical_recognition_menopause_disability_gap_score: 92.0, career_penalty_forced_exit_pattern_score: 92.0, risk_level: "critique", primary_pattern: "age_gender_intersectional_discrimination_scale", estimated_menopause_workplace_rights_index: 9.37, last_updated: "2026-06-21" },
    { id: "MWR-002", name: "Corée du Sud — 84% Femmes Cachent Symptômes Travail, Licenciement Déguisé & Silence Médical", country: "Asie de l'Est", composite_score: 90.1, workplace_symptom_accommodation_denial_score: 92.0, age_gender_intersectional_discrimination_scale_score: 90.0, medical_recognition_menopause_disability_gap_score: 88.0, career_penalty_forced_exit_pattern_score: 90.0, risk_level: "critique", primary_pattern: "career_penalty_forced_exit_pattern", estimated_menopause_workplace_rights_index: 9.01, last_updated: "2026-06-21" },
    { id: "MWR-003", name: "Inde — Ménopause = Honte, Femmes Rurales Sans Accès THS, Discrimination RH & ESIC Gap", country: "Asie du Sud", composite_score: 89.0, workplace_symptom_accommodation_denial_score: 90.0, age_gender_intersectional_discrimination_scale_score: 88.0, medical_recognition_menopause_disability_gap_score: 92.0, career_penalty_forced_exit_pattern_score: 85.0, risk_level: "critique", primary_pattern: "medical_recognition_menopause_disability_gap", estimated_menopause_workplace_rights_index: 8.9, last_updated: "2026-06-21" },
    { id: "MWR-004", name: "Afrique Sub-Sah. — Zéro THS Accessible, Ménopause Précoce Non Traitée & Exclusion Emploi", country: "Afrique", composite_score: 87.25, workplace_symptom_accommodation_denial_score: 88.0, age_gender_intersectional_discrimination_scale_score: 85.0, medical_recognition_menopause_disability_gap_score: 88.0, career_penalty_forced_exit_pattern_score: 88.0, risk_level: "critique", primary_pattern: "workplace_symptom_accommodation_denial", estimated_menopause_workplace_rights_index: 8.73, last_updated: "2026-06-21" },
    { id: "MWR-005", name: "USA — Pas de Protection Légale Ménopause, 1M Femmes/An Quittent Emploi & ADA Gap", country: "Amérique du Nord", composite_score: 53.65, workplace_symptom_accommodation_denial_score: 55.0, age_gender_intersectional_discrimination_scale_score: 52.0, medical_recognition_menopause_disability_gap_score: 55.0, career_penalty_forced_exit_pattern_score: 52.0, risk_level: "élevé", primary_pattern: "workplace_symptom_accommodation_denial", estimated_menopause_workplace_rights_index: 5.37, last_updated: "2026-06-21" },
    { id: "MWR-006", name: "France — Ménopause Invisible RH, 70% Femmes Sans Aménagement & Égalité Pro Lacunaire", country: "Europe", composite_score: 52.1, workplace_symptom_accommodation_denial_score: 52.0, age_gender_intersectional_discrimination_scale_score: 52.0, medical_recognition_menopause_disability_gap_score: 50.0, career_penalty_forced_exit_pattern_score: 55.0, risk_level: "élevé", primary_pattern: "career_penalty_forced_exit_pattern", estimated_menopause_workplace_rights_index: 5.21, last_updated: "2026-06-21" },
    { id: "MWR-007", name: "UK Menopause Taskforce/CIPD — Politiques Lieu Travail, Flexibilité & Loi Égalité 2010", country: "Europe", composite_score: 25.85, workplace_symptom_accommodation_denial_score: 22.0, age_gender_intersectional_discrimination_scale_score: 28.0, medical_recognition_menopause_disability_gap_score: 25.0, career_penalty_forced_exit_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "age_gender_intersectional_discrimination_scale", estimated_menopause_workplace_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "MWR-008", name: "OMS/ONU Femmes — Santé Reproductive Femmes 40-55, CEDAW Art.11 Emploi & SDG 5", country: "Global", composite_score: 4.4, workplace_symptom_accommodation_denial_score: 4.0, age_gender_intersectional_discrimination_scale_score: 5.0, medical_recognition_menopause_disability_gap_score: 3.0, career_penalty_forced_exit_pattern_score: 6.0, risk_level: "faible", primary_pattern: "medical_recognition_menopause_disability_gap", estimated_menopause_workplace_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/menopause-workplace-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
