import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[sexual-reproductive-health-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "sexual-reproductive-health-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "SRH-001", name: "El Salvador (avortement totalement interdit)", composite_score: 89.85, level: "critique", estimated_srh_rights_index: 8.99 },
    { id: "SRH-002", name: "Nicaragua (criminalisation totale)", composite_score: 85.80, level: "critique", estimated_srh_rights_index: 8.58 },
    { id: "SRH-003", name: "Pologne (ban quasi-total post-2021)", composite_score: 74.15, level: "critique", estimated_srh_rights_index: 7.42 },
    { id: "SRH-004", name: "USA — Texas/Idaho (trigger laws)", composite_score: 65.65, level: "critique", estimated_srh_rights_index: 6.57 },
    { id: "SRH-005", name: "Maroc (avortement illégal sauf exception)", composite_score: 51.90, level: "élevé", estimated_srh_rights_index: 5.19 },
    { id: "SRH-006", name: "Inde (mortalité maternelle rurale)", composite_score: 44.70, level: "élevé", estimated_srh_rights_index: 4.47 },
    { id: "SRH-007", name: "Allemagne (§218 vestige)", composite_score: 27.80, level: "modéré", estimated_srh_rights_index: 2.78 },
    { id: "SRH-008", name: "Pays-Bas (accès universel)", composite_score: 9.15, level: "faible", estimated_srh_rights_index: 0.92 }
  ],
  avg_composite: 56.13,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sexual-reproductive-health-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
