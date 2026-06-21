import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[religious-freedom-persecution-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "religious-freedom-persecution-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "RFP-001", name: "Chine (Ouïghours + Falun Gong)", composite_score: 92.55, level: "critique", estimated_religious_freedom_index: 9.26 },
    { entity_id: "RFP-002", name: "Corée du Nord (religion interdite)", composite_score: 90.80, level: "critique", estimated_religious_freedom_index: 9.08 },
    { entity_id: "RFP-003", name: "Arabie Saoudite (blasphème/apostasie)", composite_score: 83.65, level: "critique", estimated_religious_freedom_index: 8.37 },
    { entity_id: "RFP-004", name: "Myanmar (minorités religieuses)", composite_score: 72.40, level: "critique", estimated_religious_freedom_index: 7.24 },
    { entity_id: "RFP-005", name: "Pakistan (loi blasphème 295-C)", composite_score: 55.90, level: "élevé", estimated_religious_freedom_index: 5.59 },
    { entity_id: "RFP-006", name: "Égypte (coptes discriminés)", composite_score: 47.80, level: "élevé", estimated_religious_freedom_index: 4.78 },
    { entity_id: "RFP-007", name: "France (laïcité conflictuelle)", composite_score: 26.15, level: "modéré", estimated_religious_freedom_index: 2.62 },
    { entity_id: "RFP-008", name: "Canada (pluralisme religieux)", composite_score: 10.65, level: "faible", estimated_religious_freedom_index: 1.07 }
  ],
  avg_composite: 60.11,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/religious-freedom-persecution-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
