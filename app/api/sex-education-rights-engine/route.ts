import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sex-education-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sex Education Rights Engine Agent",
  domain: "sex_education_rights",
  total_entities: 8,
  avg_composite: 61.14,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { abstinence_only_policy_harm_scale: 2, school_dropout_unwanted_pregnancy: 2, reproductive_health_information_denial: 2, lgbtq_exclusion_curriculum_severity: 2 },
  top_risk_entities: [
    "USA/États Conservateurs — Abstinence Only 25 États, Grossesses Ados 3x Plus & VIH Ados +60%",
    "Nigeria/Afrique Sub-Sah. — Mariage Précoce, Zéro Sex-Ed Scolaire, VIH/SIDA Ados Non Informés",
    "Philippines — Église Catholique Bloque Loi RH 2012, Zéro Sex-Ed & Avortement Illégal Toujours",
  ],
  critical_alerts: [
    "USA/États Conservateurs: abstinence_only_policy_harm_scale",
    "Nigeria/Afrique Sub-Sah.: school_dropout_unwanted_pregnancy",
    "Philippines: reproductive_health_information_denial",
    "Inde: school_dropout_unwanted_pregnancy",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sex_education_rights_index: 6.11,
  data_sources: [
    "siecus_state_of_sex_education_united_states_report",
    "unesco_international_technical_guidance_sexuality_education_cse",
    "ippf_comprehensive_sexuality_education_rights_global_review",
  ],
  entities: [
    { id: "SER-001", name: "USA/États Conservateurs — Abstinence Only 25 États, Grossesses Ados 3x Plus & VIH Ados +60%", country: "Amérique du Nord", composite_score: 90.0, abstinence_only_policy_harm_scale_score: 95.0, lgbtq_exclusion_curriculum_severity_score: 88.0, reproductive_health_information_denial_score: 90.0, school_dropout_unwanted_pregnancy_score: 85.0, risk_level: "critique", primary_pattern: "abstinence_only_policy_harm_scale", estimated_sex_education_rights_index: 9.0, last_updated: "2026-06-21" },
    { id: "SER-002", name: "Nigeria/Afrique Sub-Sah. — Mariage Précoce, Zéro Sex-Ed Scolaire, VIH/SIDA Ados Non Informés", country: "Afrique de l'Ouest", composite_score: 89.5, abstinence_only_policy_harm_scale_score: 85.0, lgbtq_exclusion_curriculum_severity_score: 88.0, reproductive_health_information_denial_score: 92.0, school_dropout_unwanted_pregnancy_score: 95.0, risk_level: "critique", primary_pattern: "school_dropout_unwanted_pregnancy", estimated_sex_education_rights_index: 8.95, last_updated: "2026-06-21" },
    { id: "SER-003", name: "Philippines — Église Catholique Bloque Loi RH 2012, Zéro Sex-Ed & Avortement Illégal Toujours", country: "Asie du Sud-Est", composite_score: 88.25, abstinence_only_policy_harm_scale_score: 88.0, lgbtq_exclusion_curriculum_severity_score: 85.0, reproductive_health_information_denial_score: 92.0, school_dropout_unwanted_pregnancy_score: 88.0, risk_level: "critique", primary_pattern: "reproductive_health_information_denial", estimated_sex_education_rights_index: 8.83, last_updated: "2026-06-21" },
    { id: "SER-004", name: "Inde — Tabou Culturel, Grossesses Ados Rurales, Manuels Scolaires Expurgés & Honte Institutionnelle", country: "Asie du Sud", composite_score: 86.75, abstinence_only_policy_harm_scale_score: 85.0, lgbtq_exclusion_curriculum_severity_score: 85.0, reproductive_health_information_denial_score: 88.0, school_dropout_unwanted_pregnancy_score: 90.0, risk_level: "critique", primary_pattern: "school_dropout_unwanted_pregnancy", estimated_sex_education_rights_index: 8.68, last_updated: "2026-06-21" },
    { id: "SER-005", name: "Pologne — Loi Anti-LGBT 2019, Sex-Ed Interdite Écoles, Zones Sans Idéologie Genre & CEDH", country: "Europe", composite_score: 52.5, abstinence_only_policy_harm_scale_score: 55.0, lgbtq_exclusion_curriculum_severity_score: 52.0, reproductive_health_information_denial_score: 52.0, school_dropout_unwanted_pregnancy_score: 50.0, risk_level: "élevé", primary_pattern: "lgbtq_exclusion_curriculum_severity", estimated_sex_education_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "SER-006", name: "Brésil — Programme Sex-Ed Supprimé Bolsonaro, Manuels Révisés Bible & Avortement Criminalisé", country: "Amérique Latine", composite_score: 51.85, abstinence_only_policy_harm_scale_score: 52.0, lgbtq_exclusion_curriculum_severity_score: 55.0, reproductive_health_information_denial_score: 50.0, school_dropout_unwanted_pregnancy_score: 50.0, risk_level: "élevé", primary_pattern: "abstinence_only_policy_harm_scale", estimated_sex_education_rights_index: 5.19, last_updated: "2026-06-21" },
    { id: "SER-007", name: "SIECUS/UNESCO — Standards CSE Globaux 2018, Éducation Sexuelle Complète & Plaidoyer Droits", country: "Global", composite_score: 25.85, abstinence_only_policy_harm_scale_score: 22.0, lgbtq_exclusion_curriculum_severity_score: 28.0, reproductive_health_information_denial_score: 25.0, school_dropout_unwanted_pregnancy_score: 30.0, risk_level: "modéré", primary_pattern: "lgbtq_exclusion_curriculum_severity", estimated_sex_education_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "SER-008", name: "ONU Femmes/IPPF — Droit Sex-Ed Complète, CEDAW Art.10, SDG 4 & Rapport CSE Global 2021", country: "Global", composite_score: 4.4, abstinence_only_policy_harm_scale_score: 4.0, lgbtq_exclusion_curriculum_severity_score: 5.0, reproductive_health_information_denial_score: 3.0, school_dropout_unwanted_pregnancy_score: 6.0, risk_level: "faible", primary_pattern: "reproductive_health_information_denial", estimated_sex_education_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sex-education-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
