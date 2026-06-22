import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[border-crossing-detention-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Border Crossing Detention Rights Engine Agent",
  domain: "border_crossing_detention_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    family_separation_unaccompanied_minors: 1,
    border_violence_pushback_death_severity: 3,
    immigration_detention_conditions_duration_scale: 2,
    stateless_person_documentation_legal_aid_deficit_gap: 2,
  },
  top_risk_entities: [
    "USA/Mexique — 853 Morts Frontière 2022, Titre 42 Expulsions, Séparation Familles 5 000+, CBP Violence & Razor Wire Texas",
    "UE/Méditerranée — 30 000 Morts Depuis 1993, Pushbacks Croatie/Grèce Documentés, Frontex Complicité & Lampedusa Crise",
    "Libye — Centres Détention Torture ONU Documentée, Coast Guard Financement EU, Retours Forcés & Conditions Dégradantes",
  ],
  critical_alerts: [
    "USA/Mexique: family_separation_unaccompanied_minors",
    "UE/Méditerranée: border_violence_pushback_death_severity",
    "Libye: immigration_detention_conditions_duration_scale",
    "Australie: immigration_detention_conditions_duration_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_border_crossing_detention_rights_index: 6.14,
  data_sources: [
    "unhcr_mediterranean_sea_crossing_deaths_database",
    "border_violence_monitoring_network_report",
    "human_rights_watch_immigration_detention_conditions",
  ],
  entities: [
    {
      id: "BCD-001",
      name: "USA/Mexique — 853 Morts Frontière 2022, Titre 42 Expulsions, Séparation Familles 5 000+, CBP Violence & Razor Wire Texas",
      country: "USA/Mexique",
      border_violence_pushback_death_severity_score: 95.0,
      immigration_detention_conditions_duration_scale_score: 93.0,
      family_separation_unaccompanied_minors_score: 92.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "family_separation_unaccompanied_minors",
      estimated_border_crossing_detention_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-002",
      name: "UE/Méditerranée — 30 000 Morts Depuis 1993, Pushbacks Croatie/Grèce Documentés, Frontex Complicité & Lampedusa Crise",
      country: "UE/Méditerranée",
      border_violence_pushback_death_severity_score: 92.0,
      immigration_detention_conditions_duration_scale_score: 90.0,
      family_separation_unaccompanied_minors_score: 89.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "border_violence_pushback_death_severity",
      estimated_border_crossing_detention_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-003",
      name: "Libye — Centres Détention Torture ONU Documentée, Coast Guard Financement EU, Retours Forcés & Conditions Dégradantes",
      country: "Libye",
      border_violence_pushback_death_severity_score: 89.0,
      immigration_detention_conditions_duration_scale_score: 87.0,
      family_separation_unaccompanied_minors_score: 86.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "immigration_detention_conditions_duration_scale",
      estimated_border_crossing_detention_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-004",
      name: "Australie — Nauru Détention Offshore Indéfinie, Manus Island Fermé Tard, Suicides Détenus & Medical Transfers Refusés",
      country: "Australie",
      border_violence_pushback_death_severity_score: 86.0,
      immigration_detention_conditions_duration_scale_score: 84.0,
      family_separation_unaccompanied_minors_score: 83.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "immigration_detention_conditions_duration_scale",
      estimated_border_crossing_detention_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-005",
      name: "UK/France — Channel Deaths 2022 Record 46, Pushbacks Illégaux Dunkerque, Rwanda Plan & Small Boats Act 2023",
      country: "UK/France",
      border_violence_pushback_death_severity_score: 57.0,
      immigration_detention_conditions_duration_scale_score: 55.0,
      family_separation_unaccompanied_minors_score: 54.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "border_violence_pushback_death_severity",
      estimated_border_crossing_detention_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-006",
      name: "Turquie/Balkans — Route Bosnie Violences, Détention Sans Limite Légale, Mineurs Non-Accompagnés Perdus & Corruption Gardes",
      country: "Turquie/Balkans",
      border_violence_pushback_death_severity_score: 54.0,
      immigration_detention_conditions_duration_scale_score: 52.0,
      family_separation_unaccompanied_minors_score: 51.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "stateless_person_documentation_legal_aid_deficit_gap",
      estimated_border_crossing_detention_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-007",
      name: "UNHCR/MSF — Monitoring Frontières, Sauvetages Méditerranée, Dossiers Décès & Advocacy Standards Détention",
      country: "Global",
      border_violence_pushback_death_severity_score: 27.0,
      immigration_detention_conditions_duration_scale_score: 26.0,
      family_separation_unaccompanied_minors_score: 25.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "border_violence_pushback_death_severity",
      estimated_border_crossing_detention_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "BCD-008",
      name: "ONU/Convention 1951 Art.31 — Non-Pénalisation Entrée Irrégulière, Standards Détention UNHCR & SDG 10.7 Migration",
      country: "Global",
      border_violence_pushback_death_severity_score: 5.0,
      immigration_detention_conditions_duration_scale_score: 4.0,
      family_separation_unaccompanied_minors_score: 4.0,
      stateless_person_documentation_legal_aid_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "stateless_person_documentation_legal_aid_deficit_gap",
      estimated_border_crossing_detention_rights_index: 0.43,
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
      `${process.env.SWARM_API_URL}/border-crossing-detention-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
