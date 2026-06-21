import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[elderly-rights-ageism-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "elderly_rights_ageism",
  generated_at: new Date().toISOString(),
  entities: [
    {
      entity_id: "ERA-001",
      name: "Somalie (aucun système pension)",
      composite_score: 90.65,
      risk_level: "critique",
      estimated_elderly_rights_index: 9.07,
    },
    {
      entity_id: "ERA-002",
      name: "Haïti (seniors abandonnés)",
      composite_score: 84.85,
      risk_level: "critique",
      estimated_elderly_rights_index: 8.49,
    },
    {
      entity_id: "ERA-003",
      name: "Inde (zones rurales sans protection)",
      composite_score: 75.60,
      risk_level: "critique",
      estimated_elderly_rights_index: 7.56,
    },
    {
      entity_id: "ERA-004",
      name: "Nigeria (maltraitance seniors)",
      composite_score: 67.90,
      risk_level: "critique",
      estimated_elderly_rights_index: 6.79,
    },
    {
      entity_id: "ERA-005",
      name: "Chine (abandon rural exodus)",
      composite_score: 53.70,
      risk_level: "élevé",
      estimated_elderly_rights_index: 5.37,
    },
    {
      entity_id: "ERA-006",
      name: "USA (coût soins EHPAD)",
      composite_score: 45.80,
      risk_level: "élevé",
      estimated_elderly_rights_index: 4.58,
    },
    {
      entity_id: "ERA-007",
      name: "France (canicule 2003 legacy)",
      composite_score: 26.75,
      risk_level: "modéré",
      estimated_elderly_rights_index: 2.68,
    },
    {
      entity_id: "ERA-008",
      name: "Norvège (silver economy modèle)",
      composite_score: 9.85,
      risk_level: "faible",
      estimated_elderly_rights_index: 0.99,
    },
  ],
  avg_composite: 56.89,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/elderly-rights-ageism-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
