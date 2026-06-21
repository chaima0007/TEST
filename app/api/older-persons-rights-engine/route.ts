import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[older-persons-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Older Persons Rights Engine Agent",
  domain: "older_persons_rights",
  total_entities: 8,
  avg_composite: 60.94,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { elder_abuse_neglect_institution_severity: 4, age_discrimination_employment_exclusion_scale: 2, pension_social_protection_adequacy_gap: 2 },
  top_risk_entities: [
    "Inde — 104M Personnes Âgées, Violence Familiale 60%, Abandon Centres & Zéro Pension Universelle",
    "Afrique Sub-Saharienne — Accusations Sorcellerie Personnes Âgées, Expulsions Terres & Zéro Soins Long Terme",
    "Chine — 260M +60 Ans, Discrimination Emploi, Soins EHPAD Sous-Financés & Abandon Rural",
  ],
  critical_alerts: [
    "Inde: elder_abuse_neglect_institution_severity",
    "Afrique Sub-Saharienne: elder_abuse_neglect_institution_severity",
    "Chine: age_discrimination_employment_exclusion_scale",
    "Russie/Europe Est: pension_social_protection_adequacy_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_older_persons_rights_index: 6.09,
  data_sources: [
    "helpage_international_global_agewatch_index",
    "who_global_report_ageism_abuse_older_persons",
    "un_mipaa_madrid_international_plan_ageing_2002",
  ],
  entities: [
    { id: "OPR-001", name: "Inde — 104M Personnes Âgées, Violence Familiale 60%, Abandon Centres & Zéro Pension Universelle", country: "Inde", composite_score: 92.95, elder_abuse_neglect_institution_severity_score: 95.0, age_discrimination_employment_exclusion_scale_score: 93.0, pension_social_protection_adequacy_gap_score: 92.0, healthcare_long_term_care_access_barrier_score: 91.0, risk_level: "critique", primary_pattern: "elder_abuse_neglect_institution_severity", estimated_older_persons_rights_index: 9.30, last_updated: "2026-06-21" },
    { id: "OPR-002", name: "Afrique Sub-Saharienne — Accusations Sorcellerie Personnes Âgées, Expulsions Terres & Zéro Soins Long Terme", country: "Afrique Sub-Saharienne", composite_score: 89.75, elder_abuse_neglect_institution_severity_score: 92.0, age_discrimination_employment_exclusion_scale_score: 89.0, pension_social_protection_adequacy_gap_score: 90.0, healthcare_long_term_care_access_barrier_score: 87.0, risk_level: "critique", primary_pattern: "elder_abuse_neglect_institution_severity", estimated_older_persons_rights_index: 8.98, last_updated: "2026-06-21" },
    { id: "OPR-003", name: "Chine — 260M +60 Ans, Discrimination Emploi, Soins EHPAD Sous-Financés & Abandon Rural", country: "Chine", composite_score: 86.75, elder_abuse_neglect_institution_severity_score: 89.0, age_discrimination_employment_exclusion_scale_score: 87.0, pension_social_protection_adequacy_gap_score: 86.0, healthcare_long_term_care_access_barrier_score: 84.0, risk_level: "critique", primary_pattern: "age_discrimination_employment_exclusion_scale", estimated_older_persons_rights_index: 8.68, last_updated: "2026-06-21" },
    { id: "OPR-004", name: "Russie/Europe Est — Retraites Insuffisantes, Institutions Soviétiques, Violence Abus Non Signalés", country: "Russie/Europe Est", composite_score: 83.95, elder_abuse_neglect_institution_severity_score: 86.0, age_discrimination_employment_exclusion_scale_score: 84.0, pension_social_protection_adequacy_gap_score: 83.0, healthcare_long_term_care_access_barrier_score: 82.0, risk_level: "critique", primary_pattern: "pension_social_protection_adequacy_gap", estimated_older_persons_rights_index: 8.40, last_updated: "2026-06-21" },
    { id: "OPR-005", name: "USA — Nursing Homes Covid 130k Morts, Abus Financier Tuteurs & Age Discrimination Emploi", country: "USA", composite_score: 52.90, elder_abuse_neglect_institution_severity_score: 55.0, age_discrimination_employment_exclusion_scale_score: 53.0, pension_social_protection_adequacy_gap_score: 51.0, healthcare_long_term_care_access_barrier_score: 52.0, risk_level: "élevé", primary_pattern: "elder_abuse_neglect_institution_severity", estimated_older_persons_rights_index: 5.29, last_updated: "2026-06-21" },
    { id: "OPR-006", name: "Japon — Hyper-Vieillissement, Karoshi Retraités Travailleurs, Isolement & Soins Famille Épuisement", country: "Japon", composite_score: 50.90, elder_abuse_neglect_institution_severity_score: 53.0, age_discrimination_employment_exclusion_scale_score: 51.0, pension_social_protection_adequacy_gap_score: 49.0, healthcare_long_term_care_access_barrier_score: 50.0, risk_level: "élevé", primary_pattern: "age_discrimination_employment_exclusion_scale", estimated_older_persons_rights_index: 5.09, last_updated: "2026-06-21" },
    { id: "OPR-007", name: "HelpAge International/IFA — Droits Seniors, Plaidoyer Convention ONU & Standards Madrid Plan", country: "Global", composite_score: 26.05, elder_abuse_neglect_institution_severity_score: 27.0, age_discrimination_employment_exclusion_scale_score: 26.0, pension_social_protection_adequacy_gap_score: 25.0, healthcare_long_term_care_access_barrier_score: 26.0, risk_level: "modéré", primary_pattern: "elder_abuse_neglect_institution_severity", estimated_older_persons_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "OPR-008", name: "ONU/Plan Madrid 2002 — Plan International Vieillissement, MIPAA & SDG 3.8 Couverture Santé Universelle", country: "Global", composite_score: 4.25, elder_abuse_neglect_institution_severity_score: 4.0, age_discrimination_employment_exclusion_scale_score: 4.0, pension_social_protection_adequacy_gap_score: 5.0, healthcare_long_term_care_access_barrier_score: 4.0, risk_level: "faible", primary_pattern: "pension_social_protection_adequacy_gap", estimated_older_persons_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/older-persons-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
