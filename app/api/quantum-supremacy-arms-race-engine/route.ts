import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-supremacy-arms-race-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "quantum-supremacy-arms-race-engine",
  generated_at: new Date().toISOString(),
  accent: "#b45309",
  entities: [
    { id: "QSA-001", name: "Chine/Quantum Leap", composite_score: 88.10, risk_level: "critique", estimated_quantum_supremacy_rights_index: 8.81 },
    { id: "QSA-002", name: "USA/IBM-Google Race", composite_score: 77.15, risk_level: "critique", estimated_quantum_supremacy_rights_index: 7.72 },
    { id: "QSA-003", name: "Course Militaire Quantum", composite_score: 89.30, risk_level: "critique", estimated_quantum_supremacy_rights_index: 8.93 },
    { id: "QSA-004", name: "Monopolisation Brevets", composite_score: 78.65, risk_level: "critique", estimated_quantum_supremacy_rights_index: 7.87 },
    { id: "QSA-005", name: "UE/Quantum Flagship", composite_score: 43.60, risk_level: "élevé", estimated_quantum_supremacy_rights_index: 4.36 },
    { id: "QSA-006", name: "Pays Émergents Exclus", composite_score: 49.70, risk_level: "élevé", estimated_quantum_supremacy_rights_index: 4.97 },
    { id: "QSA-007", name: "Canada/Quantum Safe", composite_score: 22.90, risk_level: "modéré", estimated_quantum_supremacy_rights_index: 2.29 },
    { id: "QSA-008", name: "CERN/Quantum Science", composite_score: 8.80, risk_level: "faible", estimated_quantum_supremacy_rights_index: 0.88 },
  ],
  avg_composite: 57.28,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/quantum-supremacy-arms-race-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
