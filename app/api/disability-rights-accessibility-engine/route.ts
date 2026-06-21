import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-accessibility-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Disability Rights Accessibility Engine Agent",
  domain: "disability_rights_accessibility",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    institutionalization_forced_treatment_severity: 3,
    physical_accessibility_exclusion_scale: 2,
    crpd_legal_capacity_guardianship_reform_deficit_gap: 2,
    disability_employment_discrimination: 1,
  },
  top_risk_entities: [
    "Chine — Institutions Psychiatriques Dissidents, Xiebi Internement Forcé, Eugénisme Stérilisation & Travail Forcé Handicapés",
    "Russie — Internats Psychiatriques Punição Politique, Psychiatrie Punitive Retour & Handicapés Institutionnalisés 150 000",
    "Afrique Sub-Saharienne — Sorcellerie Handicaps Infantiles, Exclusion Scolaire, Albinos Mutilations & Sans Protection CRPD",
  ],
  critical_alerts: [
    "Chine: institutionalization_forced_treatment_severity",
    "Russie: institutionalization_forced_treatment_severity",
    "Afrique Sub-Saharienne: physical_accessibility_exclusion_scale",
    "Inde: crpd_legal_capacity_guardianship_reform_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_disability_rights_accessibility_index: 6.14,
  data_sources: [
    "who_disability_world_report_global_data",
    "mental_disability_rights_international_monitoring",
    "crpd_committee_concluding_observations_database",
  ],
  entities: [
    {
      entity_id: "DRA-001",
      name: "Chine — Institutions Psychiatriques Dissidents, Xiebi Internement Forcé, Eugénisme Stérilisation & Travail Forcé Handicapés",
      country: "Chine",
      institutionalization_forced_treatment_severity_score: 95.0,
      physical_accessibility_exclusion_scale_score: 93.0,
      disability_employment_discrimination_score: 92.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "institutionalization_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-002",
      name: "Russie — Internats Psychiatriques Punição Politique, Psychiatrie Punitive Retour & Handicapés Institutionnalisés 150 000",
      country: "Russie",
      institutionalization_forced_treatment_severity_score: 92.0,
      physical_accessibility_exclusion_scale_score: 90.0,
      disability_employment_discrimination_score: 89.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "institutionalization_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-003",
      name: "Afrique Sub-Saharienne — Sorcellerie Handicaps Infantiles, Exclusion Scolaire, Albinos Mutilations & Sans Protection CRPD",
      country: "Afrique Sub-Saharienne",
      institutionalization_forced_treatment_severity_score: 89.0,
      physical_accessibility_exclusion_scale_score: 87.0,
      disability_employment_discrimination_score: 86.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "physical_accessibility_exclusion_scale",
      estimated_disability_rights_accessibility_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-004",
      name: "Inde — Personnes Handicapées Mental Internées, Loi Santé Mentale 2017 Inappliquée, Accessibilité Zéro Ruraux & Discrimination Castes",
      country: "Inde",
      institutionalization_forced_treatment_severity_score: 86.0,
      physical_accessibility_exclusion_scale_score: 84.0,
      disability_employment_discrimination_score: 83.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "crpd_legal_capacity_guardianship_reform_deficit_gap",
      estimated_disability_rights_accessibility_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-005",
      name: "USA/Europe — Olmstead Inappliqué Partiellement, Guardianship Abusif, ADA/ADAEU Lacunes & Électrochocs Sans Consentement",
      country: "USA/Europe",
      institutionalization_forced_treatment_severity_score: 57.0,
      physical_accessibility_exclusion_scale_score: 55.0,
      disability_employment_discrimination_score: 54.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "institutionalization_forced_treatment_severity",
      estimated_disability_rights_accessibility_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-006",
      name: "MENA — Stigmatisation Handicap Mental, Loi Tutelle Totale, Femmes Handicapées Double Discrimination & Accessibilité Absente",
      country: "MENA",
      institutionalization_forced_treatment_severity_score: 54.0,
      physical_accessibility_exclusion_scale_score: 52.0,
      disability_employment_discrimination_score: 51.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "disability_employment_discrimination",
      estimated_disability_rights_accessibility_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-007",
      name: "IDA/DPO Global — Disabled Peoples Organisations, CRPD Advocacy, Monitoring Mise en Œuvre & Standards Accessibilité",
      country: "Global",
      institutionalization_forced_treatment_severity_score: 27.0,
      physical_accessibility_exclusion_scale_score: 26.0,
      disability_employment_discrimination_score: 25.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "crpd_legal_capacity_guardianship_reform_deficit_gap",
      estimated_disability_rights_accessibility_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "DRA-008",
      name: "ONU/CRPD — Convention Droits Personnes Handicapées 2006, Comité CRPD & SDG 10.2 Inclusion",
      country: "Global",
      institutionalization_forced_treatment_severity_score: 5.0,
      physical_accessibility_exclusion_scale_score: 4.0,
      disability_employment_discrimination_score: 4.0,
      crpd_legal_capacity_guardianship_reform_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "physical_accessibility_exclusion_scale",
      estimated_disability_rights_accessibility_index: 0.43,
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
