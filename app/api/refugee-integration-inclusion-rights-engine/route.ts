import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-integration-inclusion-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Refugee Integration Inclusion Rights Engine Agent",
  domain: "refugee_integration_inclusion_rights",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { work_authorization_economic_exclusion_severity: 3, housing_segregation_camp_confinement: 1, education_language_integration_barrier_scale: 2, social_protection_civic_participation_deficit_gap: 2 },
  top_risk_entities: ["Liban/Syrie — 1.5M Réfugiés 25% Population, Interdits Travailler 70 Secteurs, Camps Informels & Inscriptions Scolaires Échouées", "Turquie/3.5M — 3.5M Syriens, Permis Travail 15%, Ghettos Urbains, Xénophobie Montante & Expulsions Forcées 2023", "Bangladesh/Rohingya — 1M Cox Bazar Camp, 12 Ans Confinement, Éducation Limitée Myanmar Curr. & Pas Droit Travail"],
  critical_alerts: ["Liban/Syrie: work_authorization_economic_exclusion_severity", "Turquie/3.5M: housing_segregation_camp_confinement", "Bangladesh/Rohingya: education_language_integration_barrier_scale", "Australie/Offshore: social_protection_civic_participation_deficit_gap"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_refugee_integration_inclusion_rights_index: 6.13,
  data_sources: ["unhcr_global_trends_refugee_integration_report", "international_rescue_committee_integration_report", "human_rights_watch_refugee_exclusion_report"],
  entities: [
    { id: "RIR-001", name: "Liban/Syrie — 1.5M Réfugiés 25% Population, Interdits Travailler 70 Secteurs, Camps Informels & Inscriptions Scolaires Échouées", country: "Liban", composite_score: 93.55, work_authorization_economic_exclusion_severity_score: 95.0, education_language_integration_barrier_scale_score: 93.0, housing_segregation_camp_confinement_score: 92.0, social_protection_civic_participation_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "work_authorization_economic_exclusion_severity", estimated_refugee_integration_inclusion_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "RIR-002", name: "Turquie/3.5M — 3.5M Syriens, Permis Travail 15%, Ghettos Urbains, Xénophobie Montante & Expulsions Forcées 2023", country: "Turquie", composite_score: 89.65, work_authorization_economic_exclusion_severity_score: 91.0, education_language_integration_barrier_scale_score: 89.0, housing_segregation_camp_confinement_score: 90.0, social_protection_civic_participation_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "housing_segregation_camp_confinement", estimated_refugee_integration_inclusion_rights_index: 8.96, last_updated: "2026-06-21" },
    { id: "RIR-003", name: "Bangladesh/Rohingya — 1M Cox Bazar Camp, 12 Ans Confinement, Éducation Limitée Myanmar Curr. & Pas Droit Travail", country: "Bangladesh", composite_score: 86.45, work_authorization_economic_exclusion_severity_score: 87.0, education_language_integration_barrier_scale_score: 86.0, housing_segregation_camp_confinement_score: 85.0, social_protection_civic_participation_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "education_language_integration_barrier_scale", estimated_refugee_integration_inclusion_rights_index: 8.64, last_updated: "2026-06-21" },
    { id: "RIR-004", name: "Australie/Offshore — Nauru/Manus Détention Indéfinie, Interdiction Installation Permanente, Santé Mentale Crise & Boats Turn-Back Policy", country: "Australie", composite_score: 82.6, work_authorization_economic_exclusion_severity_score: 83.0, education_language_integration_barrier_scale_score: 82.0, housing_segregation_camp_confinement_score: 84.0, social_protection_civic_participation_deficit_gap_score: 81.0, risk_level: "critique", primary_pattern: "social_protection_civic_participation_deficit_gap", estimated_refugee_integration_inclusion_rights_index: 8.26, last_updated: "2026-06-21" },
    { id: "RIR-005", name: "Europe/Dublin — Dublin III Réfugiés Renvoyés, Grèce Camps Surpeuplés, Intégration Inégale & Reconnaissance Diplômes Bloquée", country: "Europe", composite_score: 55.45, work_authorization_economic_exclusion_severity_score: 56.0, education_language_integration_barrier_scale_score: 54.0, housing_segregation_camp_confinement_score: 55.0, social_protection_civic_participation_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "work_authorization_economic_exclusion_severity", estimated_refugee_integration_inclusion_rights_index: 5.54, last_updated: "2026-06-21" },
    { id: "RIR-006", name: "USA/TPS — Temporary Protected Status Expirations, Accès Services Limité, Éducation Enfants Non-Documentés & Intégration Discontinue", country: "USA", composite_score: 52.45, work_authorization_economic_exclusion_severity_score: 52.0, education_language_integration_barrier_scale_score: 51.0, housing_segregation_camp_confinement_score: 54.0, social_protection_civic_participation_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "social_protection_civic_participation_deficit_gap", estimated_refugee_integration_inclusion_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "RIR-007", name: "UNHCR/IRC — Solutions Durables 3R, International Rescue Committee, IKEA Foundation Intégration & Mécanisme Réseau Support", country: "Global", composite_score: 26.55, work_authorization_economic_exclusion_severity_score: 27.0, education_language_integration_barrier_scale_score: 25.0, housing_segregation_camp_confinement_score: 28.0, social_protection_civic_participation_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "education_language_integration_barrier_scale", estimated_refugee_integration_inclusion_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "RIR-008", name: "ONU/1951 Art.17-24 — Droits Économiques Réfugiés Conv. 1951, Art.22 Éducation, Art.21 Logement & SDG 10.7 Migration", country: "Global", composite_score: 4.0, work_authorization_economic_exclusion_severity_score: 4.0, education_language_integration_barrier_scale_score: 4.0, housing_segregation_camp_confinement_score: 4.0, social_protection_civic_participation_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "work_authorization_economic_exclusion_severity", estimated_refugee_integration_inclusion_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-integration-inclusion-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
