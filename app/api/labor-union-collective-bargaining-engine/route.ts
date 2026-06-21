import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[labor-union-collective-bargaining-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "labor_union_collective_bargaining",
  generated_at: new Date().toISOString(),
  entities: [
    {
      entity_id: "LUC-001",
      name: "Arabie Saoudite (syndicats interdits)",
      composite_score: 89.75,
      risk_level: "critique",
      estimated_labor_rights_index: 8.98,
    },
    {
      entity_id: "LUC-002",
      name: "Chine (syndicats contrôlés État)",
      composite_score: 87.60,
      risk_level: "critique",
      estimated_labor_rights_index: 8.76,
    },
    {
      entity_id: "LUC-003",
      name: "Bangladesh (garment workers)",
      composite_score: 77.85,
      risk_level: "critique",
      estimated_labor_rights_index: 7.79,
    },
    {
      entity_id: "LUC-004",
      name: "Cambodge (grèves réprimées)",
      composite_score: 71.60,
      risk_level: "critique",
      estimated_labor_rights_index: 7.16,
    },
    {
      entity_id: "LUC-005",
      name: "USA (Taft-Hartley limitations)",
      composite_score: 51.90,
      risk_level: "élevé",
      estimated_labor_rights_index: 5.19,
    },
    {
      entity_id: "LUC-006",
      name: "Inde (zones export libres)",
      composite_score: 46.70,
      risk_level: "élevé",
      estimated_labor_rights_index: 4.67,
    },
    {
      entity_id: "LUC-007",
      name: "France (représentation partielle)",
      composite_score: 27.85,
      risk_level: "modéré",
      estimated_labor_rights_index: 2.79,
    },
    {
      entity_id: "LUC-008",
      name: "Danemark (modèle nordique)",
      composite_score: 8.95,
      risk_level: "faible",
      estimated_labor_rights_index: 0.90,
    },
  ],
  avg_composite: 58.02,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/labor-union-collective-bargaining-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
