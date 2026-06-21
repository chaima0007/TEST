import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-pay-gap-economic-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "gender_pay_gap_economic_rights",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "GPG-001", name: "Yémen (femmes < 6% workforce)", composite_score: 90.85, risk_level: "critique", estimated_gender_equity_index: 9.09 },
    { entity_id: "GPG-002", name: "Pakistan (25% gap + exclusion)", composite_score: 84.60, risk_level: "critique", estimated_gender_equity_index: 8.46 },
    { entity_id: "GPG-003", name: "Inde (rural gender gap)", composite_score: 77.85, risk_level: "critique", estimated_gender_equity_index: 7.79 },
    { entity_id: "GPG-004", name: "Égypte (lois héritage inégales)", composite_score: 71.60, risk_level: "critique", estimated_gender_equity_index: 7.16 },
    { entity_id: "GPG-005", name: "Mexique (maquiladoras gap)", composite_score: 54.65, risk_level: "élevé", estimated_gender_equity_index: 5.47 },
    { entity_id: "GPG-006", name: "USA (78 cents gap)", composite_score: 46.85, risk_level: "élevé", estimated_gender_equity_index: 4.69 },
    { entity_id: "GPG-007", name: "France (16% gap résiduel)", composite_score: 27.75, risk_level: "modéré", estimated_gender_equity_index: 2.78 },
    { entity_id: "GPG-008", name: "Islande (5% gap loi égalité)", composite_score: 9.85, risk_level: "faible", estimated_gender_equity_index: 0.99 },
  ],
  avg_composite: 58.00,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/gender-pay-gap-economic-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
