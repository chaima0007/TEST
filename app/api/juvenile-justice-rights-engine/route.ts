import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[juvenile-justice-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Juvenile Justice Rights Engine Agent",
  domain: "juvenile_justice_rights",
  total_entities: 8,
  avg_composite: 60.12,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Pakistan — Peine de Mort Mineurs, 1 500 Enfants dans Prisons Adultes",
    "Iran — Exécutions Mineurs, 90 Condamnés à Mort Ex-Mineurs, CRC Non-Respectée",
    "Nigéria — Almajiri/Enfants Rues Incarcérés, Prisons Adultes, Torture",
  ],
  critical_alerts: [
    "Pakistan: adult_prosecution_minors",
    "Iran: adult_prosecution_minors",
    "Nigéria: detention_conditions_minors",
    "USA: child_incarceration",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_juvenile_justice_rights_index: 6.01,
  entities: [
    {
      entity_id: "JJR-001",
      name: "Pakistan — Peine de Mort Mineurs, 1 500 Enfants dans Prisons Adultes",
      country: "Pakistan",
      child_incarceration_score: 97.0,
      adult_prosecution_minors_score: 96.0,
      detention_conditions_minors_score: 95.0,
      rehabilitation_gap_score: 94.0,
      composite_score: 95.8,
      risk_level: "critique",
      primary_pattern: "adult_prosecution_minors",
      estimated_juvenile_justice_rights_index: 9.58,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-002",
      name: "Iran — Exécutions Mineurs, 90 Condamnés à Mort Ex-Mineurs, CRC Non-Respectée",
      country: "Iran",
      child_incarceration_score: 92.0,
      adult_prosecution_minors_score: 94.0,
      detention_conditions_minors_score: 90.0,
      rehabilitation_gap_score: 91.0,
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "adult_prosecution_minors",
      estimated_juvenile_justice_rights_index: 9.18,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-003",
      name: "Nigéria — Almajiri/Enfants Rues Incarcérés, Prisons Adultes, Torture",
      country: "Nigéria",
      child_incarceration_score: 85.0,
      adult_prosecution_minors_score: 83.0,
      detention_conditions_minors_score: 87.0,
      rehabilitation_gap_score: 82.0,
      composite_score: 84.5,
      risk_level: "critique",
      primary_pattern: "detention_conditions_minors",
      estimated_juvenile_justice_rights_index: 8.45,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-004",
      name: "USA — JLWOP (Juvenile Life Without Parole), 44 000 Mineurs Incarcérés, Solitary",
      country: "USA",
      child_incarceration_score: 76.0,
      adult_prosecution_minors_score: 78.0,
      detention_conditions_minors_score: 74.0,
      rehabilitation_gap_score: 72.0,
      composite_score: 75.2,
      risk_level: "critique",
      primary_pattern: "child_incarceration",
      estimated_juvenile_justice_rights_index: 7.52,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-005",
      name: "Brésil — FUNABEM Héritage, 24 000 Mineurs FEBEM, Violence Systémique",
      country: "Brésil",
      child_incarceration_score: 56.0,
      adult_prosecution_minors_score: 52.0,
      detention_conditions_minors_score: 58.0,
      rehabilitation_gap_score: 54.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "detention_conditions_minors",
      estimated_juvenile_justice_rights_index: 5.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-006",
      name: "Indonésie — Age Responsabilité 8 Ans, 3 000 Mineurs Prisons Adultes",
      country: "Indonésie",
      child_incarceration_score: 46.0,
      adult_prosecution_minors_score: 48.0,
      detention_conditions_minors_score: 44.0,
      rehabilitation_gap_score: 42.0,
      composite_score: 45.3,
      risk_level: "élevé",
      primary_pattern: "adult_prosecution_minors",
      estimated_juvenile_justice_rights_index: 4.53,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-007",
      name: "UK — Age Responsabilité 10 Ans (Plus Bas UE), Rainsbrook STC Fermeture Tardive",
      country: "UK",
      child_incarceration_score: 28.0,
      adult_prosecution_minors_score: 30.0,
      detention_conditions_minors_score: 26.0,
      rehabilitation_gap_score: 24.0,
      composite_score: 27.3,
      risk_level: "modéré",
      primary_pattern: "child_incarceration",
      estimated_juvenile_justice_rights_index: 2.73,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "JJR-008",
      name: "Norvège/Belgique — Justice Restauratrice, Âge 15+, Centres Ouverts Réhabilitation",
      country: "Norvège/Belgique",
      child_incarceration_score: 6.0,
      adult_prosecution_minors_score: 7.0,
      detention_conditions_minors_score: 5.0,
      rehabilitation_gap_score: 8.0,
      composite_score: 6.35,
      risk_level: "faible",
      primary_pattern: "rehabilitation_gap",
      estimated_juvenile_justice_rights_index: 0.64,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/juvenile-justice-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
