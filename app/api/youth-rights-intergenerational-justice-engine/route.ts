import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[youth-rights-intergenerational-justice-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "youth_rights_intergenerational_justice_engine",
  domain: "youth_rights_intergenerational_justice",
  total_entities: 8,
  avg_composite: 62.16,
  confidence_score: 0.89,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    child_soldier_exploitation: 3,
    education_deprivation: 2,
    intergenerational_poverty: 2,
    state_protection_deficit: 1,
  },
  top_risk_entities: [
    { id: "YRJ-001", name: "Mali — 77% Jeunes Sans Emploi, Conflit Armé, Droit Futur Violé", score: 91.9, risk: "critique" },
    { id: "YRJ-003", name: "Yémen — Génération Entière Sans Éducation, Famine", score: 91.05, risk: "critique" },
    { id: "YRJ-002", name: "Burundi — Recrutement Enfants Soldats, Pauvreté Intergénérationnelle", score: 90.85, risk: "critique" },
  ],
  critical_alerts: [
    "YRJ-001: Mali — 77% Jeunes Sans Emploi, Conflit Armé, Droit Futur Violé — composite 91.9",
    "YRJ-002: Burundi — Recrutement Enfants Soldats, Pauvreté Intergénérationnelle — composite 90.85",
    "YRJ-003: Yémen — Génération Entière Sans Éducation, Famine — composite 91.05",
    "YRJ-004: Haïti — Gangs Recruteurs Jeunes, État Défaillant — composite 88.45",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_youth_rights_intergenerational_justice_index: 6.21,
  data_sources: [
    "unicef_state_worlds_children_2023",
    "ilo_global_employment_trends_youth_2023",
    "youth_for_human_rights_report_2023",
    "un_crc_committee_recommendations_2023",
  ],
  entities: [
    {
      id: "YRJ-001",
      name: "Mali — 77% Jeunes Sans Emploi, Conflit Armé, Droit Futur Violé",
      country: "Mali",
      youth_employment_education_rights_deprivation_score: 94.0,
      child_soldier_exploitation_intergenerational_harm_score: 90.0,
      intergenerational_poverty_inequality_transmission_score: 92.0,
      state_protection_future_generations_deficit_score: 91.0,
      composite_score: 91.9,
      risk_level: "critique",
      primary_pattern: "Chômage jeunes 77%, recrutement groupes armés sahéliens, génération sans avenir",
      estimated_youth_rights_intergenerational_justice_index: 9.19,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-002",
      name: "Burundi — Recrutement Enfants Soldats, Pauvreté Intergénérationnelle",
      country: "Burundi",
      youth_employment_education_rights_deprivation_score: 91.0,
      child_soldier_exploitation_intergenerational_harm_score: 93.0,
      intergenerational_poverty_inequality_transmission_score: 90.0,
      state_protection_future_generations_deficit_score: 89.0,
      composite_score: 90.85,
      risk_level: "critique",
      primary_pattern: "Recrutement enfants Imbonerakure, pauvreté héréditaire, État défaillant protections",
      estimated_youth_rights_intergenerational_justice_index: 9.08,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-003",
      name: "Yémen — Génération Entière Sans Éducation, Famine",
      country: "Yémen",
      youth_employment_education_rights_deprivation_score: 93.0,
      child_soldier_exploitation_intergenerational_harm_score: 88.0,
      intergenerational_poverty_inequality_transmission_score: 91.0,
      state_protection_future_generations_deficit_score: 92.0,
      composite_score: 91.05,
      risk_level: "critique",
      primary_pattern: "2M enfants déscolarisés, famine générationnelle, trauma PTSD collectif, mariage précoce",
      estimated_youth_rights_intergenerational_justice_index: 9.11,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-004",
      name: "Haïti — Gangs Recruteurs Jeunes, État Défaillant",
      country: "Haïti",
      youth_employment_education_rights_deprivation_score: 89.0,
      child_soldier_exploitation_intergenerational_harm_score: 87.0,
      intergenerational_poverty_inequality_transmission_score: 88.0,
      state_protection_future_generations_deficit_score: 90.0,
      composite_score: 88.45,
      risk_level: "critique",
      primary_pattern: "Gangs G9 recrutent enfants, effondrement système éducatif, 60% population -25 ans",
      estimated_youth_rights_intergenerational_justice_index: 8.85,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-005",
      name: "Bangladesh — Ateliers Jeunes, Manifestations Réprimées 2024",
      country: "Bangladesh",
      youth_employment_education_rights_deprivation_score: 55.0,
      child_soldier_exploitation_intergenerational_harm_score: 50.0,
      intergenerational_poverty_inequality_transmission_score: 53.0,
      state_protection_future_generations_deficit_score: 54.0,
      composite_score: 53.05,
      risk_level: "élevé",
      primary_pattern: "Ateliers textile exploitant jeunes, répression manifestations étudiantes juillet 2024",
      estimated_youth_rights_intergenerational_justice_index: 5.3,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-006",
      name: "Éthiopie — Jeunes Tigré Trauma, Déplacement",
      country: "Éthiopie",
      youth_employment_education_rights_deprivation_score: 52.0,
      child_soldier_exploitation_intergenerational_harm_score: 54.0,
      intergenerational_poverty_inequality_transmission_score: 51.0,
      state_protection_future_generations_deficit_score: 50.0,
      composite_score: 51.85,
      risk_level: "élevé",
      primary_pattern: "Conflit Tigré trauma générationnel, 2M déplacés jeunes, éducation interrompue",
      estimated_youth_rights_intergenerational_justice_index: 5.18,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-007",
      name: "Brésil — Inégalités Intergénérationnelles, Crime Organisé",
      country: "Brésil",
      youth_employment_education_rights_deprivation_score: 27.0,
      child_soldier_exploitation_intergenerational_harm_score: 24.0,
      intergenerational_poverty_inequality_transmission_score: 28.0,
      state_protection_future_generations_deficit_score: 25.0,
      composite_score: 26.1,
      risk_level: "modéré",
      primary_pattern: "Favelas inégalités héréditaires, trafic drogue recrute jeunes, Bolsa Família limité",
      estimated_youth_rights_intergenerational_justice_index: 2.61,
      last_updated: "2026-06-21",
    },
    {
      id: "YRJ-008",
      name: "Finlande — Droits Jeunes Constitutionnels, Meilleur Système Éducatif",
      country: "Finlande",
      youth_employment_education_rights_deprivation_score: 4.0,
      child_soldier_exploitation_intergenerational_harm_score: 4.0,
      intergenerational_poverty_inequality_transmission_score: 4.0,
      state_protection_future_generations_deficit_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Droits jeunes constitutionnels, PISA meilleur système, parlement jeunesse consultatif",
      estimated_youth_rights_intergenerational_justice_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/youth-rights-intergenerational-justice-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
