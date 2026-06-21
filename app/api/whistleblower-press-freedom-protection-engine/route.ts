import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[whistleblower-press-freedom-protection-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "whistleblower-press-freedom-protection-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "WPF-001", name: "Mexique/Journalistes Cartels — 15 Tués 2023, Mécanisme Protection Inefficace", composite_score: 89.0, risk_level: "critique", estimated_press_freedom_index: 8.90 },
    { id: "WPF-002", name: "Russie/Loi Anti-Fake News — Journalistes 15 Ans Prison, Médias Indépendants Fermés", composite_score: 93.75, risk_level: "critique", estimated_press_freedom_index: 9.38 },
    { id: "WPF-003", name: "Philippines/Rodrigo Duterte Rappler — Maria Ressa Nobel Harcelée", composite_score: 81.75, risk_level: "critique", estimated_press_freedom_index: 8.18 },
    { id: "WPF-004", name: "Éthiopie/Tigray War Media Blackout — Internet Coupé, Journalistes Expulsés", composite_score: 69.15, risk_level: "critique", estimated_press_freedom_index: 6.92 },
    { id: "WPF-005", name: "UE/SLAPP Lois Bâillon — 570 Cas Documentés, PME Journalisme Menacées", composite_score: 51.25, risk_level: "élevé", estimated_press_freedom_index: 5.13 },
    { id: "WPF-006", name: "USA/Julian Assange 12 Ans Extradition — Espionnage Act, Précédent Dangereux", composite_score: 48.25, risk_level: "élevé", estimated_press_freedom_index: 4.83 },
    { id: "WPF-007", name: "France/Protection Sources Partielle — Loi 2010 Insuffisante, Whistleblowers UE Exposés", composite_score: 28.75, risk_level: "modéré", estimated_press_freedom_index: 2.88 },
    { id: "WPF-008", name: "Islande/International Modern Media Institute — Meilleure Protection Lances-Alertes", composite_score: 11.9, risk_level: "faible", estimated_press_freedom_index: 1.19 },
  ],
  avg_composite: 59.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/whistleblower-press-freedom-protection-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
