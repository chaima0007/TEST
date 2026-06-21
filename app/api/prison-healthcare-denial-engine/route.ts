import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-healthcare-denial-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Healthcare Denial Engine Agent",
  domain: "prison_healthcare_denial",
  total_entities: 8,
  avg_composite: 61.56,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { infectious_disease_spread: 2, torture_medical_complicity: 2, medical_care_denial_scale: 2, mental_health_neglect: 2 },
  top_risk_entities: [
    "USA — 2.2M Détenus, HCV 17x Pop. Générale, COVID Prison 3x & For-Profit Healthcare Denial",
    "Brésil — 900K Détenus, TB 35x Pop. Générale, Surpopulation 170% & HCV Non Traité",
    "Russie — TB-MR Pénitentiaire, Psychiatrie Punitive Opposants & CEDH Condamnations Soins",
  ],
  critical_alerts: [
    "USA: infectious_disease_spread",
    "Brésil: infectious_disease_spread",
    "Russie: torture_medical_complicity",
    "Philippines: medical_care_denial_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_healthcare_denial_index: 6.16,
  data_sources: [
    "penal_reform_international_prison_health_standards_mandela_rules",
    "who_prison_health_infectious_disease_tuberculosis_hiv_report",
    "hrw_sick_unable_to_get_care_prison_healthcare_denial_report",
  ],
  entities: [
    { entity_id: "PH-001", name: "USA — 2.2M Détenus, HCV 17x Pop. Générale, COVID Prison 3x & For-Profit Healthcare Denial", country: "Amérique du Nord", composite_score: 92.85, medical_care_denial_scale_score: 95.0, mental_health_neglect_score: 92.0, infectious_disease_spread_score: 95.0, torture_medical_complicity_score: 88.0, risk_level: "critique", primary_pattern: "infectious_disease_spread", estimated_prison_healthcare_denial_index: 9.29, last_updated: "2026-06-21" },
    { entity_id: "PH-002", name: "Brésil — 900K Détenus, TB 35x Pop. Générale, Surpopulation 170% & HCV Non Traité", country: "Amérique Latine", composite_score: 89.6, medical_care_denial_scale_score: 90.0, mental_health_neglect_score: 88.0, infectious_disease_spread_score: 92.0, torture_medical_complicity_score: 88.0, risk_level: "critique", primary_pattern: "infectious_disease_spread", estimated_prison_healthcare_denial_index: 8.96, last_updated: "2026-06-21" },
    { entity_id: "PH-003", name: "Russie — TB-MR Pénitentiaire, Psychiatrie Punitive Opposants & CEDH Condamnations Soins", country: "Europe de l'Est", composite_score: 89.4, medical_care_denial_scale_score: 88.0, mental_health_neglect_score: 92.0, infectious_disease_spread_score: 88.0, torture_medical_complicity_score: 90.0, risk_level: "critique", primary_pattern: "torture_medical_complicity", estimated_prison_healthcare_denial_index: 8.94, last_updated: "2026-06-21" },
    { entity_id: "PH-004", name: "Philippines — Drug War 800% Surpopulation, Maladies Infectieuses, Torture & Soins Absents", country: "Asie du Sud-Est", composite_score: 86.35, medical_care_denial_scale_score: 85.0, mental_health_neglect_score: 85.0, infectious_disease_spread_score: 88.0, torture_medical_complicity_score: 88.0, risk_level: "critique", primary_pattern: "medical_care_denial_scale", estimated_prison_healthcare_denial_index: 8.64, last_updated: "2026-06-21" },
    { entity_id: "PH-005", name: "Mexique — Prisons Rurales Sans Médecin, Surpopulation 200%+ & Malnutrition Systémique", country: "Amérique Latine", composite_score: 53.65, medical_care_denial_scale_score: 55.0, mental_health_neglect_score: 52.0, infectious_disease_spread_score: 55.0, torture_medical_complicity_score: 52.0, risk_level: "élevé", primary_pattern: "medical_care_denial_scale", estimated_prison_healthcare_denial_index: 5.37, last_updated: "2026-06-21" },
    { entity_id: "PH-006", name: "France — Suicide Prison 10x Pop. Générale, Santé Mentale Défaillante & CGLPL Alertes", country: "Europe", composite_score: 50.35, medical_care_denial_scale_score: 50.0, mental_health_neglect_score: 55.0, infectious_disease_spread_score: 48.0, torture_medical_complicity_score: 48.0, risk_level: "élevé", primary_pattern: "mental_health_neglect", estimated_prison_healthcare_denial_index: 5.04, last_updated: "2026-06-21" },
    { entity_id: "PH-007", name: "PRI/Penal Reform — Standards Mandela Règles 24-35, Monitoring Soins Médicaux & Plaidoyer", country: "Global", composite_score: 25.85, medical_care_denial_scale_score: 22.0, mental_health_neglect_score: 28.0, infectious_disease_spread_score: 25.0, torture_medical_complicity_score: 30.0, risk_level: "modéré", primary_pattern: "mental_health_neglect", estimated_prison_healthcare_denial_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "PH-008", name: "ONU/Règles Nelson Mandela — Règles 24-35 Soins Médicaux & Convention Torture Art.16", country: "Global", composite_score: 4.4, medical_care_denial_scale_score: 4.0, mental_health_neglect_score: 5.0, infectious_disease_spread_score: 3.0, torture_medical_complicity_score: 6.0, risk_level: "faible", primary_pattern: "torture_medical_complicity", estimated_prison_healthcare_denial_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-healthcare-denial-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
