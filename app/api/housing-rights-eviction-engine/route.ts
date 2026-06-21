import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[housing-rights-eviction-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "housing-rights-eviction-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "HRE-001", name: "Kenya (évictions informelles Nairobi)", composite_score: 87.60, level: "critique", estimated_housing_rights_index: 8.76 },
    { id: "HRE-002", name: "Philippines (démolitions urbaines)", composite_score: 82.85, level: "critique", estimated_housing_rights_index: 8.29 },
    { id: "HRE-003", name: "Zimbabwe (Murambatsvina legacy)", composite_score: 76.85, level: "critique", estimated_housing_rights_index: 7.69 },
    { id: "HRE-004", name: "Inde (Adivasi expulsions)", composite_score: 69.10, level: "critique", estimated_housing_rights_index: 6.91 },
    { id: "HRE-005", name: "USA (crise logement Los Angeles)", composite_score: 54.85, level: "élevé", estimated_housing_rights_index: 5.49 },
    { id: "HRE-006", name: "Brésil (favelas Rio)", composite_score: 47.60, level: "élevé", estimated_housing_rights_index: 4.76 },
    { id: "HRE-007", name: "France (saturation hébergement)", composite_score: 29.35, level: "modéré", estimated_housing_rights_index: 2.94 },
    { id: "HRE-008", name: "Finlande (Housing First)", composite_score: 9.85, level: "faible", estimated_housing_rights_index: 0.99 }
  ],
  avg_composite: 56.94,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-rights-eviction-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
