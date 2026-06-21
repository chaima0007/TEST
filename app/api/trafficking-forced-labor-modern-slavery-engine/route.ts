import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[trafficking-forced-labor-modern-slavery-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "trafficking_forced_labor_modern_slavery",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "TFM-001", name: "Corée du Nord — Travail forcé d'État export, usines Chine/Russie, 50K-100K workers", composite_score: 94.05, risk_level: "critique", estimated_modern_slavery_index: 9.40 },
    { entity_id: "TFM-002", name: "Qatar FIFA2022 — Kafala, 6500 morts travailleurs migrants, réformes insuffisantes", composite_score: 86.30, risk_level: "critique", estimated_modern_slavery_index: 8.63 },
    { entity_id: "TFM-003", name: "Libye — Marchés aux esclaves 2017, migrants subsahariens, impunité milices", composite_score: 84.30, risk_level: "critique", estimated_modern_slavery_index: 8.43 },
    { entity_id: "TFM-004", name: "Inde briqueteries/pêche — Bonded labour, 8M+ en servitude dette, lois peu appliquées", composite_score: 74.40, risk_level: "critique", estimated_modern_slavery_index: 7.44 },
    { entity_id: "TFM-005", name: "Mexique — Femmes trafiquées cartels, corridors Centramérique-USA", composite_score: 53.20, risk_level: "élevé", estimated_modern_slavery_index: 5.32 },
    { entity_id: "TFM-006", name: "Thaïlande industrie pêche — Travailleurs migrants piégés, ILO rapports", composite_score: 47.20, risk_level: "élevé", estimated_modern_slavery_index: 4.72 },
    { entity_id: "TFM-007", name: "Roumanie/Bulgarie — Trafic intra-UE, jeunes femmes, dispositifs partiels", composite_score: 25.30, risk_level: "modéré", estimated_modern_slavery_index: 2.53 },
    { entity_id: "TFM-008", name: "Suède modèle — Loi 1999 criminalise acheteur, réduction prouvée, réintégration", composite_score: 6.65, risk_level: "faible", estimated_modern_slavery_index: 0.67 },
  ],
  avg_composite: 58.92,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/trafficking-forced-labor-modern-slavery-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
