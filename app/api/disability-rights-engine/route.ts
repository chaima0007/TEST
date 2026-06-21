import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Disability Rights Engine Agent",
  domain: "disability_rights",
  total_entities: 8,
  avg_composite: 60.86,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { institutionalization_segregation_severity: 4, accessibility_barrier_discrimination_scale: 2, legal_capacity_guardianship_deprivation: 1, violence_abuse_disabled_persons_gap: 1 },
  top_risk_entities: [
    "India — 26M Personnes Handicapées Institutions, Loi RPWD 2016 Non Appliquée & Stérilisation Forcée Femmes",
    "China — Institutions Welfare Surpeuplées, Travail Forcé Ateliers & Restriction Droits Civils Handicapés",
    "Nigeria — 0,5% Budget Santé Handicap, Exclusion Éducation & Violence Communautaire Impunie",
  ],
  critical_alerts: [
    "India: institutionalization_segregation_severity",
    "China: institutionalization_segregation_severity",
    "Nigeria: accessibility_barrier_discrimination_scale",
    "Brésil: legal_capacity_guardianship_deprivation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_disability_rights_index: 6.09,
  data_sources: [
    "disability_rights_international_behind_closed_doors_report",
    "who_world_report_on_disability_2011",
    "crpd_committee_concluding_observations_2023",
  ],
  entities: [
    { id: "DR-001", name: "India — 26M Personnes Handicapées Institutions, Loi RPWD 2016 Non Appliquée & Stérilisation Forcée Femmes", country: "Inde", composite_score: 92.95, institutionalization_segregation_severity_score: 95.0, accessibility_barrier_discrimination_scale_score: 92.0, legal_capacity_guardianship_deprivation_score: 93.0, violence_abuse_disabled_persons_gap_score: 91.0, risk_level: "critique", primary_pattern: "institutionalization_segregation_severity", estimated_disability_rights_index: 9.3, last_updated: "2026-06-21" },
    { id: "DR-002", name: "China — Institutions Welfare Surpeuplées, Travail Forcé Ateliers & Restriction Droits Civils Handicapés", country: "Chine", composite_score: 89.95, institutionalization_segregation_severity_score: 92.0, accessibility_barrier_discrimination_scale_score: 89.0, legal_capacity_guardianship_deprivation_score: 90.0, violence_abuse_disabled_persons_gap_score: 88.0, risk_level: "critique", primary_pattern: "institutionalization_segregation_severity", estimated_disability_rights_index: 9.0, last_updated: "2026-06-21" },
    { id: "DR-003", name: "Nigeria — 0,5% Budget Santé Handicap, Exclusion Éducation & Violence Communautaire Impunie", country: "Nigeria", composite_score: 86.7, institutionalization_segregation_severity_score: 89.0, accessibility_barrier_discrimination_scale_score: 86.0, legal_capacity_guardianship_deprivation_score: 86.0, violence_abuse_disabled_persons_gap_score: 85.0, risk_level: "critique", primary_pattern: "accessibility_barrier_discrimination_scale", estimated_disability_rights_index: 8.67, last_updated: "2026-06-21" },
    { id: "DR-004", name: "Brésil — Internement Psychiatrique Abusif, Isolement Carcéral & Inégalités Accès Emploi", country: "Brésil", composite_score: 83.75, institutionalization_segregation_severity_score: 86.0, accessibility_barrier_discrimination_scale_score: 83.0, legal_capacity_guardianship_deprivation_score: 84.0, violence_abuse_disabled_persons_gap_score: 81.0, risk_level: "critique", primary_pattern: "legal_capacity_guardianship_deprivation", estimated_disability_rights_index: 8.38, last_updated: "2026-06-21" },
    { id: "DR-005", name: "Europe Est — Désinstitutionnalisation Lente, Tutelle Légale Abusive & Hôpitaux Psychiatriques Soviétiques", country: "Europe Est", composite_score: 52.75, institutionalization_segregation_severity_score: 55.0, accessibility_barrier_discrimination_scale_score: 52.0, legal_capacity_guardianship_deprivation_score: 53.0, violence_abuse_disabled_persons_gap_score: 50.0, risk_level: "élevé", primary_pattern: "institutionalization_segregation_severity", estimated_disability_rights_index: 5.28, last_updated: "2026-06-21" },
    { id: "DR-006", name: "Moyen-Orient — Exclusion Éducation Inclusive, Stigma Religieux & Zéro Accessibilité Urbaine", country: "Moyen-Orient", composite_score: 50.75, institutionalization_segregation_severity_score: 53.0, accessibility_barrier_discrimination_scale_score: 50.0, legal_capacity_guardianship_deprivation_score: 51.0, violence_abuse_disabled_persons_gap_score: 48.0, risk_level: "élevé", primary_pattern: "accessibility_barrier_discrimination_scale", estimated_disability_rights_index: 5.08, last_updated: "2026-06-21" },
    { id: "DR-007", name: "Disability Rights International/IDA — Plaidoyer Désinstitutionnalisation, CRPD & Standards ONU", country: "Global", composite_score: 25.85, institutionalization_segregation_severity_score: 27.0, accessibility_barrier_discrimination_scale_score: 25.0, legal_capacity_guardianship_deprivation_score: 26.0, violence_abuse_disabled_persons_gap_score: 25.0, risk_level: "modéré", primary_pattern: "institutionalization_segregation_severity", estimated_disability_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "DR-008", name: "ONU/CRPD — Convention Droits Personnes Handicapées, Comité CRPD & SDG 10.2 Inclusion", country: "Global", composite_score: 4.2, institutionalization_segregation_severity_score: 4.0, accessibility_barrier_discrimination_scale_score: 4.0, legal_capacity_guardianship_deprivation_score: 4.0, violence_abuse_disabled_persons_gap_score: 5.0, risk_level: "faible", primary_pattern: "violence_abuse_disabled_persons_gap", estimated_disability_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
