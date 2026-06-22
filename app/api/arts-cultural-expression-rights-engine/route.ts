import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[arts-cultural-expression-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Arts Cultural Expression Rights Engine Agent",
  domain: "arts_cultural_expression_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    online_creative_content_suppression: 1,
    artist_censorship_imprisonment_severity: 3,
    cultural_institution_state_capture_scale: 2,
    artistic_minority_voice_exclusion_deficit_gap: 2,
  },
  top_risk_entities: [
    "Chine — Ai Weiwei Exilé, Artistes Xinjiang Emprisonnés, Films Censurés 2000+/An & Internet Culturel Filtré",
    "Iran — Rappeurs Exécutés Toomaj Salehi, Cinéastes Jafar Panahi Prison, Femmes Artistes Voile & Concerts Interdits",
    "Russie — Pussy Riot Emprisonnées, Théâtres Fermés Guerre Ukraine, Artistes Exilés 5 000+ & Livres Retirés",
  ],
  critical_alerts: [
    "Chine: online_creative_content_suppression",
    "Iran: artist_censorship_imprisonment_severity",
    "Russie: cultural_institution_state_capture_scale",
    "Arabie Saoudite: artist_censorship_imprisonment_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_arts_cultural_expression_rights_index: 6.14,
  data_sources: [
    "freemuse_state_of_artistic_freedom_annual_report",
    "pen_international_writer_persecution_database",
    "article19_online_expression_censorship_report",
  ],
  entities: [
    {
      id: "ACE-001",
      name: "Chine — Ai Weiwei Exilé, Artistes Xinjiang Emprisonnés, Films Censurés 2000+/An & Internet Culturel Filtré",
      country: "Chine",
      artist_censorship_imprisonment_severity_score: 95.0,
      cultural_institution_state_capture_scale_score: 93.0,
      online_creative_content_suppression_score: 92.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "online_creative_content_suppression",
      estimated_arts_cultural_expression_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-002",
      name: "Iran — Rappeurs Exécutés Toomaj Salehi, Cinéastes Jafar Panahi Prison, Femmes Artistes Voile & Concerts Interdits",
      country: "Iran",
      artist_censorship_imprisonment_severity_score: 92.0,
      cultural_institution_state_capture_scale_score: 90.0,
      online_creative_content_suppression_score: 89.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "artist_censorship_imprisonment_severity",
      estimated_arts_cultural_expression_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-003",
      name: "Russie — Pussy Riot Emprisonnées, Théâtres Fermés Guerre Ukraine, Artistes Exilés 5 000+ & Livres Retirés",
      country: "Russie",
      artist_censorship_imprisonment_severity_score: 89.0,
      cultural_institution_state_capture_scale_score: 87.0,
      online_creative_content_suppression_score: 86.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "cultural_institution_state_capture_scale",
      estimated_arts_cultural_expression_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-004",
      name: "Arabie Saoudite — Vision 2030 Contrôlée, Artistes Critiques Traqués, Cinéma 35 Ans Interdit & Social Media Stars Arrêtés",
      country: "Arabie Saoudite",
      artist_censorship_imprisonment_severity_score: 86.0,
      cultural_institution_state_capture_scale_score: 84.0,
      online_creative_content_suppression_score: 83.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "artist_censorship_imprisonment_severity",
      estimated_arts_cultural_expression_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-005",
      name: "Turquie/Hongrie — Écrivains Procès 301 Code Pénal Insulte Turcité, Théâtres Hongrois Étatisés & Subventions Politisées",
      country: "Turquie/Hongrie",
      artist_censorship_imprisonment_severity_score: 57.0,
      cultural_institution_state_capture_scale_score: 55.0,
      online_creative_content_suppression_score: 54.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "cultural_institution_state_capture_scale",
      estimated_arts_cultural_expression_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-006",
      name: "USA/UK — TikTok Menace Interdiction, DMCA Surcensure, Artistes Noirs Historiquement Effacés & NFT Droits Ambigus",
      country: "USA/UK",
      artist_censorship_imprisonment_severity_score: 54.0,
      cultural_institution_state_capture_scale_score: 52.0,
      online_creative_content_suppression_score: 51.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "artistic_minority_voice_exclusion_deficit_gap",
      estimated_arts_cultural_expression_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-007",
      name: "PEN International/Freemuse — Défense Artistes Emprisonnés, Alertes Violations, Advocacy ONU & Réseau Mondial",
      country: "Global",
      artist_censorship_imprisonment_severity_score: 27.0,
      cultural_institution_state_capture_scale_score: 26.0,
      online_creative_content_suppression_score: 25.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "artist_censorship_imprisonment_severity",
      estimated_arts_cultural_expression_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "ACE-008",
      name: "ONU/Art.27 DUDH — Droit Vie Culturelle, Art.15 DESC Vie Culturelle & UNESCO Convention 2005 Diversité",
      country: "Global",
      artist_censorship_imprisonment_severity_score: 5.0,
      cultural_institution_state_capture_scale_score: 4.0,
      online_creative_content_suppression_score: 4.0,
      artistic_minority_voice_exclusion_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "artistic_minority_voice_exclusion_deficit_gap",
      estimated_arts_cultural_expression_rights_index: 0.43,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/arts-cultural-expression-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
