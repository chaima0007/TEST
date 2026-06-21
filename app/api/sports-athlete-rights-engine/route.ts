import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sports-athlete-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sports Athlete Rights Engine Agent",
  domain: "sports_athlete_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    doping_corruption_cover_up_scale: 2,
    athlete_exploitation_unpaid_labor_severity: 2,
    sports_sexual_abuse_coach_impunity: 1,
    athlete_free_speech_political_expression_deficit_gap: 3,
  },
  top_risk_entities: [
    "Russie/Chine — Dopage Systématique État, RUSADA Scandale, McLaren Report, Athlètes Femmes Gymnastes Abus & Boycotts Silenciés",
    "Qatar/FIFA — Travailleurs Stades Morts 6 500, Corruption FIFA Sepp Blatter, Athlètes Droits Bafoués & Chaleur Mortelle",
    "USA/NCAA — Athlètes Universitaires Non Payés 5B$/An Revenus, Abus Sexuels Larry Nassar 300 Victimes & NFL CTE Dissimulé",
  ],
  critical_alerts: [
    "Russie/Chine: doping_corruption_cover_up_scale",
    "Qatar/FIFA: athlete_exploitation_unpaid_labor_severity",
    "USA/NCAA: sports_sexual_abuse_coach_impunity",
    "Arabie Saoudite: athlete_free_speech_political_expression_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_sports_athlete_rights_index: 6.14,
  data_sources: [
    "global_athletes_athlete_rights_violations_report",
    "wada_doping_violations_annual_statistics",
    "human_rights_watch_sports_abuse_documentation",
  ],
  entities: [
    {
      id: "SAR-001",
      name: "Russie/Chine — Dopage Systématique État, RUSADA Scandale, McLaren Report, Athlètes Femmes Gymnastes Abus & Boycotts Silenciés",
      country: "Russie/Chine",
      athlete_exploitation_unpaid_labor_severity_score: 95.0,
      doping_corruption_cover_up_scale_score: 93.0,
      sports_sexual_abuse_coach_impunity_score: 92.0,
      athlete_free_speech_political_expression_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "doping_corruption_cover_up_scale",
      estimated_sports_athlete_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-002",
      name: "Qatar/FIFA — Travailleurs Stades Morts 6 500, Corruption FIFA Sepp Blatter, Athlètes Droits Bafoués & Chaleur Mortelle",
      country: "Qatar",
      athlete_exploitation_unpaid_labor_severity_score: 92.0,
      doping_corruption_cover_up_scale_score: 90.0,
      sports_sexual_abuse_coach_impunity_score: 89.0,
      athlete_free_speech_political_expression_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "athlete_exploitation_unpaid_labor_severity",
      estimated_sports_athlete_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-003",
      name: "USA/NCAA — Athlètes Universitaires Non Payés 5B$/An Revenus, Abus Sexuels Larry Nassar 300 Victimes & NFL CTE Dissimulé",
      country: "USA",
      athlete_exploitation_unpaid_labor_severity_score: 89.0,
      doping_corruption_cover_up_scale_score: 87.0,
      sports_sexual_abuse_coach_impunity_score: 86.0,
      athlete_free_speech_political_expression_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "sports_sexual_abuse_coach_impunity",
      estimated_sports_athlete_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-004",
      name: "Arabie Saoudite — Sports Washing Golfs/Boxe, LIV Golf Critiques Tues, Activistes Sportifs Emprisonnés & Femmes Sport Tardif",
      country: "Arabie Saoudite",
      athlete_exploitation_unpaid_labor_severity_score: 86.0,
      doping_corruption_cover_up_scale_score: 84.0,
      sports_sexual_abuse_coach_impunity_score: 83.0,
      athlete_free_speech_political_expression_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "athlete_free_speech_political_expression_deficit_gap",
      estimated_sports_athlete_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-005",
      name: "Chine/IOC — Hong Kong Athlètes Pression, IOC Silence Droits Humains, Nathan Law Exilé & Peng Shuai Disparition",
      country: "Chine",
      athlete_exploitation_unpaid_labor_severity_score: 57.0,
      doping_corruption_cover_up_scale_score: 55.0,
      sports_sexual_abuse_coach_impunity_score: 54.0,
      athlete_free_speech_political_expression_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "athlete_free_speech_political_expression_deficit_gap",
      estimated_sports_athlete_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-006",
      name: "USA/Europe — NIL Student Athletes Inégaux, Contrats Exploiteurs, Black Athletes Protest NFL & Transfer Portal Abus",
      country: "USA/Europe",
      athlete_exploitation_unpaid_labor_severity_score: 54.0,
      doping_corruption_cover_up_scale_score: 52.0,
      sports_sexual_abuse_coach_impunity_score: 51.0,
      athlete_free_speech_political_expression_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "athlete_exploitation_unpaid_labor_severity",
      estimated_sports_athlete_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-007",
      name: "Global Athletes/WADA — Association Athlètes Internationaux, Anti-Dopage Réforme, Droits Représentation & Plateforme Signalement",
      country: "Global",
      athlete_exploitation_unpaid_labor_severity_score: 27.0,
      doping_corruption_cover_up_scale_score: 26.0,
      sports_sexual_abuse_coach_impunity_score: 25.0,
      athlete_free_speech_political_expression_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "doping_corruption_cover_up_scale",
      estimated_sports_athlete_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "SAR-008",
      name: "ONU/CDES — Droit Sport Charte Internationale, Olympisme Droits Humains & SDG 3 Santé Bien-Être",
      country: "Global",
      athlete_exploitation_unpaid_labor_severity_score: 5.0,
      doping_corruption_cover_up_scale_score: 4.0,
      sports_sexual_abuse_coach_impunity_score: 4.0,
      athlete_free_speech_political_expression_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "athlete_free_speech_political_expression_deficit_gap",
      estimated_sports_athlete_rights_index: 0.43,
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
      `${process.env.SWARM_API_URL}/sports-athlete-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
