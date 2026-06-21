import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-surveillance-privacy-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "quantum-surveillance-privacy-rights-engine",
  generated_at: new Date().toISOString(),
  accent: "#7c3aed",
  entities: [
    { id: "QSP-001", name: "Chine/Quantum Radar & Satellite", composite_score: 92.55, risk_level: "critique", estimated_quantum_surveillance_rights_index: 9.25 },
    { id: "QSP-002", name: "USA/NSA Quantum", composite_score: 81.10, risk_level: "critique", estimated_quantum_surveillance_rights_index: 8.11 },
    { id: "QSP-003", name: "Russie/FSB Quantum", composite_score: 83.05, risk_level: "critique", estimated_quantum_surveillance_rights_index: 8.30 },
    { id: "QSP-004", name: "Israël/Unit 8200 Quantum", composite_score: 82.90, risk_level: "critique", estimated_quantum_surveillance_rights_index: 8.29 },
    { id: "QSP-005", name: "UE/GDPR Quantum Gap", composite_score: 50.05, risk_level: "élevé", estimated_quantum_surveillance_rights_index: 5.00 },
    { id: "QSP-006", name: "Inde/DRDO Quantum", composite_score: 50.40, risk_level: "élevé", estimated_quantum_surveillance_rights_index: 5.04 },
    { id: "QSP-007", name: "Canada/Quantum Valley", composite_score: 30.05, risk_level: "modéré", estimated_quantum_surveillance_rights_index: 3.00 },
    { id: "QSP-008", name: "ISO/IEC Quantum Privacy", composite_score: 11.35, risk_level: "faible", estimated_quantum_surveillance_rights_index: 1.13 },
  ],
  avg_composite: 60.18,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/quantum-surveillance-privacy-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
