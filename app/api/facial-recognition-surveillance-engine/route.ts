import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[facial-recognition-surveillance-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Facial Recognition Surveillance Engine Agent",
  domain: "facial_recognition_surveillance",
  total_entities: 8,
  avg_composite: 61.57,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { mass_surveillance_deployment_scale: 2, chilling_effect_dissent_suppression: 2, minority_targeting_bias_severity: 2, legal_oversight_framework_absence: 2 },
  top_risk_entities: [
    "Chine — 1Md+ Visages Xinjiang, Crédit Social Biométrique, Ouïghours Géolocalisés & Internement IA",
    "Russie — 100K Caméras Moscou, Opposants Identifiés Métro, Manifestants Arrêtés Temps Réel",
    "Inde — CCTNS/AFRS National, Manifestants CAA Identifiés, Biais Racial & 100M Visages Base",
  ],
  critical_alerts: [
    "Chine: mass_surveillance_deployment_scale",
    "Russie: chilling_effect_dissent_suppression",
    "Inde: minority_targeting_bias_severity",
    "UAE/Émirats: legal_oversight_framework_absence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_facial_recognition_surveillance_index: 6.16,
  data_sources: [
    "algorithmic_justice_league_facial_recognition_bias_audit",
    "access_now_edri_ban_biometric_surveillance_eu_ai_act_report",
    "un_ohchr_digital_surveillance_human_rights_facial_recognition",
  ],
  entities: [
    { id: "FRS-001", name: "Chine — 1Md+ Visages Xinjiang, Crédit Social Biométrique, Ouïghours Géolocalisés & Internement IA", country: "Asie de l'Est", composite_score: 93.65, mass_surveillance_deployment_scale_score: 95.0, minority_targeting_bias_severity_score: 95.0, legal_oversight_framework_absence_score: 92.0, chilling_effect_dissent_suppression_score: 92.0, risk_level: "critique", primary_pattern: "mass_surveillance_deployment_scale", estimated_facial_recognition_surveillance_index: 9.37, last_updated: "2026-06-21" },
    { id: "FRS-002", name: "Russie — 100K Caméras Moscou, Opposants Identifiés Métro, Manifestants Arrêtés Temps Réel", country: "Europe de l'Est", composite_score: 90.4, mass_surveillance_deployment_scale_score: 90.0, minority_targeting_bias_severity_score: 88.0, legal_oversight_framework_absence_score: 92.0, chilling_effect_dissent_suppression_score: 92.0, risk_level: "critique", primary_pattern: "chilling_effect_dissent_suppression", estimated_facial_recognition_surveillance_index: 9.04, last_updated: "2026-06-21" },
    { id: "FRS-003", name: "Inde — CCTNS/AFRS National, Manifestants CAA Identifiés, Biais Racial & 100M Visages Base", country: "Asie du Sud", composite_score: 87.9, mass_surveillance_deployment_scale_score: 88.0, minority_targeting_bias_severity_score: 90.0, legal_oversight_framework_absence_score: 88.0, chilling_effect_dissent_suppression_score: 85.0, risk_level: "critique", primary_pattern: "minority_targeting_bias_severity", estimated_facial_recognition_surveillance_index: 8.79, last_updated: "2026-06-21" },
    { id: "FRS-004", name: "UAE/Émirats — Surveillance Biométrique Dissidents, Journalistes Identifiés & Frontières FR 100%", country: "Moyen-Orient", composite_score: 86.5, mass_surveillance_deployment_scale_score: 85.0, minority_targeting_bias_severity_score: 88.0, legal_oversight_framework_absence_score: 88.0, chilling_effect_dissent_suppression_score: 85.0, risk_level: "critique", primary_pattern: "legal_oversight_framework_absence", estimated_facial_recognition_surveillance_index: 8.65, last_updated: "2026-06-21" },
    { id: "FRS-005", name: "USA — Police FR Faux Positifs Noirs 100x Blancs, Pas de Loi Fédérale & Amazon Rekognition", country: "Amérique du Nord", composite_score: 53.25, mass_surveillance_deployment_scale_score: 55.0, minority_targeting_bias_severity_score: 52.0, legal_oversight_framework_absence_score: 55.0, chilling_effect_dissent_suppression_score: 50.0, risk_level: "élevé", primary_pattern: "minority_targeting_bias_severity", estimated_facial_recognition_surveillance_index: 5.33, last_updated: "2026-06-21" },
    { id: "FRS-006", name: "UK — Live FR Police Manifestants, 1/3 CCTV Mondial Londres & Bridges v. South Wales Arrêt", country: "Europe", composite_score: 50.6, mass_surveillance_deployment_scale_score: 52.0, minority_targeting_bias_severity_score: 48.0, legal_oversight_framework_absence_score: 52.0, chilling_effect_dissent_suppression_score: 50.0, risk_level: "élevé", primary_pattern: "mass_surveillance_deployment_scale", estimated_facial_recognition_surveillance_index: 5.06, last_updated: "2026-06-21" },
    { id: "FRS-007", name: "EDRi/Fight for the Future — Coalition Ban FR Europe, AI Act Advocacy & Moratorium Campagne", country: "Global", composite_score: 25.85, mass_surveillance_deployment_scale_score: 22.0, minority_targeting_bias_severity_score: 28.0, legal_oversight_framework_absence_score: 25.0, chilling_effect_dissent_suppression_score: 30.0, risk_level: "modéré", primary_pattern: "legal_oversight_framework_absence", estimated_facial_recognition_surveillance_index: 2.59, last_updated: "2026-06-21" },
    { id: "FRS-008", name: "ONU/OHCHR — Rapport Surveillance Numérique Droits Humains, Moratorium FR Demandé & ICCPR Art.17", country: "Global", composite_score: 4.4, mass_surveillance_deployment_scale_score: 4.0, minority_targeting_bias_severity_score: 5.0, legal_oversight_framework_absence_score: 3.0, chilling_effect_dissent_suppression_score: 6.0, risk_level: "faible", primary_pattern: "chilling_effect_dissent_suppression", estimated_facial_recognition_surveillance_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/facial-recognition-surveillance-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
