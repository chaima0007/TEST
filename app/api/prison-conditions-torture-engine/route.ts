import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-conditions-torture-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "prison_conditions_torture",
  generated_at: new Date().toISOString(),
  avg_composite: 63.20,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "PCT-001",
      name: "Corée du Nord (gwalliso camps)",
      composite_score: 97.10,
      risk_level: "critique",
      estimated_prison_rights_index: 9.71,
    },
    {
      id: "PCT-002",
      name: "Syrie (prisons Assad — Saydnaya)",
      composite_score: 94.85,
      risk_level: "critique",
      estimated_prison_rights_index: 9.49,
    },
    {
      id: "PCT-003",
      name: "Érythrée (Sawa + prisons secrètes)",
      composite_score: 89.60,
      risk_level: "critique",
      estimated_prison_rights_index: 8.96,
    },
    {
      id: "PCT-004",
      name: "Libye (centres détention migrants)",
      composite_score: 82.85,
      risk_level: "critique",
      estimated_prison_rights_index: 8.29,
    },
    {
      id: "PCT-005",
      name: "Philippines (drug war prisons)",
      composite_score: 55.70,
      risk_level: "élevé",
      estimated_prison_rights_index: 5.57,
    },
    {
      id: "PCT-006",
      name: "USA (solitary confinement)",
      composite_score: 47.85,
      risk_level: "élevé",
      estimated_prison_rights_index: 4.79,
    },
    {
      id: "PCT-007",
      name: "France (surpopulation chronique)",
      composite_score: 28.65,
      risk_level: "modéré",
      estimated_prison_rights_index: 2.87,
    },
    {
      id: "PCT-008",
      name: "Norvège (réhabilitation modèle)",
      composite_score: 8.95,
      risk_level: "faible",
      estimated_prison_rights_index: 0.90,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-conditions-torture-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
