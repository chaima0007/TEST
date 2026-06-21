import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[internet-freedom-digital-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "internet-freedom-digital-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "IFD-001", name: "Corée du Nord (internet = intranet)", composite_score: 97.85, level: "critique", estimated_internet_freedom_index: 9.79 },
    { id: "IFD-002", name: "Chine (Great Firewall niveau maximal)", composite_score: 94.75, level: "critique", estimated_internet_freedom_index: 9.48 },
    { id: "IFD-003", name: "Iran (filtrage + shutdown 2022)", composite_score: 82.65, level: "critique", estimated_internet_freedom_index: 8.27 },
    { id: "IFD-004", name: "Russie (Runet + blocages 2022-2024)", composite_score: 75.45, level: "critique", estimated_internet_freedom_index: 7.55 },
    { id: "IFD-005", name: "Myanmar (shutdowns militaires)", composite_score: 58.90, level: "élevé", estimated_internet_freedom_index: 5.89 },
    { id: "IFD-006", name: "Inde (shutdowns Cachemire)", composite_score: 46.70, level: "élevé", estimated_internet_freedom_index: 4.67 },
    { id: "IFD-007", name: "France (surveillance LPMPM)", composite_score: 24.85, level: "modéré", estimated_internet_freedom_index: 2.49 },
    { id: "IFD-008", name: "Islande (liberté numérique totale)", composite_score: 7.95, level: "faible", estimated_internet_freedom_index: 0.80 },
  ],
  avg_composite: 61.14,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/internet-freedom-digital-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
