import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[conflict-mineral-resources-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "conflict_mineral_resources",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "CMR-001", name: "RDC Est (cobalt/coltan/or)", composite_score: 93.85, risk_level: "critique", estimated_conflict_mineral_index: 9.39 },
    { id: "CMR-002", name: "Myanmar (jade + minerais junta)", composite_score: 87.10, risk_level: "critique", estimated_conflict_mineral_index: 8.71 },
    { id: "CMR-003", name: "Soudan du Sud (pétrole conflit)", composite_score: 81.65, risk_level: "critique", estimated_conflict_mineral_index: 8.17 },
    { id: "CMR-004", name: "Zimbabwe (diamonds Marange)", composite_score: 73.90, risk_level: "critique", estimated_conflict_mineral_index: 7.39 },
    { id: "CMR-005", name: "Colombie (or + coca financement)", composite_score: 57.90, risk_level: "élevé", estimated_conflict_mineral_index: 5.79 },
    { id: "CMR-006", name: "CAR (diamants + or groupes armés)", composite_score: 57.90, risk_level: "élevé", estimated_conflict_mineral_index: 5.79 },
    { id: "CMR-007", name: "Pérou (orpaillage illégal Amazonie)", composite_score: 32.85, risk_level: "modéré", estimated_conflict_mineral_index: 3.29 },
    { id: "CMR-008", name: "Rwanda (3TG certification)", composite_score: 11.85, risk_level: "faible", estimated_conflict_mineral_index: 1.19 },
  ],
  avg_composite: 62.13,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/conflict-mineral-resources-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
