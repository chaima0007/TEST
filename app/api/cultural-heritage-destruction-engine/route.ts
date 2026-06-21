import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[cultural-heritage-destruction-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "cultural_heritage_destruction",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "CHD-001", name: "Syrie (Palmyre + Alep bombardés)", composite_score: 92.85, risk_level: "critique", estimated_heritage_protection_index: 9.29 },
    { entity_id: "CHD-002", name: "Irak (Daesh + Mossoul bibliothèque)", composite_score: 89.60, risk_level: "critique", estimated_heritage_protection_index: 8.96 },
    { entity_id: "CHD-003", name: "Mali (Tombouctou mosquées)", composite_score: 82.85, risk_level: "critique", estimated_heritage_protection_index: 8.29 },
    { entity_id: "CHD-004", name: "Yémen (sites UNESCO bombardés)", composite_score: 77.60, risk_level: "critique", estimated_heritage_protection_index: 7.76 },
    { entity_id: "CHD-005", name: "Libye (Cyrène + sites antiques)", composite_score: 56.85, risk_level: "élevé", estimated_heritage_protection_index: 5.69 },
    { entity_id: "CHD-006", name: "Afghanistan (Bamiyan legacy)", composite_score: 51.60, risk_level: "élevé", estimated_heritage_protection_index: 5.16 },
    { entity_id: "CHD-007", name: "Cambodge (pillage khmer legacy)", composite_score: 29.85, risk_level: "modéré", estimated_heritage_protection_index: 2.99 },
    { entity_id: "CHD-008", name: "Grèce (Elgin Marbles process)", composite_score: 12.85, risk_level: "faible", estimated_heritage_protection_index: 1.29 },
  ],
  avg_composite: 62.07,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cultural-heritage-destruction-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
