import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[anti-personnel-mines-cluster-munitions-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "anti_personnel_mines_cluster_munitions",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "APM-001", name: "Afghanistan — 5.4M km2 contamines, 150+ victimes/an, plus grand parc mines mondial", composite_score: 93.55, risk_level: "critique", estimated_mine_contamination_index: 9.36 },
    { id: "APM-002", name: "Myanmar — Utilisation active mines anti-Rohingya et contexte coup 2021", composite_score: 86.30, risk_level: "critique", estimated_mine_contamination_index: 8.63 },
    { id: "APM-003", name: "Yemen — Guerre Houthis et coalition, cluster munitions interdites utilisees", composite_score: 83.90, risk_level: "critique", estimated_mine_contamination_index: 8.39 },
    { id: "APM-004", name: "Ukraine — Invasion russe 2022, contamination massive est et sud du pays", composite_score: 78.20, risk_level: "critique", estimated_mine_contamination_index: 7.82 },
    { id: "APM-005", name: "Cambodge — Heritage Khmer Rouge, deminage continu depuis 40 ans", composite_score: 51.10, risk_level: "élevé", estimated_mine_contamination_index: 5.11 },
    { id: "APM-006", name: "Colombie — Legacy FARC, mines artisanales zones rurales persistantes", composite_score: 46.40, risk_level: "élevé", estimated_mine_contamination_index: 4.64 },
    { id: "APM-007", name: "Mozambique — Post-guerre civile, deminage avance mais contamination residuelle", composite_score: 22.90, risk_level: "modéré", estimated_mine_contamination_index: 2.29 },
    { id: "APM-008", name: "Allemagne — Traite Ottawa signe, zero stock mines AP, modele de conformite", composite_score: 3.60, risk_level: "faible", estimated_mine_contamination_index: 0.36 },
  ],
  avg_composite: 58.24,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-personnel-mines-cluster-munitions-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
