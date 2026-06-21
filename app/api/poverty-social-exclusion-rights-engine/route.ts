import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[poverty-social-exclusion-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Poverty Social Exclusion Rights Engine Agent",
  domain: "poverty_social_exclusion_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    extreme_poverty_essential_services_denial_severity: 3,
    social_protection_floor_absence_scale: 2,
    poverty_trap_structural_inequality_redress_deficit_gap: 2,
    homelessness_vagrancy_criminalization: 1,
  },
  top_risk_entities: [
    "Madagascar/DRC — 77% Population Extrême Pauvreté <2$/Jour, Malnutrition Aiguë Enfants 50%, Santé Absente & Oxfam Alerte",
    "Sahel/Yémen — Famines Cycliques, 100M Déplacés Pauvres, Dettes FMI Austérité & Programmes Conditionnels Exclusifs",
    "Inde/Bangladesh — Bidonvilles 100M Urbains, Dalits Sans Accès Services, Travail Bonded & Filets Protection Troués",
  ],
  critical_alerts: [
    "Madagascar/DRC: extreme_poverty_essential_services_denial_severity",
    "Sahel/Yémen: social_protection_floor_absence_scale",
    "Inde/Bangladesh: poverty_trap_structural_inequality_redress_deficit_gap",
    "Amérique Centrale: poverty_trap_structural_inequality_redress_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_poverty_social_exclusion_rights_index: 6.14,
  data_sources: [
    "world_bank_poverty_global_database",
    "oxfam_inequality_kills_annual_report",
    "ilo_social_protection_floor_global_assessment",
  ],
  entities: [
    {
      id: "PSE-001",
      name: "Madagascar/DRC — 77% Population Extrême Pauvreté <2$/Jour, Malnutrition Aiguë Enfants 50%, Santé Absente & Oxfam Alerte",
      country: "Madagascar/DRC",
      extreme_poverty_essential_services_denial_severity_score: 95.0,
      social_protection_floor_absence_scale_score: 93.0,
      homelessness_vagrancy_criminalization_score: 92.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "extreme_poverty_essential_services_denial_severity",
      estimated_poverty_social_exclusion_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-002",
      name: "Sahel/Yémen — Famines Cycliques, 100M Déplacés Pauvres, Dettes FMI Austérité & Programmes Conditionnels Exclusifs",
      country: "Sahel/Yémen",
      extreme_poverty_essential_services_denial_severity_score: 92.0,
      social_protection_floor_absence_scale_score: 90.0,
      homelessness_vagrancy_criminalization_score: 89.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "social_protection_floor_absence_scale",
      estimated_poverty_social_exclusion_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-003",
      name: "Inde/Bangladesh — Bidonvilles 100M Urbains, Dalits Sans Accès Services, Travail Bonded & Filets Protection Troués",
      country: "Inde/Bangladesh",
      extreme_poverty_essential_services_denial_severity_score: 89.0,
      social_protection_floor_absence_scale_score: 87.0,
      homelessness_vagrancy_criminalization_score: 86.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "poverty_trap_structural_inequality_redress_deficit_gap",
      estimated_poverty_social_exclusion_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-004",
      name: "Amérique Centrale — Pauvreté Migration Forcée, Gangs Contrôle Quartiers Pauvres, Remesas Unique Revenu & Inégalités Record",
      country: "Amérique Centrale",
      extreme_poverty_essential_services_denial_severity_score: 86.0,
      social_protection_floor_absence_scale_score: 84.0,
      homelessness_vagrancy_criminalization_score: 83.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "poverty_trap_structural_inequality_redress_deficit_gap",
      estimated_poverty_social_exclusion_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-005",
      name: "USA/UK — Working Poor 40M USA, Foodbanks Record UK Austérité, Evictions COVID & Sans-Abri Criminalisés",
      country: "USA/UK",
      extreme_poverty_essential_services_denial_severity_score: 57.0,
      social_protection_floor_absence_scale_score: 55.0,
      homelessness_vagrancy_criminalization_score: 54.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "homelessness_vagrancy_criminalization",
      estimated_poverty_social_exclusion_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-006",
      name: "Europe/OCDE — NEET Youth 12%, Pièges Pauvreté Bénéficiaires, Logement Social Listes Attente & Fracture Numérique",
      country: "Europe/OCDE",
      extreme_poverty_essential_services_denial_severity_score: 54.0,
      social_protection_floor_absence_scale_score: 52.0,
      homelessness_vagrancy_criminalization_score: 51.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "social_protection_floor_absence_scale",
      estimated_poverty_social_exclusion_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-007",
      name: "Oxfam/BRAC — Rapports Inégalités Mondiales, Programmes Sortie Pauvreté, Advocacy Filets Sociaux & SDG Monitoring",
      country: "Global",
      extreme_poverty_essential_services_denial_severity_score: 27.0,
      social_protection_floor_absence_scale_score: 26.0,
      homelessness_vagrancy_criminalization_score: 25.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "extreme_poverty_essential_services_denial_severity",
      estimated_poverty_social_exclusion_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "PSE-008",
      name: "ONU/Art.11 DESC — Droit Niveau Vie Suffisant, Rapporteur Extrême Pauvreté & SDG 1 Pas de Pauvreté",
      country: "Global",
      extreme_poverty_essential_services_denial_severity_score: 5.0,
      social_protection_floor_absence_scale_score: 4.0,
      homelessness_vagrancy_criminalization_score: 4.0,
      poverty_trap_structural_inequality_redress_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "extreme_poverty_essential_services_denial_severity",
      estimated_poverty_social_exclusion_rights_index: 0.43,
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
      `${process.env.SWARM_API_URL}/poverty-social-exclusion-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
