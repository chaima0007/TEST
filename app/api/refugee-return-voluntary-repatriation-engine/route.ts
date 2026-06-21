import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-return-voluntary-repatriation-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "refugee_return_voluntary_repatriation",
  generated_at: new Date().toISOString(),
  avg_composite: 59.34,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  entities: [
    {
      id: "RVR-001",
      name: "Syrie (retours forcés depuis Liban)",
      composite_score: 91.30,
      risk_level: "critique",
      estimated_refugee_return_index: 9.13,
    },
    {
      id: "RVR-002",
      name: "Afghanistan (Taliban 2021+)",
      composite_score: 86.85,
      risk_level: "critique",
      estimated_refugee_return_index: 8.69,
    },
    {
      id: "RVR-003",
      name: "Myanmar (Rohingya — aucune condition)",
      composite_score: 82.60,
      risk_level: "critique",
      estimated_refugee_return_index: 8.26,
    },
    {
      id: "RVR-004",
      name: "Éthiopie (Tigré post-conflit)",
      composite_score: 72.10,
      risk_level: "critique",
      estimated_refugee_return_index: 7.21,
    },
    {
      id: "RVR-005",
      name: "Sud-Soudan (insécurité persistante)",
      composite_score: 54.65,
      risk_level: "élevé",
      estimated_refugee_return_index: 5.47,
    },
    {
      id: "RVR-006",
      name: "RDC (est instable)",
      composite_score: 47.85,
      risk_level: "élevé",
      estimated_refugee_return_index: 4.79,
    },
    {
      id: "RVR-007",
      name: "Kosovo (retours supervisés UNHCR)",
      composite_score: 27.75,
      risk_level: "modéré",
      estimated_refugee_return_index: 2.78,
    },
    {
      id: "RVR-008",
      name: "Bosnia (Dayton Agreement model)",
      composite_score: 11.65,
      risk_level: "faible",
      estimated_refugee_return_index: 1.17,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-return-voluntary-repatriation-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
