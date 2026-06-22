import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[torture-prevention-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "Torture Prevention Rights Engine Agent",
  domain: "torture_prevention_rights",
  total_entities: 8,
  avg_composite: 62.66,
  confidence_score: 0.89,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    systematic_torture: 5,
    impunity_perpetrators: 3,
    rehabilitation_victims_denial: 1,
  },
  top_risk_entities: [
    "Corée du Nord — Camps Kwanliso Torture Institutionnalisée",
    "Syrie — Centres Détention Assad Torture Industrielle",
    "Égypte — Torture Régime Al-Sissi Documentée HRW",
  ],
  critical_alerts: [
    "Corée du Nord: systematic_torture",
    "Syrie: systematic_torture",
    "Égypte: impunity_perpetrators",
    "Chine: systematic_torture",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_torture_prevention_rights_index: 6.27,
  data_sources: [
    "un_cat_reports_2024",
    "amnesty_torture_report_2024",
    "hrw_torture_detention_2024",
    "irct_torture_survivors_data",
  ],
  entities: [
    {
      id: "TPR-001",
      name: "Corée du Nord — Camps Kwanliso Torture Institutionnalisée",
      country: "Corée du Nord",
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "systematic_torture",
      estimated_torture_prevention_rights_index: 9.18,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-002",
      name: "Syrie — Centres Détention Assad Torture Industrielle",
      country: "Syrie",
      composite_score: 90.55,
      risk_level: "critique",
      primary_pattern: "systematic_torture",
      estimated_torture_prevention_rights_index: 9.06,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-003",
      name: "Égypte — Torture Régime Al-Sissi Documentée HRW",
      country: "Égypte",
      composite_score: 91.00,
      risk_level: "critique",
      primary_pattern: "impunity_perpetrators",
      estimated_torture_prevention_rights_index: 9.10,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-004",
      name: "Chine — Torture Camps Xinjiang 1M+ Ouïghours",
      country: "Chine",
      composite_score: 90.00,
      risk_level: "critique",
      primary_pattern: "systematic_torture",
      estimated_torture_prevention_rights_index: 9.00,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-005",
      name: "Arabie Saoudite — Torture Dissidents, Impunité MBS",
      country: "Arabie Saoudite",
      composite_score: 51.00,
      risk_level: "élevé",
      primary_pattern: "impunity_perpetrators",
      estimated_torture_prevention_rights_index: 5.10,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-006",
      name: "USA — Guantanamo Waterboarding CIA, Isolement 80 000",
      country: "États-Unis",
      composite_score: 51.65,
      risk_level: "élevé",
      primary_pattern: "impunity_perpetrators",
      estimated_torture_prevention_rights_index: 5.17,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-007",
      name: "ONU CAT — Convention Contre Torture Application Limitée",
      country: "International",
      composite_score: 29.80,
      risk_level: "modéré",
      primary_pattern: "rehabilitation_victims_denial",
      estimated_torture_prevention_rights_index: 2.98,
      last_updated: "2026-06-22",
    },
    {
      id: "TPR-008",
      name: "ACAT / Amnesty International — Meilleure Pratique Documentation",
      country: "International",
      composite_score: 5.50,
      risk_level: "faible",
      primary_pattern: "systematic_torture",
      estimated_torture_prevention_rights_index: 0.55,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const upstream = await fetch(`${SWARM_API_URL}/torture-prevention-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 });
  }
}
