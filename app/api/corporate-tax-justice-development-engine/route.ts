import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-tax-justice-development-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "corporate_tax_justice_development",
  generated_at: new Date().toISOString(),
  avg_composite: 58.74,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  entities: [
    {
      entity_id: "CTJ-001",
      name: "Glencore (RDC royalties évitées)",
      composite_score: 87.85,
      risk_level: "critique",
      estimated_tax_justice_index: 8.79,
    },
    {
      entity_id: "CTJ-002",
      name: "Apple/Google (structure irlandaise)",
      composite_score: 84.60,
      risk_level: "critique",
      estimated_tax_justice_index: 8.46,
    },
    {
      entity_id: "CTJ-003",
      name: "Shell (Pays-Bas + Nigeria profit shift)",
      composite_score: 81.85,
      risk_level: "critique",
      estimated_tax_justice_index: 8.19,
    },
    {
      entity_id: "CTJ-004",
      name: "Amazon (Luxembourg structuration)",
      composite_score: 75.60,
      risk_level: "critique",
      estimated_tax_justice_index: 7.56,
    },
    {
      entity_id: "CTJ-005",
      name: "HSBC (filiales offshore)",
      composite_score: 53.70,
      risk_level: "élevé",
      estimated_tax_justice_index: 5.37,
    },
    {
      entity_id: "CTJ-006",
      name: "Starbucks (IP royalties)",
      composite_score: 46.85,
      risk_level: "élevé",
      estimated_tax_justice_index: 4.69,
    },
    {
      entity_id: "CTJ-007",
      name: "Unilever (BEPS pillar 2 partiel)",
      composite_score: 28.65,
      risk_level: "modéré",
      estimated_tax_justice_index: 2.87,
    },
    {
      entity_id: "CTJ-008",
      name: "Danone (B-Corp + transparence)",
      composite_score: 10.85,
      risk_level: "faible",
      estimated_tax_justice_index: 1.09,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-tax-justice-development-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
