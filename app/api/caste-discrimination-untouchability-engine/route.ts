import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[caste-discrimination-untouchability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Caste Discrimination Untouchability Engine Agent",
  domain: "caste_discrimination_untouchability",
  total_entities: 8,
  avg_composite: 61.43,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    caste_based_violence_atrocity_severity: 3,
    untouchability_practice_occupation_segregation_scale: 2,
    intercaste_marriage_honor_violence: 1,
    caste_affirmative_action_legal_protection_deficit_gap: 2,
  },
  top_risk_entities: ["CDU-001", "CDU-002", "CDU-003"],
  critical_alerts: [
    "CDU-001 (Inde/Dalits): composite=93.55 — caste_based_violence_atrocity_severity",
    "CDU-002 (Népal/Dalit): composite=90.30 — untouchability_practice_occupation_segregation_scale",
    "CDU-003 (Pakistan/Scheduled): composite=86.55 — caste_based_violence_atrocity_severity",
    "CDU-004 (Sri Lanka/Rodiya): composite=82.60 — intercaste_marriage_honor_violence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_caste_discrimination_untouchability_index: 6.14,
  data_sources: [
    "international_dalit_solidarity_network_report",
    "human_rights_watch_caste_discrimination_report",
    "un_cerd_descent_discrimination_report",
  ],
  entities: [
    {
      entity_id: "CDU-001",
      name: "Inde/Dalits — 165M Dalits Discrimination Systémique, 50 000 Atrocités/An PoA, Femmes Dalits 4× Viol & Manuels Scolaires Caste",
      country: "Inde",
      caste_based_violence_atrocity_severity_score: 95.0,
      untouchability_practice_occupation_segregation_scale_score: 93.0,
      intercaste_marriage_honor_violence_score: 92.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 94.0,
      composite_score: 93.55,
      risk_level: "critique",
      primary_pattern: "caste_based_violence_atrocity_severity",
      estimated_caste_discrimination_untouchability_index: 9.36,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-002",
      name: "Népal/Dalit — Untouchability 1963 Formellement Aboli, Mariage Intercaste Violence 2000+ Cas/An, Caste Publique Affichée & Dalits Temples Interdits",
      country: "Népal",
      caste_based_violence_atrocity_severity_score: 91.0,
      untouchability_practice_occupation_segregation_scale_score: 92.0,
      intercaste_marriage_honor_violence_score: 88.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 90.0,
      composite_score: 90.30,
      risk_level: "critique",
      primary_pattern: "untouchability_practice_occupation_segregation_scale",
      estimated_caste_discrimination_untouchability_index: 9.03,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-003",
      name: "Pakistan/Scheduled — Chrétiens-Hindous Sanitation Forcés, Travail Bonded 57% SC, Blasphème Dalits Ciblés & Mariages Forcés Minorités",
      country: "Pakistan",
      caste_based_violence_atrocity_severity_score: 87.0,
      untouchability_practice_occupation_segregation_scale_score: 85.0,
      intercaste_marriage_honor_violence_score: 88.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 86.0,
      composite_score: 86.55,
      risk_level: "critique",
      primary_pattern: "caste_based_violence_atrocity_severity",
      estimated_caste_discrimination_untouchability_index: 8.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-004",
      name: "Sri Lanka/Rodiya — Castes Inférieures Rodiya Marginalisation, Système Jati Bouddhisme, Discrimination Emploi & Intermariage Violence",
      country: "Sri Lanka",
      caste_based_violence_atrocity_severity_score: 83.0,
      untouchability_practice_occupation_segregation_scale_score: 82.0,
      intercaste_marriage_honor_violence_score: 84.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 81.0,
      composite_score: 82.60,
      risk_level: "critique",
      primary_pattern: "intercaste_marriage_honor_violence",
      estimated_caste_discrimination_untouchability_index: 8.26,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-005",
      name: "Japon/Burakumin — 1M Burakumin Discrimination Cachée, Bases Données Illégales Vente, Quartiers Évités & Mariage Refusé Enquêteurs",
      country: "Japon",
      caste_based_violence_atrocity_severity_score: 56.0,
      untouchability_practice_occupation_segregation_scale_score: 54.0,
      intercaste_marriage_honor_violence_score: 55.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 57.0,
      composite_score: 55.45,
      risk_level: "élevé",
      primary_pattern: "untouchability_practice_occupation_segregation_scale",
      estimated_caste_discrimination_untouchability_index: 5.55,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-006",
      name: "Afrique/Ostracisés — Osu Igbo Nigeria, Sab Somalie, Castes Wolof & Mande Discrimination Subsaharienne",
      country: "Afrique",
      caste_based_violence_atrocity_severity_score: 52.0,
      untouchability_practice_occupation_segregation_scale_score: 51.0,
      intercaste_marriage_honor_violence_score: 54.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 53.0,
      composite_score: 52.45,
      risk_level: "élevé",
      primary_pattern: "caste_affirmative_action_legal_protection_deficit_gap",
      estimated_caste_discrimination_untouchability_index: 5.25,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-007",
      name: "IDSN/NACDOR — International Dalit Solidarity Network, National Campaign Dalit HR, Résolution HRC & Principes Discrimination Caste ONU",
      country: "Global",
      caste_based_violence_atrocity_severity_score: 27.0,
      untouchability_practice_occupation_segregation_scale_score: 25.0,
      intercaste_marriage_honor_violence_score: 28.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 26.0,
      composite_score: 26.55,
      risk_level: "modéré",
      primary_pattern: "caste_affirmative_action_legal_protection_deficit_gap",
      estimated_caste_discrimination_untouchability_index: 2.66,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "CDU-008",
      name: "ONU/CERD Caste — CERD Recommandation Générale 29 Caste 2002, HCDH Rapport Discrimination Ascendance & SDG 10 Inégalités",
      country: "Global",
      caste_based_violence_atrocity_severity_score: 4.0,
      untouchability_practice_occupation_segregation_scale_score: 4.0,
      intercaste_marriage_honor_violence_score: 4.0,
      caste_affirmative_action_legal_protection_deficit_gap_score: 4.0,
      composite_score: 4.00,
      risk_level: "faible",
      primary_pattern: "caste_based_violence_atrocity_severity",
      estimated_caste_discrimination_untouchability_index: 0.40,
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
      `${process.env.SWARM_API_URL}/caste-discrimination-untouchability-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
