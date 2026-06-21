import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[minority-language-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "minority_language_rights",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "MLR-001",
      name: "Chine (tibétain + ouïghour réprimés)",
      composite_score: 87.65,
      risk_level: "critique",
      estimated_minority_language_index: 8.77,
    },
    {
      id: "MLR-002",
      name: "Turquie (kurde réprimé)",
      composite_score: 84.80,
      risk_level: "critique",
      estimated_minority_language_index: 8.48,
    },
    {
      id: "MLR-003",
      name: "Myanmar (langues Karen + Shan)",
      composite_score: 77.45,
      risk_level: "critique",
      estimated_minority_language_index: 7.75,
    },
    {
      id: "MLR-004",
      name: "Lettonie (russe post-Soviet)",
      composite_score: 64.85,
      risk_level: "critique",
      estimated_minority_language_index: 6.49,
    },
    {
      id: "MLR-005",
      name: "Espagne (catalan conflit)",
      composite_score: 51.90,
      risk_level: "élevé",
      estimated_minority_language_index: 5.19,
    },
    {
      id: "MLR-006",
      name: "France (langues régionales)",
      composite_score: 47.70,
      risk_level: "élevé",
      estimated_minority_language_index: 4.77,
    },
    {
      id: "MLR-007",
      name: "Canada (Charte langues officielles)",
      composite_score: 25.65,
      risk_level: "modéré",
      estimated_minority_language_index: 2.57,
    },
    {
      id: "MLR-008",
      name: "Suisse (4 langues officielles)",
      composite_score: 10.85,
      risk_level: "faible",
      estimated_minority_language_index: 1.09,
    },
  ],
  avg_composite: 56.36,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/minority-language-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
