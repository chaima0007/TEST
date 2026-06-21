import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[post-quantum-cryptography-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "post-quantum-cryptography-rights-engine",
  generated_at: new Date().toISOString(),
  accent: "#0e7490",
  entities: [
    { id: "PQC-001", name: "Populations Sans Post-Quantum", composite_score: 92.60, risk_level: "critique", estimated_pqc_rights_index: 9.26 },
    { id: "PQC-002", name: "Systèmes Santé Non-Protégés", composite_score: 88.05, risk_level: "critique", estimated_pqc_rights_index: 8.80 },
    { id: "PQC-003", name: "Journalistes/Sources à Risque", composite_score: 88.55, risk_level: "critique", estimated_pqc_rights_index: 8.86 },
    { id: "PQC-004", name: "Infrastructures Critiques RSA", composite_score: 81.65, risk_level: "critique", estimated_pqc_rights_index: 8.16 },
    { id: "PQC-005", name: "Gouvernements Transition Lente", composite_score: 51.70, risk_level: "élevé", estimated_pqc_rights_index: 5.17 },
    { id: "PQC-006", name: "NIST PQC Standards 2024", composite_score: 17.40, risk_level: "faible", estimated_pqc_rights_index: 1.74 },
    { id: "PQC-007", name: "Signal Protocol Post-Quantum", composite_score: 22.60, risk_level: "modéré", estimated_pqc_rights_index: 2.26 },
    { id: "PQC-008", name: "Nations Avancées PQC", composite_score: 40.30, risk_level: "élevé", estimated_pqc_rights_index: 4.03 },
  ],
  avg_composite: 60.36,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/post-quantum-cryptography-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
