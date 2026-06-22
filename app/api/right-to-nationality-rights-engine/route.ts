import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-nationality-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-nationality-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Right To Nationality Rights Engine Agent",
  domain: "right_to_nationality_rights",
  total_entities: 8,
  avg_composite: 60.11,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Myanmar — Apatridie Rohingyas, dépossession nationale systématique",
    "Koweït — Bidouns : 100k+ apatrides sans nationalité depuis 60 ans",
    "République dominicaine — Dénationalisation rétroactive des descendants haïtiens",
  ],
  critical_alerts: [
    "Myanmar: Rohingya statelessness — systematic nationality deprivation since 1982",
    "Koweït: Bidoun population — 100k+ stateless for 60 years",
    "République dominicaine: Retroactive denationalization of Haitian descendants",
    "Éthiopie: Ethnicity-based nationality stripping during conflicts",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_nationality_rights_index: 6.01,
  entities: [
    {
      entity_id: "RTN-001",
      name: "Myanmar — Apatridie Rohingyas, dépossession nationale systématique",
      country: "Myanmar",
      nationality_deprivation_score: 99.0,
      discriminatory_nationality_law_score: 98.0,
      stateless_adult_population_score: 97.0,
      naturalization_barrier_score: 99.0,
      composite_score: 98.25,
      risk_level: "critique",
      primary_pattern: "Rohingya statelessness — systematic nationality deprivation since 1982",
      estimated_right_to_nationality_rights_index: 9.83,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-002",
      name: "Koweït — Bidouns : 100k+ apatrides sans nationalité depuis 60 ans",
      country: "Koweït",
      nationality_deprivation_score: 88.0,
      discriminatory_nationality_law_score: 85.0,
      stateless_adult_population_score: 90.0,
      naturalization_barrier_score: 92.0,
      composite_score: 88.65,
      risk_level: "critique",
      primary_pattern: "Bidoun population — 100k+ stateless for 60 years",
      estimated_right_to_nationality_rights_index: 8.87,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-003",
      name: "République dominicaine — Dénationalisation rétroactive descendants haïtiens",
      country: "République dominicaine",
      nationality_deprivation_score: 78.0,
      discriminatory_nationality_law_score: 80.0,
      stateless_adult_population_score: 72.0,
      naturalization_barrier_score: 75.0,
      composite_score: 76.45,
      risk_level: "critique",
      primary_pattern: "Retroactive denationalization of Haitian descendants",
      estimated_right_to_nationality_rights_index: 7.65,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-004",
      name: "Éthiopie — Dépossession nationale ethnique lors des conflits",
      country: "Éthiopie",
      nationality_deprivation_score: 68.0,
      discriminatory_nationality_law_score: 65.0,
      stateless_adult_population_score: 62.0,
      naturalization_barrier_score: 60.0,
      composite_score: 64.25,
      risk_level: "critique",
      primary_pattern: "Ethnicity-based nationality stripping during conflicts",
      estimated_right_to_nationality_rights_index: 6.43,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-005",
      name: "Liban — Apatridie enfants nés de pères étrangers, discrimination genre",
      country: "Liban",
      nationality_deprivation_score: 55.0,
      discriminatory_nationality_law_score: 58.0,
      stateless_adult_population_score: 48.0,
      naturalization_barrier_score: 52.0,
      composite_score: 53.35,
      risk_level: "élevé",
      primary_pattern: "Gender-based nationality discrimination & stateless children",
      estimated_right_to_nationality_rights_index: 5.34,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-006",
      name: "Thaïlande — Apatridie montagnards, enregistrement refusé",
      country: "Thaïlande",
      nationality_deprivation_score: 45.0,
      discriminatory_nationality_law_score: 42.0,
      stateless_adult_population_score: 46.0,
      naturalization_barrier_score: 44.0,
      composite_score: 44.3,
      risk_level: "élevé",
      primary_pattern: "Hill tribe statelessness & denied civil registration",
      estimated_right_to_nationality_rights_index: 4.43,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-007",
      name: "Lettonie — Apatrides post-soviétiques, naturalisation lente",
      country: "Lettonie",
      nationality_deprivation_score: 28.0,
      discriminatory_nationality_law_score: 30.0,
      stateless_adult_population_score: 32.0,
      naturalization_barrier_score: 26.0,
      composite_score: 29.15,
      risk_level: "modéré",
      primary_pattern: "Post-Soviet stateless residents, slow naturalization",
      estimated_right_to_nationality_rights_index: 2.92,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTN-008",
      name: "Portugal — Droit du sol robuste, naturalisation accessible",
      country: "Portugal",
      nationality_deprivation_score: 6.0,
      discriminatory_nationality_law_score: 5.0,
      stateless_adult_population_score: 7.0,
      naturalization_barrier_score: 4.0,
      composite_score: 5.65,
      risk_level: "faible",
      primary_pattern: "Strong jus soli, accessible naturalization, low statelessness",
      estimated_right_to_nationality_rights_index: 0.57,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-nationality-rights-engine`, {
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
