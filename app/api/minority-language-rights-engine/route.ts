import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[minority-language-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Minority Language Rights Engine Agent",
  domain: "minority_language_rights",
  total_entities: 8,
  avg_composite: 56.79,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { legal_recognition_absence: 5, education_denial: 1, media_cultural_erasure: 2 },
  top_risk_entities: [
    "Chine/Ouïghours/Tibétains — Sinicisation Forcée, Internats & Effacement Linguistique Systémique",
    "Turquie/Kurdes — 40 Ans Interdiction Kurde, 20M Locuteurs & Répression Culturelle",
    "Russie/Langues Autochtones — Russification, 100+ Langues Menacées & Réforme 2018",
  ],
  critical_alerts: [
    "Chine/Ouïghours/Tibétains: legal_recognition_absence",
    "Turquie/Kurdes: legal_recognition_absence",
    "Russie/Langues Autochtones: education_denial",
    "France/Langues Régionales: legal_recognition_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_minority_language_rights_index: 5.68,
  data_sources: [
    "unesco_atlas_of_worlds_languages_in_danger_online_edition",
    "council_of_europe_ecrml_monitoring_reports_by_committee_of_experts",
    "un_special_rapporteur_minority_issues_country_reports",
  ],
  entities: [
    {
      entity_id: "ML-001",
      name: "Chine/Ouïghours/Tibétains — Sinicisation Forcée, Internats & Effacement Linguistique Systémique",
      country: "Asie du Nord-Est",
      composite_score: 93.65,
      language_suppression_score: 90.0,
      education_denial_score: 95.0,
      legal_recognition_absence_score: 98.0,
      media_cultural_erasure_score: 92.0,
      risk_level: "critique",
      primary_pattern: "legal_recognition_absence",
      estimated_minority_language_rights_index: 9.37,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-002",
      name: "Turquie/Kurdes — 40 Ans Interdiction Kurde, 20M Locuteurs & Répression Culturelle",
      country: "Moyen-Orient",
      composite_score: 83.85,
      language_suppression_score: 82.0,
      education_denial_score: 85.0,
      legal_recognition_absence_score: 88.0,
      media_cultural_erasure_score: 80.0,
      risk_level: "critique",
      primary_pattern: "legal_recognition_absence",
      estimated_minority_language_rights_index: 8.39,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-003",
      name: "Russie/Langues Autochtones — Russification, 100+ Langues Menacées & Réforme 2018",
      country: "Europe de l'Est",
      composite_score: 76.10,
      language_suppression_score: 72.0,
      education_denial_score: 78.0,
      legal_recognition_absence_score: 80.0,
      media_cultural_erasure_score: 75.0,
      risk_level: "critique",
      primary_pattern: "education_denial",
      estimated_minority_language_rights_index: 7.61,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-004",
      name: "France/Langues Régionales — Jacobinisme, Bretons/Occitans & Effacement Institutionnel",
      country: "Europe Occidentale",
      composite_score: 66.00,
      language_suppression_score: 60.0,
      education_denial_score: 68.0,
      legal_recognition_absence_score: 72.0,
      media_cultural_erasure_score: 65.0,
      risk_level: "critique",
      primary_pattern: "legal_recognition_absence",
      estimated_minority_language_rights_index: 6.60,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-005",
      name: "Inde/Langues Tribales — 780 Langues, Adivasis & Disparition Accélérée",
      country: "Asie du Sud",
      composite_score: 51.35,
      language_suppression_score: 52.0,
      education_denial_score: 48.0,
      legal_recognition_absence_score: 55.0,
      media_cultural_erasure_score: 50.0,
      risk_level: "élevé",
      primary_pattern: "legal_recognition_absence",
      estimated_minority_language_rights_index: 5.14,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-006",
      name: "USA/Langues Autochtones — 175 Langues en Danger, Pensionnats & Native American Languages Act",
      country: "Amérique du Nord",
      composite_score: 50.60,
      language_suppression_score: 45.0,
      education_denial_score: 50.0,
      legal_recognition_absence_score: 60.0,
      media_cultural_erasure_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "legal_recognition_absence",
      estimated_minority_language_rights_index: 5.06,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-007",
      name: "UE/ECRML — Charte Langues Régionales, CONFINTEA & 60M Locuteurs Minoritaires",
      country: "Europe",
      composite_score: 28.40,
      language_suppression_score: 25.0,
      education_denial_score: 30.0,
      legal_recognition_absence_score: 28.0,
      media_cultural_erasure_score: 32.0,
      risk_level: "modéré",
      primary_pattern: "media_cultural_erasure",
      estimated_minority_language_rights_index: 2.84,
      last_updated: "2026-06-20",
    },
    {
      entity_id: "ML-008",
      name: "ONU/PIDCP Art.27 — Droits Minorités Linguistiques, DNUDPA & UNESCO Atlas",
      country: "Global",
      composite_score: 4.40,
      language_suppression_score: 4.0,
      education_denial_score: 5.0,
      legal_recognition_absence_score: 3.0,
      media_cultural_erasure_score: 6.0,
      risk_level: "faible",
      primary_pattern: "media_cultural_erasure",
      estimated_minority_language_rights_index: 0.44,
      last_updated: "2026-06-20",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/minority-language-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
