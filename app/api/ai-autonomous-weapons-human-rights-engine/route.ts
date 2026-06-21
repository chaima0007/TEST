import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[ai-autonomous-weapons-human-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "ai_autonomous_weapons_human_rights",
  generated_at: new Date().toISOString(),
  avg_composite: 59.76,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "AAW-001",
      name: "Israël (Lavender AI targeting)",
      composite_score: 88.65,
      risk_level: "critique",
      estimated_ai_weapons_index: 8.87,
    },
    {
      id: "AAW-002",
      name: "Chine (LAWS développement accéléré)",
      composite_score: 84.85,
      risk_level: "critique",
      estimated_ai_weapons_index: 8.49,
    },
    {
      id: "AAW-003",
      name: "USA (Project Maven + drone kill chain)",
      composite_score: 81.60,
      risk_level: "critique",
      estimated_ai_weapons_index: 8.16,
    },
    {
      id: "AAW-004",
      name: "Russie (KUB-BLA autonome Ukraine)",
      composite_score: 77.85,
      risk_level: "critique",
      estimated_ai_weapons_index: 7.79,
    },
    {
      id: "AAW-005",
      name: "Turquie (Kargu-2 Libye)",
      composite_score: 58.70,
      risk_level: "élevé",
      estimated_ai_weapons_index: 5.87,
    },
    {
      id: "AAW-006",
      name: "Corée du Sud (Super aEgis II)",
      composite_score: 50.85,
      risk_level: "élevé",
      estimated_ai_weapons_index: 5.09,
    },
    {
      id: "AAW-007",
      name: "UK (drone Reaper humain-dans-boucle)",
      composite_score: 26.75,
      risk_level: "modéré",
      estimated_ai_weapons_index: 2.68,
    },
    {
      id: "AAW-008",
      name: "Autriche (traité ban LAWS)",
      composite_score: 8.85,
      risk_level: "faible",
      estimated_ai_weapons_index: 0.89,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/ai-autonomous-weapons-human-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
