import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mental-health-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Mental Health Rights Engine Agent",
  domain: "mental_health_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_institutionalization: 2, treatment_access_denial: 2, legal_capacity_deprivation: 2, stigma_discrimination_barrier: 2 },
  top_risk_entities: [
    "Russie — Psychiatrie Punitive Post-Soviétique, Internements Forcés Opposants & CRPD Non Ratifié",
    "Inde — 7M Institutionnalisés, Dargahs Chaînes, Loi 2017 Non Appliquée & CRPD Violations",
    "Ghana/Nigeria — Maisons Prière Patients Enchaînés, 10K+ Captifs & Lois Coloniales",
  ],
  critical_alerts: [
    "Russie: forced_institutionalization",
    "Inde: treatment_access_denial",
    "Ghana/Nigeria: treatment_access_denial",
    "USA: legal_capacity_deprivation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_mental_health_rights_index: 6.14,
  data_sources: [
    "who_mental_health_atlas_global_psychiatry_resources",
    "hrw_disability_rights_mental_health_institutionalization_report",
    "crpd_committee_general_comment_1_legal_capacity_article12",
  ],
  entities: [
    { entity_id: "MH-001", name: "Russie — Psychiatrie Punitive Post-Soviétique, Internements Forcés Opposants & CRPD Non Ratifié", country: "Europe de l'Est", composite_score: 93.25, forced_institutionalization_score: 95.0, treatment_access_denial_score: 92.0, legal_capacity_deprivation_score: 95.0, stigma_discrimination_barrier_score: 90.0, risk_level: "critique", primary_pattern: "forced_institutionalization", estimated_mental_health_rights_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "MH-002", name: "Inde — 7M Institutionnalisés, Dargahs Chaînes, Loi 2017 Non Appliquée & CRPD Violations", country: "Asie du Sud", composite_score: 90.4, forced_institutionalization_score: 90.0, treatment_access_denial_score: 92.0, legal_capacity_deprivation_score: 88.0, stigma_discrimination_barrier_score: 92.0, risk_level: "critique", primary_pattern: "treatment_access_denial", estimated_mental_health_rights_index: 9.04, last_updated: "2026-06-21" },
    { entity_id: "MH-003", name: "Ghana/Nigeria — Maisons Prière Patients Enchaînés, 10K+ Captifs & Lois Coloniales", country: "Afrique de l'Ouest", composite_score: 88.15, forced_institutionalization_score: 88.0, treatment_access_denial_score: 90.0, legal_capacity_deprivation_score: 85.0, stigma_discrimination_barrier_score: 90.0, risk_level: "critique", primary_pattern: "treatment_access_denial", estimated_mental_health_rights_index: 8.82, last_updated: "2026-06-21" },
    { entity_id: "MH-004", name: "USA — 180K Institutionnalisés, Olmstead Non Appliqué, Prisons Remplacent Asiles", country: "Amérique du Nord", composite_score: 85.15, forced_institutionalization_score: 85.0, treatment_access_denial_score: 85.0, legal_capacity_deprivation_score: 88.0, stigma_discrimination_barrier_score: 82.0, risk_level: "critique", primary_pattern: "legal_capacity_deprivation", estimated_mental_health_rights_index: 8.52, last_updated: "2026-06-21" },
    { entity_id: "MH-005", name: "UE/Malte & Hongrie — Tutelle Systémique, Capacité Juridique Restreinte & CRPD Art.12", country: "Europe", composite_score: 54.0, forced_institutionalization_score: 55.0, treatment_access_denial_score: 52.0, legal_capacity_deprivation_score: 58.0, stigma_discrimination_barrier_score: 50.0, risk_level: "élevé", primary_pattern: "legal_capacity_deprivation", estimated_mental_health_rights_index: 5.4, last_updated: "2026-06-21" },
    { entity_id: "MH-006", name: "Japon — Hospitalisations Involontaires 300+ Jours Moy., Isolement Systémique & CRPD", country: "Asie de l'Est", composite_score: 49.7, forced_institutionalization_score: 52.0, treatment_access_denial_score: 48.0, legal_capacity_deprivation_score: 50.0, stigma_discrimination_barrier_score: 48.0, risk_level: "élevé", primary_pattern: "forced_institutionalization", estimated_mental_health_rights_index: 4.97, last_updated: "2026-06-21" },
    { entity_id: "MH-007", name: "OMS/IASC — MHPSS Standards, Lignes Directrices Désinstitutionnalisation & Monitoring", country: "Global", composite_score: 25.85, forced_institutionalization_score: 22.0, treatment_access_denial_score: 28.0, legal_capacity_deprivation_score: 25.0, stigma_discrimination_barrier_score: 30.0, risk_level: "modéré", primary_pattern: "stigma_discrimination_barrier", estimated_mental_health_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "MH-008", name: "ONU/CRPD — Art.12 Capacité Juridique Égale, Art.14 Liberté & Rapporteur Spécial Handicap", country: "Global", composite_score: 4.4, forced_institutionalization_score: 4.0, treatment_access_denial_score: 5.0, legal_capacity_deprivation_score: 3.0, stigma_discrimination_barrier_score: 6.0, risk_level: "faible", primary_pattern: "stigma_discrimination_barrier", estimated_mental_health_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mental-health-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
