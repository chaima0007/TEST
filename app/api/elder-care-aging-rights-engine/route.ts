import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[elder-care-aging-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Elder Care Aging Rights Engine Agent",
  domain: "elder_care_aging_rights",
  total_entities: 8,
  avg_composite: 61.58,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    pension_social_protection_exclusion_scale: 3,
    elder_abuse_neglect_institutionalization_severity: 2,
    dementia_care_autonomy_rights_deficit_gap: 2,
    ageism_employment_healthcare_discrimination: 1,
  },
  top_risk_entities: [
    "Inde/Asie Sud — 3/4 Ainés Sans Pension, Familles Abandon Rural, Brus Vieillissants Apatrides & Maltraitance Invisible",
    "Afrique Sub-Saharienne — HIV/AIDS Orphelins Parents Ainés, Pensions Absentes 90%, Sorcellerie Âgées Accusées & Déplacement",
    "USA/Europe COVID — EHPAD COVID 40% Morts, Directives Ne-Pas-Réanimer Âge, Isolement Forcé & Vaccination Retard Ainés",
  ],
  critical_alerts: [
    "Inde/Asie Sud: pension_social_protection_exclusion_scale",
    "Afrique Sub-Saharienne: pension_social_protection_exclusion_scale",
    "USA/Europe COVID: elder_abuse_neglect_institutionalization_severity",
    "Chine/Japon: dementia_care_autonomy_rights_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_elder_care_aging_rights_index: 6.16,
  data_sources: [
    "who_global_status_report_elder_abuse",
    "helpage_international_aging_rights_index",
    "ilo_pension_social_protection_elderly_coverage",
  ],
  entities: [
    {
      id: "ECA-001",
      name: "Inde/Asie Sud — 3/4 Ainés Sans Pension, Familles Abandon Rural, Brus Vieillissants Apatrides & Maltraitance Invisible",
      country: "Inde/Asie Sud",
      elder_abuse_neglect_institutionalization_severity_score: 95.0,
      pension_social_protection_exclusion_scale_score: 93.0,
      ageism_employment_healthcare_discrimination_score: 93.0,
      dementia_care_autonomy_rights_deficit_gap_score: 91.0,
      composite_score: 93.2,
      risk_level: "critique",
      primary_pattern: "pension_social_protection_exclusion_scale",
      estimated_elder_care_aging_rights_index: 9.32,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-002",
      name: "Afrique Sub-Saharienne — HIV/AIDS Orphelins Parents Ainés, Pensions Absentes 90%, Sorcellerie Âgées Accusées & Déplacement",
      country: "Afrique Sub-Saharienne",
      elder_abuse_neglect_institutionalization_severity_score: 92.0,
      pension_social_protection_exclusion_scale_score: 90.0,
      ageism_employment_healthcare_discrimination_score: 90.0,
      dementia_care_autonomy_rights_deficit_gap_score: 88.0,
      composite_score: 90.2,
      risk_level: "critique",
      primary_pattern: "pension_social_protection_exclusion_scale",
      estimated_elder_care_aging_rights_index: 9.02,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-003",
      name: "USA/Europe COVID — EHPAD COVID 40% Morts, Directives Ne-Pas-Réanimer Âge, Isolement Forcé & Vaccination Retard Ainés",
      country: "USA/Europe",
      elder_abuse_neglect_institutionalization_severity_score: 89.0,
      pension_social_protection_exclusion_scale_score: 87.0,
      ageism_employment_healthcare_discrimination_score: 87.0,
      dementia_care_autonomy_rights_deficit_gap_score: 85.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "elder_abuse_neglect_institutionalization_severity",
      estimated_elder_care_aging_rights_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-004",
      name: "Chine/Japon — Vieillissement Démographique Crise, Traités Confucéens vs Institutions, Kodawari Abandon Urbain & Maltraitance EHPAD",
      country: "Chine/Japon",
      elder_abuse_neglect_institutionalization_severity_score: 86.0,
      pension_social_protection_exclusion_scale_score: 84.0,
      ageism_employment_healthcare_discrimination_score: 84.0,
      dementia_care_autonomy_rights_deficit_gap_score: 82.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "dementia_care_autonomy_rights_deficit_gap",
      estimated_elder_care_aging_rights_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-005",
      name: "France/UK — EHPAD Orpea Scandale Maltraitance, Personal Budgets Coupés, Restraint Chimique & Capacité Juridique Tutelle",
      country: "France/UK",
      elder_abuse_neglect_institutionalization_severity_score: 57.0,
      pension_social_protection_exclusion_scale_score: 55.0,
      ageism_employment_healthcare_discrimination_score: 55.0,
      dementia_care_autonomy_rights_deficit_gap_score: 53.0,
      composite_score: 55.2,
      risk_level: "élevé",
      primary_pattern: "elder_abuse_neglect_institutionalization_severity",
      estimated_elder_care_aging_rights_index: 5.52,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-006",
      name: "Amérique Latine — Retraites Dollarisées Perdues, Violence Intra-Familiale Âgés, Systèmes Santé Sans Gériatrie & Abandon",
      country: "Amérique Latine",
      elder_abuse_neglect_institutionalization_severity_score: 54.0,
      pension_social_protection_exclusion_scale_score: 52.0,
      ageism_employment_healthcare_discrimination_score: 52.0,
      dementia_care_autonomy_rights_deficit_gap_score: 50.0,
      composite_score: 52.2,
      risk_level: "élevé",
      primary_pattern: "pension_social_protection_exclusion_scale",
      estimated_elder_care_aging_rights_index: 5.22,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-007",
      name: "HelpAge International/AARP — Advocacy Droits Personnes Âgées, Monitoring Maltraitance, Convention Proposée ONU & Standards",
      country: "Global",
      elder_abuse_neglect_institutionalization_severity_score: 27.0,
      pension_social_protection_exclusion_scale_score: 26.0,
      ageism_employment_healthcare_discrimination_score: 26.0,
      dementia_care_autonomy_rights_deficit_gap_score: 25.0,
      composite_score: 26.1,
      risk_level: "modéré",
      primary_pattern: "ageism_employment_healthcare_discrimination",
      estimated_elder_care_aging_rights_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      id: "ECA-008",
      name: "ONU/MIPAA — Plan International Madrid Vieillissement, Décennie Vieillissement Sain 2021-2030 & SDG 3 Santé",
      country: "Global",
      elder_abuse_neglect_institutionalization_severity_score: 5.0,
      pension_social_protection_exclusion_scale_score: 4.0,
      ageism_employment_healthcare_discrimination_score: 4.0,
      dementia_care_autonomy_rights_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "dementia_care_autonomy_rights_deficit_gap",
      estimated_elder_care_aging_rights_index: 0.43,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/elder-care-aging-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
