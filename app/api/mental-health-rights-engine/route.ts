import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mental-health-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Mental Health Rights Engine Agent",
  domain: "mental_health_rights",
  total_entities: 8,
  avg_composite: 61.62,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_institutionalization_coercion_severity: 4, mental_health_service_access_gap: 3, psychiatric_treatment_without_consent_scale: 1 },
  top_risk_entities: [
    "Indonésie — 18 000 Personnes Enchaînées Pasung, Hôpitaux Surpeuplés & Zéro Psychiatres Ruraux",
    "Inde — 150M Besoins Santé Mentale, 0,3 Psychiatres/100k, Internement Forcé Famille & ECT Mineurs",
    "Afrique Sub-Saharienne — 1 Psychiatre/Million, Guérisseurs Traditionnels Seule Option & Chaînes Thérapeutiques",
  ],
  critical_alerts: [
    "Indonésie: forced_institutionalization_coercion_severity",
    "Inde: mental_health_service_access_gap",
    "Afrique Sub-Saharienne: mental_health_service_access_gap",
    "Russie: forced_institutionalization_coercion_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_mental_health_rights_index: 6.16,
  data_sources: [
    "who_mental_health_atlas_global_psychiatry_resources",
    "hrw_disability_rights_mental_health_institutionalization_report",
    "crpd_committee_general_comment_1_legal_capacity_article12",
  ],
  entities: [
    { id: "MHR-001", name: "Indonésie — 18 000 Personnes Enchaînées Pasung, Hôpitaux Surpeuplés & Zéro Psychiatres Ruraux", country: "Indonésie", composite_score: 93.95, forced_institutionalization_coercion_severity_score: 96.0, psychiatric_treatment_without_consent_scale_score: 94.0, mental_health_service_access_gap_score: 93.0, stigma_discrimination_mental_health_barrier_score: 92.0, risk_level: "critique", primary_pattern: "forced_institutionalization_coercion_severity", estimated_mental_health_rights_index: 9.40, last_updated: "2026-06-21" },
    { id: "MHR-002", name: "Inde — 150M Besoins Santé Mentale, 0,3 Psychiatres/100k, Internement Forcé Famille & ECT Mineurs", country: "Inde", composite_score: 90.95, forced_institutionalization_coercion_severity_score: 93.0, psychiatric_treatment_without_consent_scale_score: 91.0, mental_health_service_access_gap_score: 90.0, stigma_discrimination_mental_health_barrier_score: 89.0, risk_level: "critique", primary_pattern: "mental_health_service_access_gap", estimated_mental_health_rights_index: 9.10, last_updated: "2026-06-21" },
    { id: "MHR-003", name: "Afrique Sub-Saharienne — 1 Psychiatre/Million, Guérisseurs Traditionnels Seule Option & Chaînes Thérapeutiques", country: "Afrique Sub-Saharienne", composite_score: 87.95, forced_institutionalization_coercion_severity_score: 90.0, psychiatric_treatment_without_consent_scale_score: 87.0, mental_health_service_access_gap_score: 88.0, stigma_discrimination_mental_health_barrier_score: 86.0, risk_level: "critique", primary_pattern: "mental_health_service_access_gap", estimated_mental_health_rights_index: 8.80, last_updated: "2026-06-21" },
    { id: "MHR-004", name: "Russie — Hôpitaux Psychiatriques Punitifs Héritage Soviétique, Dissidents Internés & Zéro Consentement", country: "Russie", composite_score: 84.95, forced_institutionalization_coercion_severity_score: 87.0, psychiatric_treatment_without_consent_scale_score: 85.0, mental_health_service_access_gap_score: 84.0, stigma_discrimination_mental_health_barrier_score: 83.0, risk_level: "critique", primary_pattern: "forced_institutionalization_coercion_severity", estimated_mental_health_rights_index: 8.50, last_updated: "2026-06-21" },
    { id: "MHR-005", name: "USA — 500k Sans Abri Troubles Mentaux, Prisons Hôpitaux Psychiatrie, Isolement Cellulaire", country: "USA", composite_score: 53.95, forced_institutionalization_coercion_severity_score: 56.0, psychiatric_treatment_without_consent_scale_score: 54.0, mental_health_service_access_gap_score: 53.0, stigma_discrimination_mental_health_barrier_score: 52.0, risk_level: "élevé", primary_pattern: "forced_institutionalization_coercion_severity", estimated_mental_health_rights_index: 5.40, last_updated: "2026-06-21" },
    { id: "MHR-006", name: "Europe — ECT Sans Consentement Légal Plusieurs Pays, Contention Physique & Gaps Désinstitutionnalisation", country: "Europe", composite_score: 50.95, forced_institutionalization_coercion_severity_score: 53.0, psychiatric_treatment_without_consent_scale_score: 51.0, mental_health_service_access_gap_score: 50.0, stigma_discrimination_mental_health_barrier_score: 49.0, risk_level: "élevé", primary_pattern: "psychiatric_treatment_without_consent_scale", estimated_mental_health_rights_index: 5.10, last_updated: "2026-06-21" },
    { id: "MHR-007", name: "WNUSP/MIND — Réforme Psychiatrie, CRPD Article 12 & Mouvement Survivants Psychiatriques", country: "Global", composite_score: 26.05, forced_institutionalization_coercion_severity_score: 27.0, psychiatric_treatment_without_consent_scale_score: 26.0, mental_health_service_access_gap_score: 25.0, stigma_discrimination_mental_health_barrier_score: 26.0, risk_level: "modéré", primary_pattern: "forced_institutionalization_coercion_severity", estimated_mental_health_rights_index: 2.61, last_updated: "2026-06-21" },
    { id: "MHR-008", name: "ONU/CRPD — Article 12 Capacité Légale Égale, Rapporteur Santé Mentale & SDG 3.4 Bien-Être Mental", country: "Global", composite_score: 4.25, forced_institutionalization_coercion_severity_score: 4.0, psychiatric_treatment_without_consent_scale_score: 4.0, mental_health_service_access_gap_score: 5.0, stigma_discrimination_mental_health_barrier_score: 4.0, risk_level: "faible", primary_pattern: "mental_health_service_access_gap", estimated_mental_health_rights_index: 0.43, last_updated: "2026-06-21" },
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
