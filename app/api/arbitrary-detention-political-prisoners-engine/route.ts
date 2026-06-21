import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[arbitrary-detention-political-prisoners-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "arbitrary_detention_political_prisoners",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "ADP-001", name: "Chine Xinjiang — 1M+ internés camps formation, procès inexistants, surveillance totale", composite_score: 95.30, risk_level: "critique", estimated_arbitrary_detention_index: 9.53 },
    { entity_id: "ADP-002", name: "Corée du Nord — Goulags politiques, 3 générations punies, 80K-120K détenus", composite_score: 94.35, risk_level: "critique", estimated_arbitrary_detention_index: 9.44 },
    { entity_id: "ADP-003", name: "Russie — Opposants depuis 2022, Navalny mort, milliers détenus manifestants", composite_score: 79.30, risk_level: "critique", estimated_arbitrary_detention_index: 7.93 },
    { entity_id: "ADP-004", name: "Iran — Depuis 2009 Green Movement, 2022 Mahsa Amini, 15K+ détenus", composite_score: 73.20, risk_level: "critique", estimated_arbitrary_detention_index: 7.32 },
    { entity_id: "ADP-005", name: "Venezuela Maduro — Opposants, journalistes, militaires dissidents, 300+ pol.", composite_score: 53.30, risk_level: "élevé", estimated_arbitrary_detention_index: 5.33 },
    { entity_id: "ADP-006", name: "Belarus Loukachenko — 15K+ post-2020, torture systématique, Viasna", composite_score: 49.60, risk_level: "élevé", estimated_arbitrary_detention_index: 4.96 },
    { entity_id: "ADP-007", name: "Egypte — 60K+ prisonniers politiques estimés, processus judiciaires limités", composite_score: 29.20, risk_level: "modéré", estimated_arbitrary_detention_index: 2.92 },
    { entity_id: "ADP-008", name: "Finlande — 0 prisonnier politique, accès CICR total, HRC monitoring ouvert", composite_score: 4.05, risk_level: "faible", estimated_arbitrary_detention_index: 0.41 },
  ],
  avg_composite: 59.79,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/arbitrary-detention-political-prisoners-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
