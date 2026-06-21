import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[minority-language-cultural-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Minority Language Cultural Rights Engine Agent",
  domain: "minority_language_cultural_rights",
  total_entities: 8,
  avg_composite: 61.35,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    language_prohibition_forced_assimilation_severity: 3,
    minority_language_education_media_suppression_scale: 2,
    cultural_heritage_destruction_appropriation: 0,
    language_revitalization_legal_recognition_deficit_gap: 3,
  },
  top_risk_entities: ["MLC-001", "MLC-002", "MLC-003"],
  critical_alerts: [
    "MLC-001 (Chine/Tibétain-Ouïghour): composite=93.55 — language_prohibition_forced_assimilation_severity",
    "MLC-002 (Turquie/Kurde): composite=89.65 — minority_language_education_media_suppression_scale",
    "MLC-003 (France/Langues Régionales): composite=86.55 — language_revitalization_legal_recognition_deficit_gap",
    "MLC-004 (USA/Hawaiian-Navajo): composite=82.60 — language_prohibition_forced_assimilation_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_minority_language_cultural_rights_index: 6.14,
  data_sources: [
    "unesco_endangered_languages_atlas",
    "minority_rights_group_language_report",
    "un_special_rapporteur_minority_rights_language",
  ],
  entities: [
    {
      entity_id: "MLC-001",
      name: "Chine/Tibétain-Ouïghour — Langues Tibétaines Interdites Écoles 2020, Ouïghour Alphabet Latin Supprimé, Monastères Fermés & Enseignement Mandarin Forcé",
      country: "Chine",
      language_prohibition_forced_assimilation_severity_score: 95.0,
      minority_language_education_media_suppression_scale_score: 93.0,
      cultural_heritage_destruction_appropriation_score: 92.0,
      language_revitalization_legal_recognition_deficit_gap_score: 94.0,
      composite_score: 93.55,
      risk_level: "critique",
      primary_pattern: "language_prohibition_forced_assimilation_severity",
      estimated_minority_language_cultural_rights_index: 9.36,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-002",
      name: "Turquie/Kurde — Kurde Interdit 1924-1991, PKK Excuse Censure Médias, Fonctionnaires Kurdes Destitués & Enseignement Limité Privé",
      country: "Turquie",
      language_prohibition_forced_assimilation_severity_score: 91.0,
      minority_language_education_media_suppression_scale_score: 89.0,
      cultural_heritage_destruction_appropriation_score: 90.0,
      language_revitalization_legal_recognition_deficit_gap_score: 88.0,
      composite_score: 89.65,
      risk_level: "critique",
      primary_pattern: "minority_language_education_media_suppression_scale",
      estimated_minority_language_cultural_rights_index: 8.97,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-003",
      name: "France/Langues Régionales — Loi 2021 Invalidée Occitan/Breton, Alsacien Déclin 50% Locuteurs, Éducation Bilingue Bloquée & République Une Et Indivisible",
      country: "France",
      language_prohibition_forced_assimilation_severity_score: 87.0,
      minority_language_education_media_suppression_scale_score: 85.0,
      cultural_heritage_destruction_appropriation_score: 88.0,
      language_revitalization_legal_recognition_deficit_gap_score: 86.0,
      composite_score: 86.55,
      risk_level: "critique",
      primary_pattern: "language_revitalization_legal_recognition_deficit_gap",
      estimated_minority_language_cultural_rights_index: 8.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-004",
      name: "USA/Hawaiian-Navajo — Hawaiian Quasi-Éteint 1970s, Navajo Code Talkers Honte Post-Guerre, English-Only Lois 31 États & Boarding Schools Héritage",
      country: "USA",
      language_prohibition_forced_assimilation_severity_score: 83.0,
      minority_language_education_media_suppression_scale_score: 82.0,
      cultural_heritage_destruction_appropriation_score: 84.0,
      language_revitalization_legal_recognition_deficit_gap_score: 81.0,
      composite_score: 82.60,
      risk_level: "critique",
      primary_pattern: "language_prohibition_forced_assimilation_severity",
      estimated_minority_language_cultural_rights_index: 8.26,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-005",
      name: "Russie/Langues — 17 Langues Minorités Non-Enseignées Post-2018 Loi, Tatare Kirillisé Forcé, Médias Locaux Fermés & Pression Identité Russe",
      country: "Russie",
      language_prohibition_forced_assimilation_severity_score: 56.0,
      minority_language_education_media_suppression_scale_score: 54.0,
      cultural_heritage_destruction_appropriation_score: 55.0,
      language_revitalization_legal_recognition_deficit_gap_score: 57.0,
      composite_score: 55.45,
      risk_level: "élevé",
      primary_pattern: "minority_language_education_media_suppression_scale",
      estimated_minority_language_cultural_rights_index: 5.55,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-006",
      name: "Australie/Langues Autochtones — 250 Langues 1788 → 120 Survivantes, 20 Menacées Extinction, AIATSIS Budget & Accord Walmajarri Documentation",
      country: "Australie",
      language_prohibition_forced_assimilation_severity_score: 52.0,
      minority_language_education_media_suppression_scale_score: 51.0,
      cultural_heritage_destruction_appropriation_score: 54.0,
      language_revitalization_legal_recognition_deficit_gap_score: 53.0,
      composite_score: 52.45,
      risk_level: "élevé",
      primary_pattern: "language_revitalization_legal_recognition_deficit_gap",
      estimated_minority_language_cultural_rights_index: 5.25,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-007",
      name: "UNESCO/FEL — Atlas Langues Menacées, Foundation Endangered Languages, Enduring Voices & Réseau Vitalité Linguistique",
      country: "Global",
      language_prohibition_forced_assimilation_severity_score: 27.0,
      minority_language_education_media_suppression_scale_score: 25.0,
      cultural_heritage_destruction_appropriation_score: 28.0,
      language_revitalization_legal_recognition_deficit_gap_score: 26.0,
      composite_score: 26.55,
      risk_level: "modéré",
      primary_pattern: "language_revitalization_legal_recognition_deficit_gap",
      estimated_minority_language_cultural_rights_index: 2.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "MLC-008",
      name: "ONU/DDPA Langues — Déclaration Droits Peuples Autochtones Art.13-16 Langues, PIDESC Art.27 Minorités & UNESCO Conv. Diversité 2005",
      country: "Global",
      language_prohibition_forced_assimilation_severity_score: 4.0,
      minority_language_education_media_suppression_scale_score: 4.0,
      cultural_heritage_destruction_appropriation_score: 4.0,
      language_revitalization_legal_recognition_deficit_gap_score: 4.0,
      composite_score: 4.00,
      risk_level: "faible",
      primary_pattern: "language_prohibition_forced_assimilation_severity",
      estimated_minority_language_cultural_rights_index: 0.40,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/minority-language-cultural-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
