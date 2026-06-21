import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-accessibility-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Disability Rights Accessibility Engine Agent",
  domain: "disability_rights_accessibility",
  total_entities: 8,
  avg_composite: 61.55,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    institutional_segregation_forced_treatment_severity: 3,
    crpd_legal_capacity_recognition_deficit_gap: 4,
    employment_education_exclusion_scale: 1,
  },
  top_risk_entities: [
    "Russie/Internats Psychiatriques — Handicapés Isolés Institutions, Traitement Forcé Soviétique & Tutelle Totale Abus",
    "Inde/Lépreux Colonies — Exclus Société Villages Séparés, Mendier Autorisé Légalement & Discrimination Systémique",
    "Chine/Handicapés Mentaux — Institutions Abus Documentés, Loi 2008 Non-Appliquée & Travail Forcé Ateliers",
  ],
  critical_alerts: [
    "Russie/Internats Psychiatriques: institutional_segregation_forced_treatment_severity",
    "Inde/Lépreux Colonies: institutional_segregation_forced_treatment_severity",
    "Chine/Handicapés Mentaux: crpd_legal_capacity_recognition_deficit_gap",
    "Brésil/Manicômios: institutional_segregation_forced_treatment_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_disability_rights_accessibility_index: 6.16,
  data_sources: [
    "un_crpd_committee_concluding_observations",
    "hrw_disability_rights_violations_documentation",
    "ida_international_disability_alliance_reports",
  ],
  entities: [
    {
      entity_id: "DRA-001",
      name: "Russie/Internats Psychiatriques — Handicapés Isolés Institutions, Traitement Forcé Soviétique & Tutelle Totale Abus",
      country: "Russie",
      institutional_segregation_forced_treatment_severity_score: 94.0,
      employment_education_exclusion_scale_score: 91.0,
      physical_infrastructure_accessibility_barrier_score: 90.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 93.0,
      composite_score: 92.05,
      risk_level: "critique",
      primary_pattern: "institutional_segregation_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 9.21,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-002",
      name: "Inde/Lépreux Colonies — Exclus Société Villages Séparés, Mendier Autorisé Légalement & Discrimination Systémique",
      country: "Inde",
      institutional_segregation_forced_treatment_severity_score: 91.0,
      employment_education_exclusion_scale_score: 89.0,
      physical_infrastructure_accessibility_barrier_score: 88.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 90.0,
      composite_score: 89.55,
      risk_level: "critique",
      primary_pattern: "institutional_segregation_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 8.96,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-003",
      name: "Chine/Handicapés Mentaux — Institutions Abus Documentés, Loi 2008 Non-Appliquée & Travail Forcé Ateliers",
      country: "Chine",
      institutional_segregation_forced_treatment_severity_score: 88.0,
      employment_education_exclusion_scale_score: 86.0,
      physical_infrastructure_accessibility_barrier_score: 85.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 87.0,
      composite_score: 86.55,
      risk_level: "critique",
      primary_pattern: "crpd_legal_capacity_recognition_deficit_gap",
      estimated_disability_rights_accessibility_index: 8.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-004",
      name: "Brésil/Manicômios — Réforme Psychiatrique Incomplète, 30 000 Internés Institutions & Violence Documentée HRW",
      country: "Brésil",
      institutional_segregation_forced_treatment_severity_score: 85.0,
      employment_education_exclusion_scale_score: 83.0,
      physical_infrastructure_accessibility_barrier_score: 82.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 84.0,
      composite_score: 83.55,
      risk_level: "critique",
      primary_pattern: "institutional_segregation_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 8.36,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-005",
      name: "USA/Institutions Psychiatriques — Olmstead Non-Appliqué Intégralement, ADA Gaps & Criminalisation Handicap Mental",
      country: "USA",
      institutional_segregation_forced_treatment_severity_score: 55.0,
      employment_education_exclusion_scale_score: 53.0,
      physical_infrastructure_accessibility_barrier_score: 52.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 58.0,
      composite_score: 54.35,
      risk_level: "élevé",
      primary_pattern: "crpd_legal_capacity_recognition_deficit_gap",
      estimated_disability_rights_accessibility_index: 5.44,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-006",
      name: "Afrique Sub-Saharienne — Handicap Exclusion Emploi 90%, Infrastructures Inaccessibles & Sorcellerie Stigma Handicap",
      country: "Afrique Sub-Saharienne",
      institutional_segregation_forced_treatment_severity_score: 52.0,
      employment_education_exclusion_scale_score: 58.0,
      physical_infrastructure_accessibility_barrier_score: 57.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 54.0,
      composite_score: 55.15,
      risk_level: "élevé",
      primary_pattern: "employment_education_exclusion_scale",
      estimated_disability_rights_accessibility_index: 5.52,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-007",
      name: "DPO/IDA Alliance Internationale — Handicapés Organisations, CRPD Monitoring & Inclusion Advocacy Global",
      country: "Global",
      institutional_segregation_forced_treatment_severity_score: 27.0,
      employment_education_exclusion_scale_score: 25.0,
      physical_infrastructure_accessibility_barrier_score: 26.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 28.0,
      composite_score: 26.45,
      risk_level: "modéré",
      primary_pattern: "crpd_legal_capacity_recognition_deficit_gap",
      estimated_disability_rights_accessibility_index: 2.65,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-008",
      name: "ONU/CRPD 2006 — Convention Droits Personnes Handicapées, Comité CRPD Examen États & Art.12 Capacité Juridique",
      country: "Global",
      institutional_segregation_forced_treatment_severity_score: 5.0,
      employment_education_exclusion_scale_score: 5.0,
      physical_infrastructure_accessibility_barrier_score: 4.0,
      crpd_legal_capacity_recognition_deficit_gap_score: 5.0,
      composite_score: 4.75,
      risk_level: "faible",
      primary_pattern: "crpd_legal_capacity_recognition_deficit_gap",
      estimated_disability_rights_accessibility_index: 0.48,
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
      `${process.env.SWARM_API_URL}/disability-rights-accessibility-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
