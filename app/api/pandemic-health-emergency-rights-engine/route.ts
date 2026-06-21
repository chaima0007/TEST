import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[pandemic-health-emergency-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "pandemic_health_emergency_rights",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "PHE-001", name: "Brésil (Bolsonaro COVID response)", composite_score: 89.3, level: "critique", estimated_health_emergency_index: 8.93 },
    { id: "PHE-002", name: "Inde (2021 Delta wave collapse)", composite_score: 84.7, level: "critique", estimated_health_emergency_index: 8.47 },
    { id: "PHE-003", name: "USA (inégalités vaccins COVID)", composite_score: 76.5, level: "critique", estimated_health_emergency_index: 7.65 },
    { id: "PHE-004", name: "Afrique sub-saharienne (accès vaccins)", composite_score: 71.2, level: "critique", estimated_health_emergency_index: 7.12 },
    { id: "PHE-005", name: "Chine (SARS-CoV-2 information)", composite_score: 55.8, level: "élevé", estimated_health_emergency_index: 5.58 },
    { id: "PHE-006", name: "Italie (mars 2020 triage)", composite_score: 43.6, level: "élevé", estimated_health_emergency_index: 4.36 },
    { id: "PHE-007", name: "Espagne (surmortalité EHPAD)", composite_score: 29.4, level: "modéré", estimated_health_emergency_index: 2.94 },
    { id: "PHE-008", name: "Nouvelle-Zélande (Ardern model)", composite_score: 13.8, level: "faible", estimated_health_emergency_index: 1.38 },
  ],
  avg_composite: 58.04,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pandemic-health-emergency-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
