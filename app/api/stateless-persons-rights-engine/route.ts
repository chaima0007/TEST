import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[stateless-persons-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Stateless Persons Rights Engine Agent",
  domain: "stateless_persons_rights",
  total_entities: 8,
  avg_composite: 60.94,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    statelessness_documentation_denial_severity: 3,
    birth_registration_nationality_access_gap: 2,
    arbitrary_detention_deportation_stateless_scale: 2,
    stateless_children_education_rights_deficit_gap: 1,
  },
  top_risk_entities: [
    "Myanmar/Rohingya — Apatridie Légale 1982, Carte Identité NV Refusée, Camps Concentration & Génocide Documentation",
    "Koweït/Bidoun — 100 000 Apatrides Bidoun Légaux, Pas Passeports, Enfants Non Enregistrés & Discrimination Systémique",
    "Éthiopie/Érythrée — Rapatriés Déchus Citoyenneté 1998, Binationaux Expulsés & Générations Apatrides Conflits",
  ],
  critical_alerts: [
    "Myanmar/Rohingya: statelessness_documentation_denial_severity",
    "Koweït/Bidoun: birth_registration_nationality_access_gap",
    "Éthiopie/Érythrée: arbitrary_detention_deportation_stateless_scale",
    "Dom. Rep./Haïtiens: statelessness_documentation_denial_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_stateless_persons_rights_index: 6.09,
  data_sources: [
    "unhcr_statelessness_global_report",
    "european_network_on_statelessness_report",
    "human_rights_watch_rohingya_documentation",
  ],
  entities: [
    {
      id: "SPR-001",
      name: "Myanmar/Rohingya — Apatridie Légale 1982, Carte Identité NV Refusée, Camps Concentration & Génocide Documentation",
      country: "Myanmar",
      statelessness_documentation_denial_severity_score: 95.0,
      arbitrary_detention_deportation_stateless_scale_score: 93.0,
      birth_registration_nationality_access_gap_score: 92.0,
      stateless_children_education_rights_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "statelessness_documentation_denial_severity",
      estimated_stateless_persons_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-002",
      name: "Koweït/Bidoun — 100 000 Apatrides Bidoun Légaux, Pas Passeports, Enfants Non Enregistrés & Discrimination Systémique",
      country: "Koweït",
      statelessness_documentation_denial_severity_score: 91.0,
      arbitrary_detention_deportation_stateless_scale_score: 89.0,
      birth_registration_nationality_access_gap_score: 90.0,
      stateless_children_education_rights_deficit_gap_score: 88.0,
      composite_score: 89.65,
      risk_level: "critique",
      primary_pattern: "birth_registration_nationality_access_gap",
      estimated_stateless_persons_rights_index: 8.97,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-003",
      name: "Éthiopie/Érythrée — Rapatriés Déchus Citoyenneté 1998, Binationaux Expulsés & Générations Apatrides Conflits",
      country: "Éthiopie",
      statelessness_documentation_denial_severity_score: 87.0,
      arbitrary_detention_deportation_stateless_scale_score: 86.0,
      birth_registration_nationality_access_gap_score: 85.0,
      stateless_children_education_rights_deficit_gap_score: 84.0,
      composite_score: 85.65,
      risk_level: "critique",
      primary_pattern: "arbitrary_detention_deportation_stateless_scale",
      estimated_stateless_persons_rights_index: 8.57,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-004",
      name: "Dom. Rep./Haïtiens — Arrêt 168-13 Rétroactif 1929, 200k Stateless Haïtiano-Dominicains & Registres Refus",
      country: "Rép. Dominicaine",
      statelessness_documentation_denial_severity_score: 84.0,
      arbitrary_detention_deportation_stateless_scale_score: 82.0,
      birth_registration_nationality_access_gap_score: 83.0,
      stateless_children_education_rights_deficit_gap_score: 81.0,
      composite_score: 82.65,
      risk_level: "critique",
      primary_pattern: "statelessness_documentation_denial_severity",
      estimated_stateless_persons_rights_index: 8.27,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-005",
      name: "Thaïlande/Minorités — Tribus Montagnardes Apatrides, 480 000 Sans Nationalité, Travail Enfant & Accès Éducation Refusé",
      country: "Thaïlande",
      statelessness_documentation_denial_severity_score: 56.0,
      arbitrary_detention_deportation_stateless_scale_score: 54.0,
      birth_registration_nationality_access_gap_score: 53.0,
      stateless_children_education_rights_deficit_gap_score: 55.0,
      composite_score: 54.55,
      risk_level: "élevé",
      primary_pattern: "stateless_children_education_rights_deficit_gap",
      estimated_stateless_persons_rights_index: 5.46,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-006",
      name: "Europe/Roms — Roms Apatrides Est-Europe, Enregistrement Naissance Refus, Discrimination Institutionnelle & Expulsions Massives",
      country: "Europe",
      statelessness_documentation_denial_severity_score: 52.0,
      arbitrary_detention_deportation_stateless_scale_score: 51.0,
      birth_registration_nationality_access_gap_score: 53.0,
      stateless_children_education_rights_deficit_gap_score: 50.0,
      composite_score: 51.6,
      risk_level: "élevé",
      primary_pattern: "birth_registration_nationality_access_gap",
      estimated_stateless_persons_rights_index: 5.16,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-007",
      name: "UNHCR/ENS — #IBelong 2024-2024, European Network on Statelessness, Mesures Réduction & Procédures Détermination Apatridie",
      country: "Global",
      statelessness_documentation_denial_severity_score: 27.0,
      arbitrary_detention_deportation_stateless_scale_score: 26.0,
      birth_registration_nationality_access_gap_score: 25.0,
      stateless_children_education_rights_deficit_gap_score: 28.0,
      composite_score: 26.45,
      risk_level: "modéré",
      primary_pattern: "statelessness_documentation_denial_severity",
      estimated_stateless_persons_rights_index: 2.65,
      last_updated: "2026-06-21",
    },
    {
      id: "SPR-008",
      name: "ONU/Conv 1954 — Convention Apatridie 1954 & 1961, UNHCR Mandat, Art.1 Définition & Protocole Réduction Apatridie",
      country: "Global",
      statelessness_documentation_denial_severity_score: 4.0,
      arbitrary_detention_deportation_stateless_scale_score: 4.0,
      birth_registration_nationality_access_gap_score: 4.0,
      stateless_children_education_rights_deficit_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "arbitrary_detention_deportation_stateless_scale",
      estimated_stateless_persons_rights_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/stateless-persons-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
