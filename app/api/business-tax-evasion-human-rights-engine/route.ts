import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[business-tax-evasion-human-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "business_tax_evasion_human_rights",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "TAX-001", name: "Panama Papers — offshore networks", composite_score: 88.5, level: "critique", estimated_tax_justice_index: 8.85 },
    { id: "TAX-002", name: "Bermudes/Caïmans multinationales", composite_score: 83.2, level: "critique", estimated_tax_justice_index: 8.32 },
    { id: "TAX-003", name: "Delaware shell companies", composite_score: 79.6, level: "critique", estimated_tax_justice_index: 7.96 },
    { id: "TAX-004", name: "Îles Vierges Britanniques", composite_score: 68.4, level: "critique", estimated_tax_justice_index: 6.84 },
    { id: "TAX-005", name: "Luxembourg (Luxleaks)", composite_score: 52.1, level: "élevé", estimated_tax_justice_index: 5.21 },
    { id: "TAX-006", name: "Pays-Bas (rulings fiscaux)", composite_score: 45.8, level: "élevé", estimated_tax_justice_index: 4.58 },
    { id: "TAX-007", name: "Suisse (secret bancaire résiduel)", composite_score: 32.7, level: "modéré", estimated_tax_justice_index: 3.27 },
    { id: "TAX-008", name: "Norvège (transparence totale)", composite_score: 11.2, level: "faible", estimated_tax_justice_index: 1.12 },
  ],
  avg_composite: 57.69,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/business-tax-evasion-human-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
