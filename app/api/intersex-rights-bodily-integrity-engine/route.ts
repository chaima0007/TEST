import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[intersex-rights-bodily-integrity-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "intersex-rights-bodily-integrity-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "IRB-001", name: "USA/Chirurgies Intersexes Nourrissons — Pratique Courante Sans Consentement, AAP Réticent", composite_score: 90.8, risk_level: "critique", estimated_intersex_rights_index: 9.08 },
    { id: "IRB-002", name: "Allemagne/Interdiction Partielle 2021 — Loi Insuffisante, Exceptions Larges Maintien Pratiques", composite_score: 84.65, risk_level: "critique", estimated_intersex_rights_index: 8.46 },
    { id: "IRB-003", name: "Chine/Intersexes Invisibles — Médicalisation Forcée, Zéro Reconnaissance Légale", composite_score: 81.65, risk_level: "critique", estimated_intersex_rights_index: 8.16 },
    { id: "IRB-004", name: "Afrique du Sud/Chirurgies Normalisantes — Sport Caster Semenya, CAS vs IAAF Droits Bafoués", composite_score: 77.65, risk_level: "critique", estimated_intersex_rights_index: 7.77 },
    { id: "IRB-005", name: "France/Loi Bioéthique 2021 Partielle — Moratoire Non Contraignant, Pratiques Continuent", composite_score: 51.75, risk_level: "élevé", estimated_intersex_rights_index: 5.17 },
    { id: "IRB-006", name: "Australie/Senate Inquiry 2013 — Recommandations Non Appliquées, États Divergents", composite_score: 44.65, risk_level: "élevé", estimated_intersex_rights_index: 4.46 },
    { id: "IRB-007", name: "Malte/Loi GIGESC 2015 — Premier Pays Interdiction Totale, Modèle Mondial", composite_score: 22.05, risk_level: "modéré", estimated_intersex_rights_index: 2.21 },
    { id: "IRB-008", name: "Portugal/Interdiction 2018 Complète — Droits Complets Reconnaissance Légale Genre", composite_score: 6.85, risk_level: "faible", estimated_intersex_rights_index: 0.68 },
  ],
  avg_composite: 57.51,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/intersex-rights-bodily-integrity-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
