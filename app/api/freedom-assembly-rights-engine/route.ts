import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[freedom-assembly-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[freedom-assembly-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "Freedom Assembly Rights Engine Agent",
  domain: "freedom_assembly_rights",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.87,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    protest_repression: 5,
    civil_society_suppression: 2,
    ngo_criminalization: 2,
  },
  top_risk_entities: [
    "Biélorussie — 35 000 Arrêtés Manifestations Post-2020",
    "Iran — Mahsa Amini 2022, 500+ Tués, 15 000 Arrêtés",
    "Russie — Loi Anti-Guerre, 16 000+ Arrestations",
  ],
  critical_alerts: [
    "Biélorussie: protest_repression",
    "Iran: protest_repression",
    "Russie: civil_society_suppression",
    "Myanmar: protest_repression",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_freedom_assembly_rights_index: 6.18,
  data_sources: [
    "civicus_monitor_2024",
    "hrw_assembly_rights_2024",
    "amnesty_protest_crackdown_2024",
    "ifex_freedom_expression_report",
  ],
  entities: [
    {
      id: "FAR-001",
      name: "Biélorussie — 35 000 Arrêtés Manifestations Post-2020",
      country: "Biélorussie",
      composite_score: 89.55,
      risk_level: "critique",
      primary_pattern: "protest_repression",
      estimated_freedom_assembly_rights_index: 8.96,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-002",
      name: "Iran — Mahsa Amini 2022, 500+ Tués, 15 000 Arrêtés",
      country: "Iran",
      composite_score: 87.85,
      risk_level: "critique",
      primary_pattern: "protest_repression",
      estimated_freedom_assembly_rights_index: 8.79,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-003",
      name: "Russie — Loi Anti-Guerre, 16 000+ Arrestations",
      country: "Russie",
      composite_score: 91.75,
      risk_level: "critique",
      primary_pattern: "civil_society_suppression",
      estimated_freedom_assembly_rights_index: 9.18,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-004",
      name: "Myanmar — Militaires Tirant Manifestants Post-Coup 2021",
      country: "Myanmar",
      composite_score: 91.65,
      risk_level: "critique",
      primary_pattern: "protest_repression",
      estimated_freedom_assembly_rights_index: 9.17,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-005",
      name: "Éthiopie/Tigray — ONG Expulsées, Anti-Terroriste Contre Civils",
      country: "Éthiopie",
      composite_score: 54.00,
      risk_level: "élevé",
      primary_pattern: "ngo_criminalization",
      estimated_freedom_assembly_rights_index: 5.40,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-006",
      name: "Inde — UAPA Contre Militants, ONG FCRA Bloquées",
      country: "Inde",
      composite_score: 49.35,
      risk_level: "élevé",
      primary_pattern: "ngo_criminalization",
      estimated_freedom_assembly_rights_index: 4.94,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-007",
      name: "France — LBD Mutilations Gilets Jaunes, Maintien Ordre",
      country: "France",
      composite_score: 25.00,
      risk_level: "modéré",
      primary_pattern: "protest_repression",
      estimated_freedom_assembly_rights_index: 2.50,
      last_updated: "2026-06-22",
    },
    {
      id: "FAR-008",
      name: "Costa Rica/Uruguay — Meilleure Pratique Liberté Réunion",
      country: "Costa Rica/Uruguay",
      composite_score: 5.30,
      risk_level: "faible",
      primary_pattern: "civil_society_suppression",
      estimated_freedom_assembly_rights_index: 0.53,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const upstream = await fetch(`${SWARM_API_URL}/freedom-assembly-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 }));
  }
}
