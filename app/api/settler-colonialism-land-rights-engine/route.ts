import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[settler-colonialism-land-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "settler_colonialism_land_rights",
  generated_at: new Date().toISOString(),
  avg_composite: 58.33,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  entities: [
    {
      id: "SCL-001",
      name: "Palestine (colonisation Cisjordanie)",
      composite_score: 94.30,
      risk_level: "critique",
      estimated_land_rights_index: 9.43,
    },
    {
      id: "SCL-002",
      name: "Australie (terra nullius legacy)",
      composite_score: 78.10,
      risk_level: "critique",
      estimated_land_rights_index: 7.81,
    },
    {
      id: "SCL-003",
      name: "Inde (Adivasi déplacements mines)",
      composite_score: 74.10,
      risk_level: "critique",
      estimated_land_rights_index: 7.41,
    },
    {
      id: "SCL-004",
      name: "Colombie (accaparement terres)",
      composite_score: 69.10,
      risk_level: "critique",
      estimated_land_rights_index: 6.91,
    },
    {
      id: "SCL-005",
      name: "Brésil (Amazonie garimpeiros)",
      composite_score: 58.10,
      risk_level: "élevé",
      estimated_land_rights_index: 5.81,
    },
    {
      id: "SCL-006",
      name: "Canada (revendications territoriales)",
      composite_score: 52.10,
      risk_level: "élevé",
      estimated_land_rights_index: 5.21,
    },
    {
      id: "SCL-007",
      name: "Nouvelle-Zélande (Treaty Waitangi)",
      composite_score: 27.75,
      risk_level: "modéré",
      estimated_land_rights_index: 2.78,
    },
    {
      id: "SCL-008",
      name: "Bolivie (plurinationalité)",
      composite_score: 13.10,
      risk_level: "faible",
      estimated_land_rights_index: 1.31,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/settler-colonialism-land-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
