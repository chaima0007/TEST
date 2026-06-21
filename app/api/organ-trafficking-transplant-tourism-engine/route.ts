import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[organ-trafficking-transplant-tourism-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "organ-trafficking-transplant-tourism-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "OTT-001", name: "Chine/Prélèvements Organes Prisonniers Conscience", composite_score: 95.2, risk_level: "critique", estimated_organ_trafficking_index: 9.52 },
    { id: "OTT-002", name: "Pakistan/Trafic Reins Pauvres", composite_score: 87.65, risk_level: "critique", estimated_organ_trafficking_index: 8.77 },
    { id: "OTT-003", name: "Égypte/Tourisme Transplant Illégal", composite_score: 83.9, risk_level: "critique", estimated_organ_trafficking_index: 8.39 },
    { id: "OTT-004", name: "Kosovo/Clinique Medicus 2008", composite_score: 78.95, risk_level: "critique", estimated_organ_trafficking_index: 7.89 },
    { id: "OTT-005", name: "Inde/Marché Reins Informel", composite_score: 54.0, risk_level: "élevé", estimated_organ_trafficking_index: 5.4 },
    { id: "OTT-006", name: "Philippines/Trafic Organes Post-Typhon", composite_score: 46.2, risk_level: "élevé", estimated_organ_trafficking_index: 4.62 },
    { id: "OTT-007", name: "Interpol/Op. Lionfish", composite_score: 27.2, risk_level: "modéré", estimated_organ_trafficking_index: 2.72 },
    { id: "OTT-008", name: "Espagne/Modèle Opt-Out Consentement", composite_score: 6.05, risk_level: "faible", estimated_organ_trafficking_index: 0.6 },
  ],
  avg_composite: 59.89,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/organ-trafficking-transplant-tourism-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
