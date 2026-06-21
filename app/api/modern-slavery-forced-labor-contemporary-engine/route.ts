import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[modern-slavery-forced-labor-contemporary-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "modern-slavery-forced-labor-contemporary-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "MSL-001", name: "Corée du Nord/Travail Forcé Étatique — 2.6M Travailleurs Forcés Camps Kwanliso Exportés Chine Russie", composite_score: 93.30, risk_level: "critique", estimated_modern_slavery_index: 9.33 },
    { id: "MSL-002", name: "Érythrée/Service National Indéfini — Conscription Forcée Vie Entière Salaire $30/Mois Fuite Criminel", composite_score: 87.30, risk_level: "critique", estimated_modern_slavery_index: 8.73 },
    { id: "MSL-003", name: "Mauritanie/Esclavage Héréditaire — 90 000 Esclaves Haratin Nés Esclavage Criminalisation 2007 Impunité", composite_score: 81.30, risk_level: "critique", estimated_modern_slavery_index: 8.13 },
    { id: "MSL-004", name: "Inde/Travail Bonded — 18M Travailleurs Endettés Agriculture Briques Carrières Caste Dalits", composite_score: 73.30, risk_level: "critique", estimated_modern_slavery_index: 7.33 },
    { id: "MSL-005", name: "Qatar/Kafala Mondial — 2M Travailleurs Migrants Passeport Confisqué Réforme 2021 Partielle FIFA", composite_score: 57.90, risk_level: "élevé", estimated_modern_slavery_index: 5.79 },
    { id: "MSL-006", name: "UAE/Kafala Construction — 500 000 Travailleurs Domestiques Exclus Labour Law Abus Dénoncés", composite_score: 49.90, risk_level: "élevé", estimated_modern_slavery_index: 4.99 },
    { id: "MSL-007", name: "Brésil/Trabalho Escravo — Opération Liberdade 3 000 Libérés/An Agriculture Textile Liste Suja", composite_score: 33.50, risk_level: "modéré", estimated_modern_slavery_index: 3.35 },
    { id: "MSL-008", name: "Portugal/Plan Anti-Traite — Décriminalisation Victimes Accès Justice Réseau Support ONG", composite_score: 13.90, risk_level: "faible", estimated_modern_slavery_index: 1.39 },
  ],
  avg_composite: 61.30,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/modern-slavery-forced-labor-contemporary-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
