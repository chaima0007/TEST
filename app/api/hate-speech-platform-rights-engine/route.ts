import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hate-speech-platform-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Hate Speech Platform Rights Engine Agent",
  domain: "hate_speech_platform_rights",
  total_entities: 8,
  avg_composite: 61.29,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { online_hate_escalation_violence_severity: 2, content_moderation_bias_minority_targeting: 2, platform_impunity_accountability_gap: 2, victim_legal_redress_absence_scale: 2 },
  top_risk_entities: [
    "Myanmar/Facebook — Discours Haine Rohingyas, Génocide Algorithmique & Zéro Modération Birmane",
    "Inde/WhatsApp — Lynchages Viraux, Fake News Musulmans & 200M Users Sans Vérification",
    "Éthiopie/Tigré — Facebook Haine Ethnique Tigréens, Massacres & Algorithme Amplification",
  ],
  critical_alerts: [
    "Myanmar/Facebook: online_hate_escalation_violence_severity",
    "Inde/WhatsApp: content_moderation_bias_minority_targeting",
    "Éthiopie/Tigré: platform_impunity_accountability_gap",
    "USA/Twitter-X: platform_impunity_accountability_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_hate_speech_platform_rights_index: 6.13,
  data_sources: [
    "un_special_adviser_genocide_prevention_myanmar_facebook_hate_speech_report",
    "global_witnesses_facebook_hate_speech_ethiopia_tigray_investigation",
    "adl_online_hate_index_platform_accountability_annual_report",
  ],
  entities: [
    { id: "HSP-001", name: "Myanmar/Facebook — Discours Haine Rohingyas, Génocide Algorithmique & Zéro Modération Birmane", country: "Asie du Sud-Est", composite_score: 92.5, online_hate_escalation_violence_severity_score: 95.0, content_moderation_bias_minority_targeting_score: 92.0, platform_impunity_accountability_gap_score: 92.0, victim_legal_redress_absence_scale_score: 90.0, risk_level: "critique", primary_pattern: "online_hate_escalation_violence_severity", estimated_hate_speech_platform_rights_index: 9.25, last_updated: "2026-06-21" },
    { id: "HSP-002", name: "Inde/WhatsApp — Lynchages Viraux, Fake News Musulmans & 200M Users Sans Vérification", country: "Asie du Sud", composite_score: 89.6, online_hate_escalation_violence_severity_score: 90.0, content_moderation_bias_minority_targeting_score: 92.0, platform_impunity_accountability_gap_score: 88.0, victim_legal_redress_absence_scale_score: 88.0, risk_level: "critique", primary_pattern: "content_moderation_bias_minority_targeting", estimated_hate_speech_platform_rights_index: 8.96, last_updated: "2026-06-21" },
    { id: "HSP-003", name: "Éthiopie/Tigré — Facebook Haine Ethnique Tigréens, Massacres & Algorithme Amplification", country: "Afrique de l'Est", composite_score: 88.1, online_hate_escalation_violence_severity_score: 88.0, content_moderation_bias_minority_targeting_score: 88.0, platform_impunity_accountability_gap_score: 90.0, victim_legal_redress_absence_scale_score: 86.0, risk_level: "critique", primary_pattern: "platform_impunity_accountability_gap", estimated_hate_speech_platform_rights_index: 8.81, last_updated: "2026-06-21" },
    { id: "HSP-004", name: "USA/Twitter-X — Suppression Modération, Haine Raciale & Islamophobie Sans Restriction", country: "Amérique du Nord", composite_score: 85.8, online_hate_escalation_violence_severity_score: 85.0, content_moderation_bias_minority_targeting_score: 86.0, platform_impunity_accountability_gap_score: 88.0, victim_legal_redress_absence_scale_score: 84.0, risk_level: "critique", primary_pattern: "platform_impunity_accountability_gap", estimated_hate_speech_platform_rights_index: 8.58, last_updated: "2026-06-21" },
    { id: "HSP-005", name: "UE — DSA Insuffisant, Haine En Ligne +40% & Délais Retrait 24h Non Respectés", country: "Europe", composite_score: 53.5, online_hate_escalation_violence_severity_score: 55.0, content_moderation_bias_minority_targeting_score: 52.0, platform_impunity_accountability_gap_score: 52.0, victim_legal_redress_absence_scale_score: 55.0, risk_level: "élevé", primary_pattern: "victim_legal_redress_absence_scale", estimated_hate_speech_platform_rights_index: 5.35, last_updated: "2026-06-21" },
    { id: "HSP-006", name: "Afrique/Asie Francophone — Haine Ethnique Sans Modération Locale & Zéro Langue Minoritaire", country: "Afrique/Asie", composite_score: 50.6, online_hate_escalation_violence_severity_score: 50.0, content_moderation_bias_minority_targeting_score: 52.0, platform_impunity_accountability_gap_score: 52.0, victim_legal_redress_absence_scale_score: 48.0, risk_level: "élevé", primary_pattern: "content_moderation_bias_minority_targeting", estimated_hate_speech_platform_rights_index: 5.06, last_updated: "2026-06-21" },
    { id: "HSP-007", name: "Global Voices/ADL — Monitoring Discours Haine, Contre-Narration & Plaidoyer DSA/Section 230", country: "Global", composite_score: 25.85, online_hate_escalation_violence_severity_score: 22.0, content_moderation_bias_minority_targeting_score: 28.0, platform_impunity_accountability_gap_score: 25.0, victim_legal_redress_absence_scale_score: 30.0, risk_level: "modéré", primary_pattern: "victim_legal_redress_absence_scale", estimated_hate_speech_platform_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "HSP-008", name: "ONU/HRC — Plan Rabat Discours Haine, Rapporteur Spécial Liberté Expression & SDG 16", country: "Global", composite_score: 4.4, online_hate_escalation_violence_severity_score: 4.0, content_moderation_bias_minority_targeting_score: 5.0, platform_impunity_accountability_gap_score: 3.0, victim_legal_redress_absence_scale_score: 6.0, risk_level: "faible", primary_pattern: "online_hate_escalation_violence_severity", estimated_hate_speech_platform_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hate-speech-platform-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
