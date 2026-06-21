import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-surveillance-pegasus-spyware-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "digital-surveillance-pegasus-spyware-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "DSP-001", name: "Mexique/Pegasus Journalistes Défenseurs", composite_score: 92.9, risk_level: "critique", estimated_surveillance_rights_index: 9.29 },
    { id: "DSP-002", name: "Arabie Saoudite/Jamal Khashoggi Pegasus", composite_score: 90.2, risk_level: "critique", estimated_surveillance_rights_index: 9.02 },
    { id: "DSP-003", name: "Inde/Opposition Activistes Ciblés", composite_score: 86.2, risk_level: "critique", estimated_surveillance_rights_index: 8.62 },
    { id: "DSP-004", name: "Azerbaïdjan/Journalistes Emprisonnés Pegasus", composite_score: 81.2, risk_level: "critique", estimated_surveillance_rights_index: 8.12 },
    { id: "DSP-005", name: "France/Macron Ciblé Maroc", composite_score: 53.2, risk_level: "élevé", estimated_surveillance_rights_index: 5.32 },
    { id: "DSP-006", name: "EU/FinFisher Hacking Team", composite_score: 45.2, risk_level: "élevé", estimated_surveillance_rights_index: 4.52 },
    { id: "DSP-007", name: "USA/NSO Group Blacklist 2021", composite_score: 28.2, risk_level: "modéré", estimated_surveillance_rights_index: 2.82 },
    { id: "DSP-008", name: "UE/Règlement IA & Surveillance", composite_score: 9.35, risk_level: "faible", estimated_surveillance_rights_index: 0.94 },
  ],
  avg_composite: 60.81,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/digital-surveillance-pegasus-spyware-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
