import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[hate-speech-incitement-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[hate-speech-incitement-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Hate Speech Incitement Rights Engine Agent",
  domain: "hate_speech_incitement_rights",
  total_entities: 8,
  avg_composite: 60.95,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Myanmar — Discours Haine Anti-Rohingya, ONU Génocide Intentionnel Documenté, Facebook Vecteur Principal",
    "Russie — Propagande Haineuse LGBT, Agents Étrangers, Incitation Documentée, Cadre Légal Anti-Minorités",
    "Inde — Discours Haine Anti-Musulman Organisé BJP/RSS, Lynchages Mob Documentés, Impunité Institutionnelle",
  ],
  critical_alerts: [
    "Myanmar: minority_targeting_score",
    "Russie: state_sponsored_hate_score",
    "Inde: minority_targeting_score",
    "Éthiopie: minority_targeting_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_hate_speech_incitement_rights_index: 6.10,
  entities: [
    {
      entity_id: "HSR-001",
      name: "Myanmar — Discours Haine Anti-Rohingya, ONU Génocide Intentionnel Documenté, Facebook Vecteur Principal",
      country: "Myanmar",
      state_sponsored_hate_score: 93.0,
      online_incitement_impunity_score: 91.0,
      minority_targeting_score: 95.0,
      legal_protection_gap_score: 92.0,
      composite_score: 92.9,
      risk_level: "critique",
      primary_pattern: "minority_targeting_score",
      estimated_hate_speech_incitement_rights_index: 9.29,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-002",
      name: "Inde — Discours Haine Anti-Musulman Organisé BJP/RSS, Lynchages Mob Documentés, Impunité Institutionnelle",
      country: "Inde",
      state_sponsored_hate_score: 86.0,
      online_incitement_impunity_score: 84.0,
      minority_targeting_score: 88.0,
      legal_protection_gap_score: 83.0,
      composite_score: 85.45,
      risk_level: "critique",
      primary_pattern: "minority_targeting_score",
      estimated_hate_speech_incitement_rights_index: 8.55,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-003",
      name: "Russie — Propagande Haineuse LGBT, Agents Étrangers, Incitation Documentée, Cadre Légal Anti-Minorités",
      country: "Russie",
      state_sponsored_hate_score: 89.0,
      online_incitement_impunity_score: 82.0,
      minority_targeting_score: 84.0,
      legal_protection_gap_score: 87.0,
      composite_score: 85.55,
      risk_level: "critique",
      primary_pattern: "state_sponsored_hate_score",
      estimated_hate_speech_incitement_rights_index: 8.56,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-004",
      name: "Éthiopie — Médias Ethniques Incitation Génocide Tigré/Amhara, Modèle Radio Rwanda 2.0, Impunité Totale",
      country: "Éthiopie",
      state_sponsored_hate_score: 82.0,
      online_incitement_impunity_score: 80.0,
      minority_targeting_score: 85.0,
      legal_protection_gap_score: 80.0,
      composite_score: 81.85,
      risk_level: "critique",
      primary_pattern: "minority_targeting_score",
      estimated_hate_speech_incitement_rights_index: 8.19,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-005",
      name: "Brésil — Bolsonarisme, Discours Haine LGBTQ et Autochtones, Impunité Digitale Documentée",
      country: "Brésil",
      state_sponsored_hate_score: 52.0,
      online_incitement_impunity_score: 55.0,
      minority_targeting_score: 53.0,
      legal_protection_gap_score: 50.0,
      composite_score: 52.85,
      risk_level: "élevé",
      primary_pattern: "online_incitement_impunity_score",
      estimated_hate_speech_incitement_rights_index: 5.29,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-006",
      name: "Pakistan — Blasphème Instrumentalisé, Minorités Chrétiennes et Hindoues Ciblées, Incitation Religieuse Systémique",
      country: "Pakistan",
      state_sponsored_hate_score: 48.0,
      online_incitement_impunity_score: 50.0,
      minority_targeting_score: 55.0,
      legal_protection_gap_score: 52.0,
      composite_score: 51.15,
      risk_level: "élevé",
      primary_pattern: "minority_targeting_score",
      estimated_hate_speech_incitement_rights_index: 5.12,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-007",
      name: "France — Montée Extrême Droite, Discours Haine Anti-Immigration, Lacunes Réglementation Plateformes",
      country: "France",
      state_sponsored_hate_score: 28.0,
      online_incitement_impunity_score: 32.0,
      minority_targeting_score: 30.0,
      legal_protection_gap_score: 27.0,
      composite_score: 29.45,
      risk_level: "modéré",
      primary_pattern: "online_incitement_impunity_score",
      estimated_hate_speech_incitement_rights_index: 2.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "HSR-008",
      name: "Allemagne — NetzDG Loi Contre Discours Haine en Ligne, Meilleure Pratique UE, Sanctions Plateformes Effectives",
      country: "Allemagne",
      state_sponsored_hate_score: 9.0,
      online_incitement_impunity_score: 10.0,
      minority_targeting_score: 8.0,
      legal_protection_gap_score: 9.0,
      composite_score: 9.1,
      risk_level: "faible",
      primary_pattern: "online_incitement_impunity_score",
      estimated_hate_speech_incitement_rights_index: 0.91,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/hate-speech-incitement-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
