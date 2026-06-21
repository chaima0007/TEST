import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Elder Rights Aging Population Engine Agent",
  domain: "elder_rights_aging_population",
  total_entities: 8,
  avg_composite: 62.27,
  confidence_score: 0.88,
  avg_estimated_elder_rights_aging_index: 6.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_open_ended_working_group_ageing_2023",
    "helpage_global_agewatch_index_2023",
    "human_rights_watch_elder_rights_2022",
    "who_global_report_on_ageism_2021",
  ],
  critical_alerts: [],
  entities: [
    {
      entity_id: "YE-001",
      name: "Yémen — Aînés en Zone de Conflit",
      composite_score: 89.1,
      risk_level: "critique",
      estimated_elder_rights_aging_index: 8.91,
    },
    {
      entity_id: "MM-002",
      name: "Myanmar — Junta & Abandon des Aînés",
      composite_score: 86.25,
      risk_level: "critique",
      estimated_elder_rights_aging_index: 8.62,
    },
    {
      entity_id: "KP-003",
      name: "Corée du Nord — Aînés sous Contrôle Totalitaire",
      composite_score: 87.05,
      risk_level: "critique",
      estimated_elder_rights_aging_index: 8.71,
    },
    {
      entity_id: "PK-004",
      name: "Pakistan — Protection Sociale Inexistante",
      composite_score: 81.6,
      risk_level: "critique",
      estimated_elder_rights_aging_index: 8.16,
    },
    {
      entity_id: "IN-R-005",
      name: "Inde Rurale — Maltraitance & Dépendance Familiale",
      composite_score: 54.9,
      risk_level: "élevé",
      estimated_elder_rights_aging_index: 5.49,
    },
    {
      entity_id: "RU-006",
      name: "Russie — Guerre & Détérioration des Droits",
      composite_score: 55.1,
      risk_level: "élevé",
      estimated_elder_rights_aging_index: 5.51,
    },
    {
      entity_id: "PH-007",
      name: "Philippines — Seniors Act, Inégalités Persistantes",
      composite_score: 31.6,
      risk_level: "modéré",
      estimated_elder_rights_aging_index: 3.16,
    },
    {
      entity_id: "JP-008",
      name: "Japon — Modèle Vieillissement avec Défis Persistants",
      composite_score: 12.6,
      risk_level: "faible",
      estimated_elder_rights_aging_index: 1.26,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[elder-rights-aging-population-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elder-rights-aging-population-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
