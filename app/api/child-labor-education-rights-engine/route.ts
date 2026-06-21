import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "child_labor_education_rights_engine",
  domain: "child_labor_education_rights",
  total_entities: 8,
  avg_composite: 59.19,
  confidence_score: 0.91,
  avg_estimated_child_labor_education_rights_index: 5.92,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_child_labour_global_estimates_2022",
    "unicef_education_crisis_2023",
    "save_the_children_2023",
    "un_crc_committee_reports_2023",
  ],
  critical_alerts: [
    "Mali — 77% enfants hors école en zones de conflit, recrutement milices jihadistes — risk_level: critique, composite: 84.5",
    "Burkina Faso — fermetures massives écoles (4000+) par groupes armés, enseignants ciblés — risk_level: critique, composite: 81.9",
    "Yémen — 2300 écoles bombardées, 4,5M enfants déscolarisés, travail forcé conflit — risk_level: critique, composite: 81.45",
    "Érythrée — service national Sawa obligatoire enfants 17 ans, travail d'État forcé — risk_level: critique, composite: 78.6",
  ],
  entities: [
    {
      entity_id: "CLER-001",
      name: "Mali — 77% enfants hors école en zones de conflit, recrutement milices jihadistes",
      sub1: 85.0,
      sub2: 90.0,
      sub3: 82.0,
      sub4: 80.0,
      composite_score: 84.5,
      risk_level: "critique",
      estimated_child_labor_education_rights_index: 8.45,
    },
    {
      entity_id: "CLER-002",
      name: "Burkina Faso — fermetures massives écoles (4000+) par groupes armés, enseignants ciblés",
      sub1: 80.0,
      sub2: 88.0,
      sub3: 78.0,
      sub4: 82.0,
      composite_score: 81.9,
      risk_level: "critique",
      estimated_child_labor_education_rights_index: 8.19,
    },
    {
      entity_id: "CLER-003",
      name: "Yémen — 2300 écoles bombardées, 4,5M enfants déscolarisés, travail forcé conflit",
      sub1: 82.0,
      sub2: 85.0,
      sub3: 80.0,
      sub4: 78.0,
      composite_score: 81.45,
      risk_level: "critique",
      estimated_child_labor_education_rights_index: 8.14,
    },
    {
      entity_id: "CLER-004",
      name: "Érythrée — service national Sawa obligatoire enfants 17 ans, travail d&apos;État forcé",
      sub1: 78.0,
      sub2: 75.0,
      sub3: 85.0,
      sub4: 76.0,
      composite_score: 78.6,
      risk_level: "critique",
      estimated_child_labor_education_rights_index: 7.86,
    },
    {
      entity_id: "CLER-005",
      name: "Bangladesh — garment factories, 1,2M enfants travailleurs, accord Rana Plaza",
      sub1: 62.0,
      sub2: 55.0,
      sub3: 58.0,
      sub4: 52.0,
      composite_score: 57.25,
      risk_level: "élevé",
      estimated_child_labor_education_rights_index: 5.72,
    },
    {
      entity_id: "CLER-006",
      name: "Cambodge — travail briqueteries/exploitation rurale, dette familiale, abandon scolaire",
      sub1: 58.0,
      sub2: 52.0,
      sub3: 55.0,
      sub4: 50.0,
      composite_score: 54.15,
      risk_level: "élevé",
      estimated_child_labor_education_rights_index: 5.42,
    },
    {
      entity_id: "CLER-007",
      name: "Inde — Child Labour Act application partielle, 10M enfants au travail secteurs informels",
      sub1: 38.0,
      sub2: 32.0,
      sub3: 35.0,
      sub4: 30.0,
      composite_score: 34.15,
      risk_level: "modéré",
      estimated_child_labor_education_rights_index: 3.41,
    },
    {
      entity_id: "CLER-008",
      name: "Islande — 100% scolarisation, zéro travail enfants documenté, meilleur modèle mondial",
      sub1: 2.0,
      sub2: 1.0,
      sub3: 2.0,
      sub4: 1.0,
      composite_score: 1.55,
      risk_level: "faible",
      estimated_child_labor_education_rights_index: 0.15,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[child-labor-education-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-labor-education-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
