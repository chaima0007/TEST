import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[press-freedom-journalist-protection-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "press_freedom_journalist_protection",
  total_entities: 8,
  avg_composite: 60.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "PFJ-001",
      name: "Corée du Nord (journalisme d'État)",
      composite_score: 92.60,
      level: "critique",
      estimated_press_freedom_index: 9.26,
    },
    {
      id: "PFJ-002",
      name: "Érythrée (censure totale)",
      composite_score: 86.60,
      level: "critique",
      estimated_press_freedom_index: 8.66,
    },
    {
      id: "PFJ-003",
      name: "Chine (Great Firewall + RSF)",
      composite_score: 83.05,
      level: "critique",
      estimated_press_freedom_index: 8.31,
    },
    {
      id: "PFJ-004",
      name: "Russie (loi 'désinformation' 2022)",
      composite_score: 74.50,
      level: "critique",
      estimated_press_freedom_index: 7.45,
    },
    {
      id: "PFJ-005",
      name: "Turquie (3e emprisonnements)",
      composite_score: 54.35,
      level: "élevé",
      estimated_press_freedom_index: 5.44,
    },
    {
      id: "PFJ-006",
      name: "Iran (journalistes web)",
      composite_score: 49.60,
      level: "élevé",
      estimated_press_freedom_index: 4.96,
    },
    {
      id: "PFJ-007",
      name: "Inde (presse régionale)",
      composite_score: 31.35,
      level: "modéré",
      estimated_press_freedom_index: 3.14,
    },
    {
      id: "PFJ-008",
      name: "Finlande (RSF classement #1)",
      composite_score: 9.35,
      level: "faible",
      estimated_press_freedom_index: 0.94,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/press-freedom-journalist-protection-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
