import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[kafala-migrant-domestic-workers-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "kafala-migrant-domestic-workers-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "KMD-001", name: "Arabie Saoudite/Kafala 2.5M Travailleurs — Passeports Confisqués, Esclavage Légal", composite_score: 92.75, risk_level: "critique", estimated_kafala_migrant_index: 9.28 },
    { id: "KMD-002", name: "Qatar/Coupe 2022 Migrants Morts — 6 500 Morts Chantier", composite_score: 94.75, risk_level: "critique", estimated_kafala_migrant_index: 9.48 },
    { id: "KMD-003", name: "Liban/Travailleuses Éthiopiennes — Vidéos Abandons Aéroport, Suicide Prévalent", composite_score: 85.75, risk_level: "critique", estimated_kafala_migrant_index: 8.58 },
    { id: "KMD-004", name: "UAE/Philippines OFW Exploitation — Salaires Volés, Aucun Recours Légal", composite_score: 70.4, risk_level: "critique", estimated_kafala_migrant_index: 7.04 },
    { id: "KMD-005", name: "Jordanie/Réforme Kafala Partielle — 660K Travailleurs, Améliorations Limitées", composite_score: 52.4, risk_level: "élevé", estimated_kafala_migrant_index: 5.24 },
    { id: "KMD-006", name: "Bahreïn/Corridor Migration — Réformes 2021 Inégalement Appliquées", composite_score: 47.4, risk_level: "élevé", estimated_kafala_migrant_index: 4.74 },
    { id: "KMD-007", name: "Oman/Kafala Progressif — Changement Patronal Autorisé Partiellement", composite_score: 29.75, risk_level: "modéré", estimated_kafala_migrant_index: 2.98 },
    { id: "KMD-008", name: "Canada/Caregiver Pathway — Droits Résidence Domestiques Étrangers", composite_score: 12.9, risk_level: "faible", estimated_kafala_migrant_index: 1.29 },
  ],
  avg_composite: 60.76,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/kafala-migrant-domestic-workers-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
