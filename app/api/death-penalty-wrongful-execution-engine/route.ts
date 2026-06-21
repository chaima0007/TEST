import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[death-penalty-wrongful-execution-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "death-penalty-wrongful-execution-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "DPW-001", name: "Chine/10 000 Exécutions/An Estimées", composite_score: 94.2, risk_level: "critique", estimated_death_penalty_index: 9.42 },
    { id: "DPW-002", name: "Iran/Mineurs Exécutés", composite_score: 89.2, risk_level: "critique", estimated_death_penalty_index: 8.92 },
    { id: "DPW-003", name: "Arabie Saoudite/Décapitations Publiques", composite_score: 85.2, risk_level: "critique", estimated_death_penalty_index: 8.52 },
    { id: "DPW-004", name: "USA/Innocents Dans Couloir Mort", composite_score: 78.2, risk_level: "critique", estimated_death_penalty_index: 7.82 },
    { id: "DPW-005", name: "Singapour/Peine Mort Trafic Drogue", composite_score: 55.2, risk_level: "élevé", estimated_death_penalty_index: 5.52 },
    { id: "DPW-006", name: "Japon/Peine Mort Secrète", composite_score: 47.2, risk_level: "élevé", estimated_death_penalty_index: 4.72 },
    { id: "DPW-007", name: "UE/Abolition Totale", composite_score: 22.2, risk_level: "modéré", estimated_death_penalty_index: 2.22 },
    { id: "DPW-008", name: "Rwanda/Abolition Post-Génocide", composite_score: 7.35, risk_level: "faible", estimated_death_penalty_index: 0.73 },
  ],
  avg_composite: 59.84,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/death-penalty-wrongful-execution-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
