import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[stateless-persons-documentation-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "stateless_persons_documentation",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "STP-001", name: "Myanmar Rohingyas — Sans nationalite depuis 1982, 1M+ apatrides, genocide documente", composite_score: 92.90, risk_level: "critique", estimated_statelessness_index: 9.29 },
    { entity_id: "STP-002", name: "Thailande Hill Tribes — 600K sans papiers, acces education et sante refuse", composite_score: 84.65, risk_level: "critique", estimated_statelessness_index: 8.46 },
    { entity_id: "STP-003", name: "Cote d'Ivoire — Apatridie post-conflit, Dioulas sans actes naissance", composite_score: 77.30, risk_level: "critique", estimated_statelessness_index: 7.73 },
    { entity_id: "STP-004", name: "Republique Dominicaine — Haitiens denationalises 2013, arret TC/0168/13", composite_score: 71.00, risk_level: "critique", estimated_statelessness_index: 7.10 },
    { entity_id: "STP-005", name: "Bangladesh chars et haors — Sans-papiers minorites riveraines, zones inondees", composite_score: 53.00, risk_level: "élevé", estimated_statelessness_index: 5.30 },
    { entity_id: "STP-006", name: "Europe apatrides ex-sovietiques — Lettonie/Estonie non-citoyens, russophones", composite_score: 41.30, risk_level: "élevé", estimated_statelessness_index: 4.13 },
    { entity_id: "STP-007", name: "Kenya Nubians — Apatrides historiques depuis ere coloniale, reconnaissance partielle", composite_score: 25.30, risk_level: "modéré", estimated_statelessness_index: 2.53 },
    { entity_id: "STP-008", name: "Portugal — Processus naturalisation rapide, enregistrement naissances universel", composite_score: 6.65, risk_level: "faible", estimated_statelessness_index: 0.67 },
  ],
  avg_composite: 56.51,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/stateless-persons-documentation-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
