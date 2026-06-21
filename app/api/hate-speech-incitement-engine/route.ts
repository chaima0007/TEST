import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hate-speech-incitement-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Hate Speech Incitement Engine Agent",
  domain: "hate_speech_incitement",
  total_entities: 8,
  avg_composite: 61.67,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { incitement_violence_scale: 1, minority_targeting_pattern: 1, platform_amplification_failure: 3, legal_accountability_gap: 3 },
  top_risk_entities: [
    "Myanmar/Facebook — Rohingya Génocide 2017, Aveu Zuckerberg Échec Modération & 700K Déplacés",
    "Éthiopie/Tigray — Facebook Discours Ethnique Meurtriers, 500K Morts & Appels Génocide Tigréens",
    "Inde/BJP — Comptes Vérifiés Twitter Discours Anti-Musulmans, Incitation Pogroms & Silence X",
  ],
  critical_alerts: [
    "Myanmar/Facebook: incitement_violence_scale",
    "Éthiopie/Tigray: minority_targeting_pattern",
    "Inde/BJP: platform_amplification_failure",
    "USA/Jan.6: platform_amplification_failure",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_hate_speech_incitement_index: 6.17,
  data_sources: [
    "un_special_adviser_prevention_genocide_hate_speech_report",
    "global_network_initiative_content_moderation_human_rights_assessment",
    "ims_media_monitoring_hate_speech_conflict_zones_database",
  ],
  entities: [
    { entity_id: "HS-001", name: "Myanmar/Facebook — Rohingya Génocide 2017, Aveu Zuckerberg Échec Modération & 700K Déplacés", country: "Asie du Sud-Est", composite_score: 93.25, incitement_violence_scale_score: 95.0, platform_amplification_failure_score: 95.0, legal_accountability_gap_score: 92.0, minority_targeting_pattern_score: 90.0, risk_level: "critique", primary_pattern: "incitement_violence_scale", estimated_hate_speech_incitement_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "HS-002", name: "Éthiopie/Tigray — Facebook Discours Ethnique Meurtriers, 500K Morts & Appels Génocide Tigréens", country: "Afrique de l'Est", composite_score: 90.5, incitement_violence_scale_score: 92.0, platform_amplification_failure_score: 90.0, legal_accountability_gap_score: 88.0, minority_targeting_pattern_score: 92.0, risk_level: "critique", primary_pattern: "minority_targeting_pattern", estimated_hate_speech_incitement_index: 9.05, last_updated: "2026-06-21" },
    { entity_id: "HS-003", name: "Inde/BJP — Comptes Vérifiés Twitter Discours Anti-Musulmans, Incitation Pogroms & Silence X", country: "Asie du Sud", composite_score: 88.5, incitement_violence_scale_score: 88.0, platform_amplification_failure_score: 90.0, legal_accountability_gap_score: 88.0, minority_targeting_pattern_score: 88.0, risk_level: "critique", primary_pattern: "platform_amplification_failure", estimated_hate_speech_incitement_index: 8.85, last_updated: "2026-06-21" },
    { entity_id: "HS-004", name: "USA/Jan.6 — Incitation Trump Capitol, Plateformes Tardives & Musk Réintègre Comptes Haineux", country: "Amérique du Nord", composite_score: 86.35, incitement_violence_scale_score: 85.0, platform_amplification_failure_score: 88.0, legal_accountability_gap_score: 85.0, minority_targeting_pattern_score: 88.0, risk_level: "critique", primary_pattern: "platform_amplification_failure", estimated_hate_speech_incitement_index: 8.64, last_updated: "2026-06-21" },
    { entity_id: "HS-005", name: "UE/DSA — Règlement Services Numériques 2024, Sanctions Meta & Enforcement Lacunaire", country: "Europe", composite_score: 53.85, incitement_violence_scale_score: 52.0, platform_amplification_failure_score: 58.0, legal_accountability_gap_score: 55.0, minority_targeting_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "legal_accountability_gap", estimated_hate_speech_incitement_index: 5.39, last_updated: "2026-06-21" },
    { entity_id: "HS-006", name: "Russie/RT — Propagande État Déshumanisation Ukraine, Discours Guerre Génocidaire & Bans Tardifs", country: "Europe de l'Est", composite_score: 50.65, incitement_violence_scale_score: 48.0, platform_amplification_failure_score: 55.0, legal_accountability_gap_score: 50.0, minority_targeting_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "platform_amplification_failure", estimated_hate_speech_incitement_index: 5.07, last_updated: "2026-06-21" },
    { entity_id: "HS-007", name: "Global Network Initiative/Access Now — Standards Modération & Droits Humains Ligne", country: "Global", composite_score: 25.85, incitement_violence_scale_score: 22.0, platform_amplification_failure_score: 25.0, legal_accountability_gap_score: 28.0, minority_targeting_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "legal_accountability_gap", estimated_hate_speech_incitement_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "HS-008", name: "ONU/Plan Action Rabat & Stratégie Discours Haine — Seuils Incitation & Liberté Expression", country: "Global", composite_score: 4.4, incitement_violence_scale_score: 4.0, platform_amplification_failure_score: 5.0, legal_accountability_gap_score: 3.0, minority_targeting_pattern_score: 6.0, risk_level: "faible", primary_pattern: "legal_accountability_gap", estimated_hate_speech_incitement_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/hate-speech-incitement-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
