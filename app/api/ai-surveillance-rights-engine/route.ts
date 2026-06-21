import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-surveillance-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "AI Surveillance Rights Engine Agent",
  domain: "ai_surveillance_rights",
  total_entities: 8,
  avg_composite: 61.6,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { mass_surveillance_biometric_severity: 4, predictive_policing_racial_targeting: 2, data_privacy_algorithmic_accountability_gap: 2 },
  top_risk_entities: [
    "China — SCS Social Credit System 1,4Md, Xinjiang Surveillance Totale & 700M Caméras CCTV AI",
    "Russia — SORM Surveillance Totale, Reconnaissance Faciale Moscou 200k Caméras & Militants Ciblés",
    "Iran — Surveillance Internet Filtrée, AI Reconnaisance Protestataires 2022 & Arrestations Algorithme",
  ],
  critical_alerts: [
    "China: mass_surveillance_biometric_severity",
    "Russia: mass_surveillance_biometric_severity",
    "Iran: predictive_policing_racial_targeting",
    "India: mass_surveillance_biometric_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_ai_surveillance_rights_index: 6.16,
  data_sources: [
    "amnesty_international_surveillance_giants_ai_report",
    "eff_atlas_of_surveillance_2023",
    "ohchr_right_to_privacy_digital_age_report",
  ],
  entities: [
    { id: "ASR-001", name: "China — SCS Social Credit System 1,4Md, Xinjiang Surveillance Totale & 700M Caméras CCTV AI", country: "Chine", composite_score: 93.95, mass_surveillance_biometric_severity_score: 96.0, social_scoring_behavioral_control_scale_score: 94.0, predictive_policing_racial_targeting_score: 93.0, data_privacy_algorithmic_accountability_gap_score: 92.0, risk_level: "critique", primary_pattern: "mass_surveillance_biometric_severity", estimated_ai_surveillance_rights_index: 9.4, last_updated: "2026-06-21" },
    { id: "ASR-002", name: "Russia — SORM Surveillance Totale, Reconnaissance Faciale Moscou 200k Caméras & Militants Ciblés", country: "Russie", composite_score: 90.95, mass_surveillance_biometric_severity_score: 93.0, social_scoring_behavioral_control_scale_score: 90.0, predictive_policing_racial_targeting_score: 91.0, data_privacy_algorithmic_accountability_gap_score: 89.0, risk_level: "critique", primary_pattern: "mass_surveillance_biometric_severity", estimated_ai_surveillance_rights_index: 9.1, last_updated: "2026-06-21" },
    { id: "ASR-003", name: "Iran — Surveillance Internet Filtrée, AI Reconnaisance Protestataires 2022 & Arrestations Algorithme", country: "Iran", composite_score: 87.95, mass_surveillance_biometric_severity_score: 90.0, social_scoring_behavioral_control_scale_score: 87.0, predictive_policing_racial_targeting_score: 88.0, data_privacy_algorithmic_accountability_gap_score: 86.0, risk_level: "critique", primary_pattern: "predictive_policing_racial_targeting", estimated_ai_surveillance_rights_index: 8.8, last_updated: "2026-06-21" },
    { id: "ASR-004", name: "India — Aadhaar Biométrique 1,4Md, Surveillance Cachemire & Facial Recognition Manifestants CAA", country: "Inde", composite_score: 84.95, mass_surveillance_biometric_severity_score: 87.0, social_scoring_behavioral_control_scale_score: 84.0, predictive_policing_racial_targeting_score: 85.0, data_privacy_algorithmic_accountability_gap_score: 83.0, risk_level: "critique", primary_pattern: "mass_surveillance_biometric_severity", estimated_ai_surveillance_rights_index: 8.5, last_updated: "2026-06-21" },
    { id: "ASR-005", name: "USA — Clearview AI 30Md Visages, Predictive Policing Chicago/LA & NYPD Drone Surveillance", country: "USA", composite_score: 54.0, mass_surveillance_biometric_severity_score: 56.0, social_scoring_behavioral_control_scale_score: 53.0, predictive_policing_racial_targeting_score: 55.0, data_privacy_algorithmic_accountability_gap_score: 51.0, risk_level: "élevé", primary_pattern: "predictive_policing_racial_targeting", estimated_ai_surveillance_rights_index: 5.4, last_updated: "2026-06-21" },
    { id: "ASR-006", name: "Europe — ANPR London Ring of Steel, Belgique Clearview Ban, IA Act Implemention Gap", country: "Europe", composite_score: 50.95, mass_surveillance_biometric_severity_score: 53.0, social_scoring_behavioral_control_scale_score: 50.0, predictive_policing_racial_targeting_score: 51.0, data_privacy_algorithmic_accountability_gap_score: 49.0, risk_level: "élevé", primary_pattern: "data_privacy_algorithmic_accountability_gap", estimated_ai_surveillance_rights_index: 5.1, last_updated: "2026-06-21" },
    { id: "ASR-007", name: "EFF/Amnesty Tech — Ban Facial Recognition Campagne, Algorithmic Accountability & GDPR Enforcement", country: "Global", composite_score: 25.85, mass_surveillance_biometric_severity_score: 27.0, social_scoring_behavioral_control_scale_score: 25.0, predictive_policing_racial_targeting_score: 26.0, data_privacy_algorithmic_accountability_gap_score: 25.0, risk_level: "modéré", primary_pattern: "mass_surveillance_biometric_severity", estimated_ai_surveillance_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "ASR-008", name: "ONU/OHCHR — Rapport IA Droits Homme, Cadre Réglementation & SDG 16.10 Accès Information", country: "Global", composite_score: 4.2, mass_surveillance_biometric_severity_score: 4.0, social_scoring_behavioral_control_scale_score: 4.0, predictive_policing_racial_targeting_score: 4.0, data_privacy_algorithmic_accountability_gap_score: 5.0, risk_level: "faible", primary_pattern: "data_privacy_algorithmic_accountability_gap", estimated_ai_surveillance_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-surveillance-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
