import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[statelessness-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Statelessness Rights Engine Agent",
  domain: "statelessness_rights",
  total_entities: 8,
  avg_composite: 61.64,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { statelessness_documentation_deprivation_severity: 2, birth_registration_absence_exclusion_scale: 3, nationality_acquisition_barrier: 2, social_service_access_stateless_gap: 1 },
  top_risk_entities: [
    "Myanmar/Rohingyas — 600 000 Apatrides, Loi Citoyenneté 1982 Exclusion Ethnique & Déni Documents Génération",
    "Côte d'Ivoire — 700 000 Apatrides Post-Guerre Civile, Enregistrement Naissances Rural Absent & Discrimination Dioula",
    "Thaïlande/Peuples Collines — 480 000 Highland Peoples Sans Nationalité, Restriction Mobilité & Exclusion Éducation",
  ],
  critical_alerts: [
    "Myanmar/Rohingyas: statelessness_documentation_deprivation_severity",
    "Côte d'Ivoire: birth_registration_absence_exclusion_scale",
    "Thaïlande/Peuples Collines: nationality_acquisition_barrier",
    "Koweït/Bidoun: social_service_access_stateless_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_statelessness_rights_index: 6.16,
  data_sources: [
    "unhcr_ibelong_campaign_statelessness_global_trends_report",
    "institute_statelessness_inclusion_global_statelessness_report",
    "human_rights_watch_statelessness_nationality_discrimination_review",
  ],
  entities: [
    { entity_id: "STR-001", name: "Myanmar/Rohingyas — 600 000 Apatrides, Loi Citoyenneté 1982 Exclusion Ethnique & Déni Documents Génération", country: "Myanmar", composite_score: 93.8, statelessness_documentation_deprivation_severity_score: 97.0, birth_registration_absence_exclusion_scale_score: 93.0, nationality_acquisition_barrier_score: 93.0, social_service_access_stateless_gap_score: 91.0, risk_level: "critique", primary_pattern: "statelessness_documentation_deprivation_severity", estimated_statelessness_rights_index: 9.38, last_updated: "2026-06-21" },
    { entity_id: "STR-002", name: "Côte d'Ivoire — 700 000 Apatrides Post-Guerre Civile, Enregistrement Naissances Rural Absent & Discrimination Dioula", country: "Côte d'Ivoire", composite_score: 89.75, statelessness_documentation_deprivation_severity_score: 93.0, birth_registration_absence_exclusion_scale_score: 89.0, nationality_acquisition_barrier_score: 88.0, social_service_access_stateless_gap_score: 88.0, risk_level: "critique", primary_pattern: "birth_registration_absence_exclusion_scale", estimated_statelessness_rights_index: 8.98, last_updated: "2026-06-21" },
    { entity_id: "STR-003", name: "Thaïlande/Peuples Collines — 480 000 Highland Peoples Sans Nationalité, Restriction Mobilité & Exclusion Éducation", country: "Thaïlande", composite_score: 88.0, statelessness_documentation_deprivation_severity_score: 91.0, birth_registration_absence_exclusion_scale_score: 87.0, nationality_acquisition_barrier_score: 87.0, social_service_access_stateless_gap_score: 86.0, risk_level: "critique", primary_pattern: "nationality_acquisition_barrier", estimated_statelessness_rights_index: 8.8, last_updated: "2026-06-21" },
    { entity_id: "STR-004", name: "Koweït/Bidoun — 100 000 Bidoun Apatrides, Accès Emploi Public Interdit & Passeports Voyageurs Refusés", country: "Koweït", composite_score: 86.45, statelessness_documentation_deprivation_severity_score: 89.0, birth_registration_absence_exclusion_scale_score: 85.0, nationality_acquisition_barrier_score: 86.0, social_service_access_stateless_gap_score: 85.0, risk_level: "critique", primary_pattern: "social_service_access_stateless_gap", estimated_statelessness_rights_index: 8.65, last_updated: "2026-06-21" },
    { entity_id: "STR-005", name: "Europe/Roms — 46 000 Roms Apatrides UE, Non-Enregistrement Naissances Itinérants & Discrimination Administrative", country: "Europe", composite_score: 53.25, statelessness_documentation_deprivation_severity_score: 56.0, birth_registration_absence_exclusion_scale_score: 52.0, nationality_acquisition_barrier_score: 53.0, social_service_access_stateless_gap_score: 51.0, risk_level: "élevé", primary_pattern: "birth_registration_absence_exclusion_scale", estimated_statelessness_rights_index: 5.33, last_updated: "2026-06-21" },
    { entity_id: "STR-006", name: "République Dominicaine — Arrêt TC 168-13 Déchéance Rétroactive, 133 000 Dominicains Haïtiens Apatrides", country: "République Dominicaine", composite_score: 51.55, statelessness_documentation_deprivation_severity_score: 54.0, birth_registration_absence_exclusion_scale_score: 51.0, nationality_acquisition_barrier_score: 52.0, social_service_access_stateless_gap_score: 48.0, risk_level: "élevé", primary_pattern: "nationality_acquisition_barrier", estimated_statelessness_rights_index: 5.16, last_updated: "2026-06-21" },
    { entity_id: "STR-007", name: "UNHCR/ISI — Campagne #IBelong Fin Apatridie 2024, Cartographie Globale & Plaidoyer Convention 1954", country: "Global", composite_score: 25.9, statelessness_documentation_deprivation_severity_score: 24.0, birth_registration_absence_exclusion_scale_score: 28.0, nationality_acquisition_barrier_score: 26.0, social_service_access_stateless_gap_score: 26.0, risk_level: "modéré", primary_pattern: "statelessness_documentation_deprivation_severity", estimated_statelessness_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "STR-008", name: "ONU/Convention 1954 — Statut Apatrides, Convention 1961 Réduction Apatridie & SDG 16.9 Identité Légale", country: "Global", composite_score: 4.45, statelessness_documentation_deprivation_severity_score: 4.0, birth_registration_absence_exclusion_scale_score: 5.0, nationality_acquisition_barrier_score: 4.0, social_service_access_stateless_gap_score: 5.0, risk_level: "faible", primary_pattern: "birth_registration_absence_exclusion_scale", estimated_statelessness_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
