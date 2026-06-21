import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[enforced-disappearances-extrajudicial-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  agent: "Enforced Disappearances Extrajudicial Engine Agent",
  domain: "enforced_disappearances_extrajudicial",
  total_entities: 8,
  avg_composite: 63.72,
  confidence_score: 0.87,
  avg_estimated_disappearances_index: 6.37,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_working_group_enforced_disappearances_2023",
    "amnesty_international_disappearances_report_2023",
    "human_rights_watch_extrajudicial_killings_2023",
    "icc_enforced_disappearances_jurisprudence_2023",
  ],
  entities: [
    {
      id: "EDE-001",
      name: "Mexique — 100 000+ Personnes Disparues, Cartels & Complicité État, Fosses Communes Massives",
      country: "Mexique",
      composite_score: 93.75,
      risk_level: "critique",
      disappearance_rate_impunity_score: 96.0,
      extrajudicial_killing_score: 93.0,
      state_accountability_deficit_score: 94.0,
      truth_justice_reparation_score: 91.0,
      estimated_disappearances_index: 9.38,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-002",
      name: "Syrie — Régime Assad: 150 000+ Détenus Disparus, Torture Industrielle, Charnel Saydnaya",
      country: "Syrie",
      composite_score: 97.55,
      risk_level: "critique",
      disappearance_rate_impunity_score: 98.0,
      extrajudicial_killing_score: 97.0,
      state_accountability_deficit_score: 98.0,
      truth_justice_reparation_score: 97.0,
      estimated_disappearances_index: 9.76,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-003",
      name: "Philippines — Guerre Duterte Drogue: 7 000-30 000 Morts Extrajudiciaires 2016-2022",
      country: "Philippines",
      composite_score: 89.15,
      risk_level: "critique",
      disappearance_rate_impunity_score: 89.0,
      extrajudicial_killing_score: 93.0,
      state_accountability_deficit_score: 88.0,
      truth_justice_reparation_score: 86.0,
      estimated_disappearances_index: 8.92,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-004",
      name: "Égypte — 2 000+ Disparitions Forcées Depuis 2013, Détention Secrète, Sisi Impunité Totale",
      country: "Égypte",
      composite_score: 84.65,
      risk_level: "critique",
      disappearance_rate_impunity_score: 86.0,
      extrajudicial_killing_score: 82.0,
      state_accountability_deficit_score: 87.0,
      truth_justice_reparation_score: 83.0,
      estimated_disappearances_index: 8.47,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-005",
      name: "Colombie Post-FARC — 85 000+ Disparus Conflit, Faux Positifs Armée, JEP Vérité Partielle",
      country: "Colombie",
      composite_score: 51.85,
      risk_level: "élevé",
      disappearance_rate_impunity_score: 55.0,
      extrajudicial_killing_score: 53.0,
      state_accountability_deficit_score: 50.0,
      truth_justice_reparation_score: 48.0,
      estimated_disappearances_index: 5.19,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-006",
      name: "Sri Lanka — 65 000-100 000 Disparus Guerre Civile, Lassana Manel Oubliées, Commission Vérité",
      country: "Sri Lanka",
      composite_score: 51.95,
      risk_level: "élevé",
      disappearance_rate_impunity_score: 53.0,
      extrajudicial_killing_score: 50.0,
      state_accountability_deficit_score: 55.0,
      truth_justice_reparation_score: 49.0,
      estimated_disappearances_index: 5.20,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-007",
      name: "Argentine — Modèle CONADEP: 30 000 Disparus Junte 1976-1983, Procès Emblématiques",
      country: "Argentine",
      composite_score: 26.4,
      risk_level: "modéré",
      disappearance_rate_impunity_score: 30.0,
      extrajudicial_killing_score: 27.0,
      state_accountability_deficit_score: 25.0,
      truth_justice_reparation_score: 22.0,
      estimated_disappearances_index: 2.64,
      last_updated: "2026-06-21",
    },
    {
      id: "EDE-008",
      name: "Espagne — 114 000 Disparus Franquisme, Loi Mémoire Démocratique 2022, Amnistie 1977 Obstacle",
      country: "Espagne",
      composite_score: 14.45,
      risk_level: "faible",
      disappearance_rate_impunity_score: 14.0,
      extrajudicial_killing_score: 11.0,
      state_accountability_deficit_score: 18.0,
      truth_justice_reparation_score: 15.0,
      estimated_disappearances_index: 1.45,
      last_updated: "2026-06-21",
    },
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/enforced-disappearances-extrajudicial-engine`, {
      next: { revalidate: 30 },
    });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
