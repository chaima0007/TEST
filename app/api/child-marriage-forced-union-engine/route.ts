import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[child-marriage-forced-union-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "child-marriage-forced-union-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "CMF-001", name: "Niger (75% filles avant 18 ans)", composite_score: 92.50, level: "critique", estimated_child_marriage_index: 9.25 },
    { id: "CMF-002", name: "République Centrafricaine (52% prévalence)", composite_score: 86.80, level: "critique", estimated_child_marriage_index: 8.68 },
    { id: "CMF-003", name: "Bangladesh (59% prévalence rurale)", composite_score: 79.60, level: "critique", estimated_child_marriage_index: 7.96 },
    { id: "CMF-004", name: "Mali (52% zones sahéliennes)", composite_score: 72.40, level: "critique", estimated_child_marriage_index: 7.24 },
    { id: "CMF-005", name: "Inde (27% taux national)", composite_score: 54.70, level: "élevé", estimated_child_marriage_index: 5.47 },
    { id: "CMF-006", name: "Éthiopie (40% régions rurales)", composite_score: 47.50, level: "élevé", estimated_child_marriage_index: 4.75 },
    { id: "CMF-007", name: "Turquie (15% zones rurales)", composite_score: 28.90, level: "modéré", estimated_child_marriage_index: 2.89 },
    { id: "CMF-008", name: "Suède (droit strict + enforcement)", composite_score: 8.80, level: "faible", estimated_child_marriage_index: 0.88 },
  ],
  avg_composite: 59.12,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-marriage-forced-union-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
