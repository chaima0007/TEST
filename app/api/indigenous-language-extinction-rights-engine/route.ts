import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-language-extinction-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "indigenous_language_extinction_rights_engine",
  domain: "indigenous_language_extinction_rights",
  total_entities: 8,
  avg_composite: 63.08,
  confidence_score: 0.89,
  accent: "#b45309",
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    speakers_decline: 4,
    state_erasure_policy: 2,
    digital_exclusion: 1,
    revitalization_deficit: 1,
  },
  top_risk_entities: [
    { id: "ILE-002", name: "Brésil Amazonie — 180 Langues Isolées, Déforestation Culturicide", score: 90.6, risk: "critique" },
    { id: "ILE-003", name: "Sibérie Russie — 30 Langues <100 Locuteurs, Russification Forcée", score: 90.55, risk: "critique" },
    { id: "ILE-004", name: "Chine — Tibétain & Ouïghour, Politique Mandarin Forcé", score: 89.55, risk: "critique" },
  ],
  critical_alerts: [
    "ILE-001: Papouasie-Nouvelle-Guinée — 840 Langues, 200 En Extinction Critique — composite 89.35",
    "ILE-002: Brésil Amazonie — 180 Langues Isolées — composite 90.60",
    "ILE-003: Sibérie Russie — 30 Langues <100 Locuteurs — composite 90.55",
    "ILE-004: Chine — Tibétain & Ouïghour, Mandarin Forcé — composite 89.55",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_indigenous_language_extinction_index: 6.31,
  data_sources: [
    "ethnologue_endangered_languages_2024",
    "unesco_atlas_worlds_languages_danger_2023",
    "survival_international_tribal_peoples_2024",
    "un_permanent_forum_indigenous_issues_2023",
  ],
  entities: [
    {
      id: "ILE-001",
      name: "Papouasie-Nouvelle-Guinée — 840 Langues, 200 En Extinction Critique",
      country: "Papouasie-Nouvelle-Guinée",
      language_speakers_decline_velocity_score: 89,
      state_policy_cultural_erasure_score: 85,
      digital_exclusion_endangered_language_score: 92,
      revitalization_resource_deficit_score: 90,
      composite_score: 89.35,
      risk_level: "critique",
      primary_pattern: "840 langues dont 200 menacées, politique scolaire anglais-tok pisin, 0 ressources numériques langues minoritaires",
      estimated_indigenous_language_extinction_index: 8.93,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-002",
      name: "Brésil Amazonie — 180 Langues Isolées, Déforestation Culturicide",
      country: "Brésil",
      language_speakers_decline_velocity_score: 93,
      state_policy_cultural_erasure_score: 88,
      digital_exclusion_endangered_language_score: 90,
      revitalization_resource_deficit_score: 91,
      composite_score: 90.6,
      risk_level: "critique",
      primary_pattern: "180 langues amazoniennes, 50 locuteurs uniques, déforestation détruit communautés, FUNAI sous-financée",
      estimated_indigenous_language_extinction_index: 9.06,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-003",
      name: "Sibérie Russie — 30 Langues <100 Locuteurs, Russification Forcée",
      country: "Russie",
      language_speakers_decline_velocity_score: 94,
      state_policy_cultural_erasure_score: 92,
      digital_exclusion_endangered_language_score: 88,
      revitalization_resource_deficit_score: 89,
      composite_score: 90.55,
      risk_level: "critique",
      primary_pattern: "Nganassane 200 locuteurs, Ket 200 locuteurs, loi 2018 rend enseignement langues autochtones facultatif",
      estimated_indigenous_language_extinction_index: 9.06,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-004",
      name: "Chine — Tibétain & Ouïghour, Politique Mandarin Forcé",
      country: "Chine",
      language_speakers_decline_velocity_score: 87,
      state_policy_cultural_erasure_score: 95,
      digital_exclusion_endangered_language_score: 91,
      revitalization_resource_deficit_score: 86,
      composite_score: 89.55,
      risk_level: "critique",
      primary_pattern: "Écoles tibétaines internat séparent enfants parents, classes ouïghours remplacées mandarin, 100+ langues minoritaires effacées",
      estimated_indigenous_language_extinction_index: 8.96,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-005",
      name: "Australie — Langues Aborigènes, 90% Perdues Depuis Colonisation",
      country: "Australie",
      language_speakers_decline_velocity_score: 58,
      state_policy_cultural_erasure_score: 52,
      digital_exclusion_endangered_language_score: 55,
      revitalization_resource_deficit_score: 60,
      composite_score: 56.4,
      risk_level: "élevé",
      primary_pattern: "250 langues → 120 actives, 13 avec enfants locuteurs, financement AIATSIS insuffisant malgré Stolen Generations excuse",
      estimated_indigenous_language_extinction_index: 5.64,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-006",
      name: "Mexique — Langues Mayas & Nahuas, Urbanisation Accélère Déclin",
      country: "Mexique",
      language_speakers_decline_velocity_score: 55,
      state_policy_cultural_erasure_score: 48,
      digital_exclusion_endangered_language_score: 58,
      revitalization_resource_deficit_score: 54,
      composite_score: 54.25,
      risk_level: "élevé",
      primary_pattern: "68 langues nationales, exode rural accélère, INALI sous-doté, jeunes abandonnent langue pour espagnol mobile",
      estimated_indigenous_language_extinction_index: 5.42,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-007",
      name: "Canada — Langues Premières Nations, TRC & Financement Partiel",
      country: "Canada",
      language_speakers_decline_velocity_score: 28,
      state_policy_cultural_erasure_score: 24,
      digital_exclusion_endangered_language_score: 30,
      revitalization_resource_deficit_score: 26,
      composite_score: 27.3,
      risk_level: "modéré",
      primary_pattern: "Loi langues autochtones 2019 adoptée, 500M$ financement limité, Cri & Inuktitut stabilisés, Loi TRC en attente",
      estimated_indigenous_language_extinction_index: 2.73,
      last_updated: "2026-06-21",
    },
    {
      id: "ILE-008",
      name: "Nouvelle-Zélande — Te Reo Māori, Revitalisation Succès Mondial",
      country: "Nouvelle-Zélande",
      language_speakers_decline_velocity_score: 7,
      state_policy_cultural_erasure_score: 5,
      digital_exclusion_endangered_language_score: 8,
      revitalization_resource_deficit_score: 6,
      composite_score: 6.65,
      risk_level: "faible",
      primary_pattern: "Langue officielle NZ, immersion Kura Kaupapa, TVNZ Māori chaîne nationale, 185K locuteurs +40% 2006-2023",
      estimated_indigenous_language_extinction_index: 0.67,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-language-extinction-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
