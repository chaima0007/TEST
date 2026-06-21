import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[refugees-asylum-seekers-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "refugees_asylum_seekers_rights",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "REF-001", name: "Bangladesh (Rohingya camps)", composite_score: 91.5, level: "critique", estimated_refugee_protection_index: 9.15 },
    { id: "REF-002", name: "Liban (réfugiés syriens)", composite_score: 82.3, level: "critique", estimated_refugee_protection_index: 8.23 },
    { id: "REF-003", name: "Turquie (3.6M réfugiés)", composite_score: 78.4, level: "critique", estimated_refugee_protection_index: 7.84 },
    { id: "REF-004", name: "Kenya (camp Dadaab)", composite_score: 65.2, level: "critique", estimated_refugee_protection_index: 6.52 },
    { id: "REF-005", name: "Grèce (îles Égée)", composite_score: 51.8, level: "élevé", estimated_refugee_protection_index: 5.18 },
    { id: "REF-006", name: "Australie (offshore)", composite_score: 48.6, level: "élevé", estimated_refugee_protection_index: 4.86 },
    { id: "REF-007", name: "Mexique (transit)", composite_score: 31.4, level: "modéré", estimated_refugee_protection_index: 3.14 },
    { id: "REF-008", name: "Canada (IRPA)", composite_score: 12.5, level: "faible", estimated_refugee_protection_index: 1.25 },
  ],
  avg_composite: 57.71,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugees-asylum-seekers-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
