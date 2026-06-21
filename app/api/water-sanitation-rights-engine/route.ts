import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[water-sanitation-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "water_sanitation_rights",
  total_entities: 8,
  avg_composite: 58.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "WSR-001",
      name: "Somalie (accès eau <50%, conflits)",
      composite_score: 91.30,
      level: "critique",
      estimated_water_rights_index: 9.13,
    },
    {
      id: "WSR-002",
      name: "République Centrafricaine (infrastructure détruite)",
      composite_score: 85.85,
      level: "critique",
      estimated_water_rights_index: 8.59,
    },
    {
      id: "WSR-003",
      name: "Mali (zones rurales sahéliennes)",
      composite_score: 78.85,
      level: "critique",
      estimated_water_rights_index: 7.89,
    },
    {
      id: "WSR-004",
      name: "Niger (pénurie chronique)",
      composite_score: 70.85,
      level: "critique",
      estimated_water_rights_index: 7.09,
    },
    {
      id: "WSR-005",
      name: "Bangladesh (arsenic nappes)",
      composite_score: 54.65,
      level: "élevé",
      estimated_water_rights_index: 5.47,
    },
    {
      id: "WSR-006",
      name: "Inde (contaminations chroniques)",
      composite_score: 46.60,
      level: "élevé",
      estimated_water_rights_index: 4.66,
    },
    {
      id: "WSR-007",
      name: "Mexique (accès inégal urbain/rural)",
      composite_score: 29.30,
      level: "modéré",
      estimated_water_rights_index: 2.93,
    },
    {
      id: "WSR-008",
      name: "Pays-Bas (eau universelle garantie)",
      composite_score: 8.05,
      level: "faible",
      estimated_water_rights_index: 0.81,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-sanitation-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
