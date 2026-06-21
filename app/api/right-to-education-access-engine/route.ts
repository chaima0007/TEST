import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-education-access-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right To Education Access Engine Agent",
  domain: "right_to_education_access",
  total_entities: 8,
  avg_composite: 60.38,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    out_of_school_children_crisis_scale: 2,
    girls_education_exclusion_gender_gap: 2,
    conflict_zone_school_destruction_attacks: 2,
    structural_inequality_education_poverty_access: 2,
  },
  top_risk_entities: [
    "Afghanistan/Taliban — Filles Bannies Écoles, 3M Enfants Hors Scolarité, Universités Femmes Fermées & Enseignantes Exclues",
    "Sahel/Mali-Niger-Burkina — Écoles Brûlées Djihadistes, 10 000+ Fermées Conflit, Enseignants Assassinés & IDP Enfants Exclus",
    "Pakistan/Bangladesh — 20M Enfants Hors École, Filles Rurales Mariages Précoces, Madrassas Alternatives & Inondations Écoles",
  ],
  critical_alerts: [
    "Afghanistan/Taliban: girls_education_exclusion_gender_gap",
    "Sahel/Mali-Niger-Burkina: conflict_zone_school_destruction_attacks",
    "Pakistan/Bangladesh: out_of_school_children_crisis_scale",
    "Nigéria/Boko-Haram — Chibok Girls Legacy: girls_education_exclusion_gender_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_right_to_education_access_index: 6.04,
  data_sources: [
    "unicef_out_of_school_children_initiative_2023",
    "unesco_global_education_monitoring_report_2023",
    "global_coalition_protect_education_conflict_2023",
    "human_rights_watch_right_to_education_reports_2023",
  ],
  entities: [
    {
      entity_id: "RTEA-001",
      name: "Afghanistan/Taliban — Filles Bannies Écoles, 3M Enfants Hors Scolarité, Universités Femmes Fermées & Enseignantes Exclues",
      country: "Afghanistan",
      out_of_school_children_crisis_scale_score: 96.0,
      girls_education_exclusion_gender_gap_score: 98.0,
      conflict_zone_school_destruction_attacks_score: 90.0,
      structural_inequality_education_poverty_access_score: 88.0,
      composite_score: 93.65,
      risk_level: "critique",
      primary_pattern: "girls_education_exclusion_gender_gap",
      estimated_right_to_education_access_index: 9.37,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-002",
      name: "Sahel/Mali-Niger-Burkina — Écoles Brûlées Djihadistes, 10 000+ Fermées Conflit, Enseignants Assassinés & IDP Enfants Exclus",
      country: "Sahel",
      out_of_school_children_crisis_scale_score: 91.0,
      girls_education_exclusion_gender_gap_score: 89.0,
      conflict_zone_school_destruction_attacks_score: 94.0,
      structural_inequality_education_poverty_access_score: 87.0,
      composite_score: 90.65,
      risk_level: "critique",
      primary_pattern: "conflict_zone_school_destruction_attacks",
      estimated_right_to_education_access_index: 9.07,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-003",
      name: "Pakistan/Bangladesh — 20M Enfants Hors École, Filles Rurales Mariages Précoces, Madrassas Alternatives & Inondations Écoles",
      country: "Pakistan/Bangladesh",
      out_of_school_children_crisis_scale_score: 88.0,
      girls_education_exclusion_gender_gap_score: 86.0,
      conflict_zone_school_destruction_attacks_score: 80.0,
      structural_inequality_education_poverty_access_score: 85.0,
      composite_score: 85.25,
      risk_level: "critique",
      primary_pattern: "out_of_school_children_crisis_scale",
      estimated_right_to_education_access_index: 8.53,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-004",
      name: "Nigéria/Boko-Haram — Chibok Girls Legacy, Nordeste Écoles Fermées, ISWA Attaques & Millions Déplacés Sans Accès",
      country: "Nigéria",
      out_of_school_children_crisis_scale_score: 85.0,
      girls_education_exclusion_gender_gap_score: 84.0,
      conflict_zone_school_destruction_attacks_score: 86.0,
      structural_inequality_education_poverty_access_score: 83.0,
      composite_score: 84.6,
      risk_level: "critique",
      primary_pattern: "girls_education_exclusion_gender_gap",
      estimated_right_to_education_access_index: 8.46,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-005",
      name: "Yémen/Syrie — Décennie Conflit, 50% Écoles Endommagées, Enseignants Impayés 3 Ans & Génération Perdue Éducation",
      country: "Yémen/Syrie",
      out_of_school_children_crisis_scale_score: 56.0,
      girls_education_exclusion_gender_gap_score: 54.0,
      conflict_zone_school_destruction_attacks_score: 58.0,
      structural_inequality_education_poverty_access_score: 52.0,
      composite_score: 55.25,
      risk_level: "élevé",
      primary_pattern: "conflict_zone_school_destruction_attacks",
      estimated_right_to_education_access_index: 5.53,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-006",
      name: "Amérique Centrale/Haïti — Gangs Écoles Fermées, Exode Rural, Travail Enfants Agriculture & Coût Indirect Scolarisation",
      country: "Amérique Centrale/Haïti",
      out_of_school_children_crisis_scale_score: 53.0,
      girls_education_exclusion_gender_gap_score: 51.0,
      conflict_zone_school_destruction_attacks_score: 49.0,
      structural_inequality_education_poverty_access_score: 55.0,
      composite_score: 52.35,
      risk_level: "élevé",
      primary_pattern: "structural_inequality_education_poverty_access",
      estimated_right_to_education_access_index: 5.24,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-007",
      name: "UNICEF/UNESCO — Coalitions Éducation Crise, Rapports Exclusion Mondiale, Programmes Rattrapage & Fonds Urgence",
      country: "Global",
      out_of_school_children_crisis_scale_score: 26.0,
      girls_education_exclusion_gender_gap_score: 25.0,
      conflict_zone_school_destruction_attacks_score: 24.0,
      structural_inequality_education_poverty_access_score: 27.0,
      composite_score: 25.65,
      risk_level: "modéré",
      primary_pattern: "structural_inequality_education_poverty_access",
      estimated_right_to_education_access_index: 2.57,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "RTEA-008",
      name: "ONU/Art.26 DUDH — Droit Éducation Universel, Convention Enfant Art.28, SDG 4 & Protocole Facultatif DESC",
      country: "Global",
      out_of_school_children_crisis_scale_score: 5.0,
      girls_education_exclusion_gender_gap_score: 4.0,
      conflict_zone_school_destruction_attacks_score: 4.0,
      structural_inequality_education_poverty_access_score: 5.0,
      composite_score: 4.55,
      risk_level: "faible",
      primary_pattern: "out_of_school_children_crisis_scale",
      estimated_right_to_education_access_index: 0.46,
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
      `${process.env.SWARM_API_URL}/right-to-education-access-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
