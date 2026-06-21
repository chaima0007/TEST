import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[anti-money-laundering-human-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "anti_money_laundering_human_rights",
  generated_at: new Date().toISOString(),
  avg_composite: 59.86,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  entities: [
    {
      entity_id: "AML-001",
      name: "Corée du Nord (financement nucléaire)",
      composite_score: 91.30,
      risk_level: "critique",
      estimated_aml_rights_index: 9.13,
    },
    {
      entity_id: "AML-002",
      name: "Îles Caïmans (paradis blanchiment)",
      composite_score: 86.85,
      risk_level: "critique",
      estimated_aml_rights_index: 8.69,
    },
    {
      entity_id: "AML-003",
      name: "Russie (oligarques post-sanctions)",
      composite_score: 83.30,
      risk_level: "critique",
      estimated_aml_rights_index: 8.33,
    },
    {
      entity_id: "AML-004",
      name: "Venezuela (narco-État)",
      composite_score: 78.10,
      risk_level: "critique",
      estimated_aml_rights_index: 7.81,
    },
    {
      entity_id: "AML-005",
      name: "Panama (Pandora Papers legacy)",
      composite_score: 54.65,
      risk_level: "élevé",
      estimated_aml_rights_index: 5.47,
    },
    {
      entity_id: "AML-006",
      name: "Émirats Arabes Unis (or + crypto)",
      composite_score: 47.85,
      risk_level: "élevé",
      estimated_aml_rights_index: 4.79,
    },
    {
      entity_id: "AML-007",
      name: "Luxembourg (rulings fiscaux résiduels)",
      composite_score: 27.00,
      risk_level: "modéré",
      estimated_aml_rights_index: 2.70,
    },
    {
      entity_id: "AML-008",
      name: "Suisse post-FATF",
      composite_score: 9.85,
      risk_level: "faible",
      estimated_aml_rights_index: 0.99,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-money-laundering-human-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
