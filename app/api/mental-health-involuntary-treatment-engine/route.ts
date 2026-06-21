import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mental-health-involuntary-treatment-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Mental Health Involuntary Treatment Engine Agent",
  domain: "mental_health_involuntary_treatment",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    involuntary_psychiatric_hospitalization_severity: 2,
    electroconvulsive_chemical_restraint_scale: 2,
    mental_health_criminal_justice_diversion_failure: 2,
    community_mental_health_service_absence_deficit_gap: 2,
  },
  top_risk_entities: [
    "Russie/Belarus — Psychiatrie Punitive Dissidents, Serbsky Centre Abus, Internements Forcés Longue Durée & Médicaments Forcés",
    "Chine — Ankang Hôpitaux Psychiatrie Police, Falun Gong Internements, Activistes Psychiatrisés & Conditions Inhumaines",
    "USA — 250 000 Personnes Santé Mentale Incarcérées, Crisis Intervention Manque, Taser Deaths & Rikers Island",
  ],
  critical_alerts: [
    "Russie/Belarus: involuntary_psychiatric_hospitalization_severity",
    "Chine: electroconvulsive_chemical_restraint_scale",
    "USA: mental_health_criminal_justice_diversion_failure",
    "Inde/Asie Sud: community_mental_health_service_absence_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_mental_health_involuntary_treatment_index: 6.14,
  data_sources: [
    "who_mental_health_atlas_global_report",
    "mental_disability_rights_international_behind_closed_doors",
    "mdri_human_rights_psychiatric_institutions_report",
  ],
  entities: [
    {
      entity_id: "MHI-001",
      name: "Russie/Belarus — Psychiatrie Punitive Dissidents, Serbsky Centre Abus, Internements Forcés Longue Durée & Médicaments Forcés",
      country: "Russie/Belarus",
      involuntary_psychiatric_hospitalization_severity_score: 95.0,
      electroconvulsive_chemical_restraint_scale_score: 93.0,
      mental_health_criminal_justice_diversion_failure_score: 92.0,
      community_mental_health_service_absence_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "involuntary_psychiatric_hospitalization_severity",
      estimated_mental_health_involuntary_treatment_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-002",
      name: "Chine — Ankang Hôpitaux Psychiatrie Police, Falun Gong Internements, Activistes Psychiatrisés & Conditions Inhumaines",
      country: "Chine",
      involuntary_psychiatric_hospitalization_severity_score: 92.0,
      electroconvulsive_chemical_restraint_scale_score: 90.0,
      mental_health_criminal_justice_diversion_failure_score: 89.0,
      community_mental_health_service_absence_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "electroconvulsive_chemical_restraint_scale",
      estimated_mental_health_involuntary_treatment_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-003",
      name: "USA — 250 000 Personnes Santé Mentale Incarcérées, Crisis Intervention Manque, Taser Deaths & Rikers Island",
      country: "USA",
      involuntary_psychiatric_hospitalization_severity_score: 89.0,
      electroconvulsive_chemical_restraint_scale_score: 87.0,
      mental_health_criminal_justice_diversion_failure_score: 86.0,
      community_mental_health_service_absence_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "mental_health_criminal_justice_diversion_failure",
      estimated_mental_health_involuntary_treatment_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-004",
      name: "Inde/Asie Sud — Chaînes Patients Hôpitaux, Exorcisme Pratiques, Stigmatisation Suicide Criminalisé & Soins Zéro Rural",
      country: "Inde/Asie Sud",
      involuntary_psychiatric_hospitalization_severity_score: 86.0,
      electroconvulsive_chemical_restraint_scale_score: 84.0,
      mental_health_criminal_justice_diversion_failure_score: 83.0,
      community_mental_health_service_absence_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "community_mental_health_service_absence_deficit_gap",
      estimated_mental_health_involuntary_treatment_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-005",
      name: "Europe — Involuntary Placement 5-20% Hospitalisations, Électrochocs Sans Consentement, Longue Détention & CRPD Violations",
      country: "Europe",
      involuntary_psychiatric_hospitalization_severity_score: 57.0,
      electroconvulsive_chemical_restraint_scale_score: 55.0,
      mental_health_criminal_justice_diversion_failure_score: 54.0,
      community_mental_health_service_absence_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "electroconvulsive_chemical_restraint_scale",
      estimated_mental_health_involuntary_treatment_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-006",
      name: "Afrique/MENA — Budget Santé Mentale 0.5%, Guérisseurs Traditionnels Seuls, Médicaments Indisponibles & Lois Coloniales",
      country: "Afrique/MENA",
      involuntary_psychiatric_hospitalization_severity_score: 54.0,
      electroconvulsive_chemical_restraint_scale_score: 52.0,
      mental_health_criminal_justice_diversion_failure_score: 51.0,
      community_mental_health_service_absence_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "community_mental_health_service_absence_deficit_gap",
      estimated_mental_health_involuntary_treatment_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-007",
      name: "WHO/MHRN — Global Mental Health Action Plan, Réseau Recherche, CRPD Art.12 Capacité Juridique & Standards Soins",
      country: "Global",
      involuntary_psychiatric_hospitalization_severity_score: 27.0,
      electroconvulsive_chemical_restraint_scale_score: 26.0,
      mental_health_criminal_justice_diversion_failure_score: 25.0,
      community_mental_health_service_absence_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "involuntary_psychiatric_hospitalization_severity",
      estimated_mental_health_involuntary_treatment_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MHI-008",
      name: "ONU/CRPD Art.12-17 — Capacité Juridique, Intégrité Personne, Convention Torture & SDG 3.4 Santé Mentale",
      country: "Global",
      involuntary_psychiatric_hospitalization_severity_score: 5.0,
      electroconvulsive_chemical_restraint_scale_score: 4.0,
      mental_health_criminal_justice_diversion_failure_score: 4.0,
      community_mental_health_service_absence_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "mental_health_criminal_justice_diversion_failure",
      estimated_mental_health_involuntary_treatment_index: 0.43,
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
      `${process.env.SWARM_API_URL}/mental-health-involuntary-treatment-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
