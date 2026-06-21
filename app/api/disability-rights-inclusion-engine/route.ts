import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-inclusion-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "disability_rights_inclusion",
  total_entities: 8,
  avg_composite: 56.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      entity_id: "DRI-001",
      name: "Soudan du Sud (aucun cadre légal)",
      composite_score: 87.90,
      level: "critique",
      estimated_disability_inclusion_index: 8.79,
    },
    {
      entity_id: "DRI-002",
      name: "Haïti (post-séisme, handicapés abandonnés)",
      composite_score: 83.10,
      level: "critique",
      estimated_disability_inclusion_index: 8.31,
    },
    {
      entity_id: "DRI-003",
      name: "Inde (Persons with Disabilities Act insuffisant)",
      composite_score: 75.30,
      level: "critique",
      estimated_disability_inclusion_index: 7.53,
    },
    {
      entity_id: "DRI-004",
      name: "Indonésie (barrières physiques + sociales)",
      composite_score: 67.90,
      level: "critique",
      estimated_disability_inclusion_index: 6.79,
    },
    {
      entity_id: "DRI-005",
      name: "Mexique (application partielle)",
      composite_score: 52.60,
      level: "élevé",
      estimated_disability_inclusion_index: 5.26,
    },
    {
      entity_id: "DRI-006",
      name: "Brésil (LBI 2015 non appliquée)",
      composite_score: 45.30,
      level: "élevé",
      estimated_disability_inclusion_index: 4.53,
    },
    {
      entity_id: "DRI-007",
      name: "France (RQTH insuffisant)",
      composite_score: 27.30,
      level: "modéré",
      estimated_disability_inclusion_index: 2.73,
    },
    {
      entity_id: "DRI-008",
      name: "Suède (modèle universel)",
      composite_score: 10.05,
      level: "faible",
      estimated_disability_inclusion_index: 1.01,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-inclusion-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
