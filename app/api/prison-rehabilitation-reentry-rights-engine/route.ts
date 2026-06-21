import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-rehabilitation-reentry-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Rehabilitation Reentry Rights Engine Agent",
  domain: "prison_rehabilitation_reentry_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    solitary_confinement_prolonged_use: 1,
    prison_overcrowding_inhumane_conditions_severity: 2,
    rehabilitation_education_program_absence_scale: 3,
    post_release_reintegration_support_deficit_gap: 2,
  },
  top_risk_entities: [
    "USA — 2.3M Détenus #1 Monde, Solitary 80 000, Prison Privatisée Lobby, For-Profit & Three Strikes Perpétuité",
    "Philippines — Prisons 500% Surpeuplées, 800 Détenus/Cellule 50 Places, Morts Chaleur & Guerre Drogue Détenus Abandonnés",
    "Brésil — APAC vs Complexes Régimes, Massacres Pénitentiaires Carandiru, Factions Contrôlent Prisons & Réhab Absente",
  ],
  critical_alerts: [
    "USA: solitary_confinement_prolonged_use",
    "Philippines: prison_overcrowding_inhumane_conditions_severity",
    "Brésil: rehabilitation_education_program_absence_scale",
    "Russie/Belarus: post_release_reintegration_support_deficit_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_prison_rehabilitation_reentry_rights_index: 6.14,
  data_sources: [
    "penal_reform_international_global_prison_trends",
    "un_mandela_rules_implementation_monitoring_report",
    "human_rights_watch_solitary_confinement_report",
  ],
  entities: [
    {
      id: "PRR-001",
      name: "USA — 2.3M Détenus #1 Monde, Solitary 80 000, Prison Privatisée Lobby, For-Profit & Three Strikes Perpétuité",
      country: "USA",
      prison_overcrowding_inhumane_conditions_severity_score: 95.0,
      rehabilitation_education_program_absence_scale_score: 93.0,
      solitary_confinement_prolonged_use_score: 92.0,
      post_release_reintegration_support_deficit_gap_score: 91.0,
      composite_score: 92.95,
      risk_level: "critique",
      primary_pattern: "solitary_confinement_prolonged_use",
      estimated_prison_rehabilitation_reentry_rights_index: 9.3,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-002",
      name: "Philippines — Prisons 500% Surpeuplées, 800 Détenus/Cellule 50 Places, Morts Chaleur & Guerre Drogue Détenus Abandonnés",
      country: "Philippines",
      prison_overcrowding_inhumane_conditions_severity_score: 92.0,
      rehabilitation_education_program_absence_scale_score: 90.0,
      solitary_confinement_prolonged_use_score: 89.0,
      post_release_reintegration_support_deficit_gap_score: 88.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "prison_overcrowding_inhumane_conditions_severity",
      estimated_prison_rehabilitation_reentry_rights_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-003",
      name: "Brésil — APAC vs Complexes Régimes, Massacres Pénitentiaires Carandiru, Factions Contrôlent Prisons & Réhab Absente",
      country: "Brésil",
      prison_overcrowding_inhumane_conditions_severity_score: 89.0,
      rehabilitation_education_program_absence_scale_score: 87.0,
      solitary_confinement_prolonged_use_score: 86.0,
      post_release_reintegration_support_deficit_gap_score: 85.0,
      composite_score: 86.95,
      risk_level: "critique",
      primary_pattern: "rehabilitation_education_program_absence_scale",
      estimated_prison_rehabilitation_reentry_rights_index: 8.7,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-004",
      name: "Russie/Belarus — Colonies Pénitentiaires Sibérie, Travail Forcé Prisonniers, Torture Systématique & IK-6 Navalny",
      country: "Russie/Belarus",
      prison_overcrowding_inhumane_conditions_severity_score: 86.0,
      rehabilitation_education_program_absence_scale_score: 84.0,
      solitary_confinement_prolonged_use_score: 83.0,
      post_release_reintegration_support_deficit_gap_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "post_release_reintegration_support_deficit_gap",
      estimated_prison_rehabilitation_reentry_rights_index: 8.4,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-005",
      name: "Afrique Sub-Saharienne — Prisons Coloniales Non Réformées, Détention Préventive 70%, Sans Procès Années & Maladies",
      country: "Afrique Sub-Saharienne",
      prison_overcrowding_inhumane_conditions_severity_score: 57.0,
      rehabilitation_education_program_absence_scale_score: 55.0,
      solitary_confinement_prolonged_use_score: 54.0,
      post_release_reintegration_support_deficit_gap_score: 53.0,
      composite_score: 54.95,
      risk_level: "élevé",
      primary_pattern: "prison_overcrowding_inhumane_conditions_severity",
      estimated_prison_rehabilitation_reentry_rights_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-006",
      name: "Europe — Récidive Manque Réhab France, UK Short Sentences Inefficaces, Norvège Modèle Non Copié & Détention Immigrants",
      country: "Europe",
      prison_overcrowding_inhumane_conditions_severity_score: 54.0,
      rehabilitation_education_program_absence_scale_score: 52.0,
      solitary_confinement_prolonged_use_score: 51.0,
      post_release_reintegration_support_deficit_gap_score: 50.0,
      composite_score: 51.95,
      risk_level: "élevé",
      primary_pattern: "rehabilitation_education_program_absence_scale",
      estimated_prison_rehabilitation_reentry_rights_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-007",
      name: "Penal Reform International/ICPA — Standards Mandela Rules, Réforme Pénitentiaire Globale, Réhab Evidence-Based & Monitoring",
      country: "Global",
      prison_overcrowding_inhumane_conditions_severity_score: 27.0,
      rehabilitation_education_program_absence_scale_score: 26.0,
      solitary_confinement_prolonged_use_score: 25.0,
      post_release_reintegration_support_deficit_gap_score: 25.0,
      composite_score: 25.85,
      risk_level: "modéré",
      primary_pattern: "rehabilitation_education_program_absence_scale",
      estimated_prison_rehabilitation_reentry_rights_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "PRR-008",
      name: "ONU/Règles Mandela — Règles Minima Traitement Détenus, OPCAT Mécanismes & SDG 16.3 Justice Accès",
      country: "Global",
      prison_overcrowding_inhumane_conditions_severity_score: 5.0,
      rehabilitation_education_program_absence_scale_score: 4.0,
      solitary_confinement_prolonged_use_score: 4.0,
      post_release_reintegration_support_deficit_gap_score: 4.0,
      composite_score: 4.3,
      risk_level: "faible",
      primary_pattern: "post_release_reintegration_support_deficit_gap",
      estimated_prison_rehabilitation_reentry_rights_index: 0.43,
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
      `${process.env.SWARM_API_URL}/prison-rehabilitation-reentry-rights-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
