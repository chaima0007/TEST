import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-digital-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Refugee Digital Rights Engine Agent",
  domain: "refugee_digital_rights",
  total_entities: 8,
  avg_composite: 61.77,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { data_sharing_persecution_risk_gap: 2, surveillance_control_refugee_population: 2, digital_exclusion_service_denial_severity: 2, biometric_data_coercion_scale: 2 },
  top_risk_entities: [
    "Bangladesh/Rohingyas — UNHCR Biométrie Forcée, Données Partagées Myanmar & Camp Numérique",
    "Jordanie/Liban — 1,5M Syriens, SIM Biométrique Obligatoire & Surveillance Téléphonie",
    "Kenya/Dadaab — Biométrie UNHCR, Couverture Internet 3%, Services Numériques Bloqués Réfugiés",
  ],
  critical_alerts: [
    "Bangladesh/Rohingyas: data_sharing_persecution_risk_gap",
    "Jordanie/Liban: surveillance_control_refugee_population",
    "Kenya/Dadaab: digital_exclusion_service_denial_severity",
    "UE/Eurodac: biometric_data_coercion_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_refugee_digital_rights_index: 6.18,
  data_sources: [
    "privacy_international_unhcr_biometric_data_refugee_rights_report",
    "human_rights_watch_digital_id_surveillance_refugees_global_review",
    "alan_turing_institute_data_protection_displaced_populations_study",
  ],
  entities: [
    { id: "RDR-001", name: "Bangladesh/Rohingyas — UNHCR Biométrie Forcée, Données Partagées Myanmar & Camp Numérique", country: "Asie du Sud", composite_score: 92.5, biometric_data_coercion_scale_score: 95.0, digital_exclusion_service_denial_severity_score: 88.0, surveillance_control_refugee_population_score: 92.0, data_sharing_persecution_risk_gap_score: 95.0, risk_level: "critique", primary_pattern: "data_sharing_persecution_risk_gap", estimated_refugee_digital_rights_index: 9.25, last_updated: "2026-06-21" },
    { id: "RDR-002", name: "Jordanie/Liban — 1,5M Syriens, SIM Biométrique Obligatoire & Surveillance Téléphonie", country: "Moyen-Orient", composite_score: 90.7, biometric_data_coercion_scale_score: 92.0, digital_exclusion_service_denial_severity_score: 90.0, surveillance_control_refugee_population_score: 92.0, data_sharing_persecution_risk_gap_score: 88.0, risk_level: "critique", primary_pattern: "surveillance_control_refugee_population", estimated_refugee_digital_rights_index: 9.07, last_updated: "2026-06-21" },
    { id: "RDR-003", name: "Kenya/Dadaab — Biométrie UNHCR, Couverture Internet 3%, Services Numériques Bloqués Réfugiés", country: "Afrique de l'Est", composite_score: 88.25, biometric_data_coercion_scale_score: 88.0, digital_exclusion_service_denial_severity_score: 92.0, surveillance_control_refugee_population_score: 85.0, data_sharing_persecution_risk_gap_score: 88.0, risk_level: "critique", primary_pattern: "digital_exclusion_service_denial_severity", estimated_refugee_digital_rights_index: 8.83, last_updated: "2026-06-21" },
    { id: "RDR-004", name: "UE/Eurodac — Empreintes Digitales Demandeurs Asile, Interopérabilité Bases Police & Leaks", country: "Europe", composite_score: 86.5, biometric_data_coercion_scale_score: 88.0, digital_exclusion_service_denial_severity_score: 82.0, surveillance_control_refugee_population_score: 88.0, data_sharing_persecution_risk_gap_score: 88.0, risk_level: "critique", primary_pattern: "biometric_data_coercion_scale", estimated_refugee_digital_rights_index: 8.65, last_updated: "2026-06-21" },
    { id: "RDR-005", name: "Turquie — 3,6M Syriens, Surveillance Apps, Expulsions Via Données Téléphoniques", country: "Europe/Asie", composite_score: 53.65, biometric_data_coercion_scale_score: 55.0, digital_exclusion_service_denial_severity_score: 52.0, surveillance_control_refugee_population_score: 55.0, data_sharing_persecution_risk_gap_score: 52.0, risk_level: "élevé", primary_pattern: "biometric_data_coercion_scale", estimated_refugee_digital_rights_index: 5.37, last_updated: "2026-06-21" },
    { id: "RDR-006", name: "Australie — Offshore Processing Numérique, Surveillance Manus/Nauru & IMSI Catchers Camps", country: "Océanie", composite_score: 52.35, biometric_data_coercion_scale_score: 52.0, digital_exclusion_service_denial_severity_score: 55.0, surveillance_control_refugee_population_score: 52.0, data_sharing_persecution_risk_gap_score: 50.0, risk_level: "élevé", primary_pattern: "digital_exclusion_service_denial_severity", estimated_refugee_digital_rights_index: 5.24, last_updated: "2026-06-21" },
    { id: "RDR-007", name: "Privacy International/UNHCR — Data Protection Réfugiés, Biométrie Éthique & Do No Harm", country: "Global", composite_score: 25.85, biometric_data_coercion_scale_score: 22.0, digital_exclusion_service_denial_severity_score: 28.0, surveillance_control_refugee_population_score: 25.0, data_sharing_persecution_risk_gap_score: 30.0, risk_level: "modéré", primary_pattern: "data_sharing_persecution_risk_gap", estimated_refugee_digital_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "RDR-008", name: "ONU/HCR — Convention Réfugiés 1951, SDG 16 Identité Légale & RGPD Personnes Déplacées", country: "Global", composite_score: 4.4, biometric_data_coercion_scale_score: 4.0, digital_exclusion_service_denial_severity_score: 5.0, surveillance_control_refugee_population_score: 3.0, data_sharing_persecution_risk_gap_score: 6.0, risk_level: "faible", primary_pattern: "surveillance_control_refugee_population", estimated_refugee_digital_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-digital-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
