import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-inclusive-development-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "disability-rights-inclusive-development-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "DBR-001", name: "Congo/Personnes Handicapées Mines Antipersonnel — Amputés Sans Prothèses, ONG Manquent", composite_score: 89.75, risk_level: "critique", estimated_disability_rights_index: 8.98 },
    { id: "DBR-002", name: "Afghanistan/Femmes Handicapées Talibans — Double Discrimination, Éducation Interdite", composite_score: 93.5, risk_level: "critique", estimated_disability_rights_index: 9.35 },
    { id: "DBR-003", name: "Inde/Institutionnalisation Forcée Autistes — Chaînes Pratiques Traditionnelles", composite_score: 84.25, risk_level: "critique", estimated_disability_rights_index: 8.43 },
    { id: "DBR-004", name: "USA/Olmstead Act Non-Appliqué — Intégration Communautaire Retardée", composite_score: 67.4, risk_level: "critique", estimated_disability_rights_index: 6.74 },
    { id: "DBR-005", name: "Brésil/Accessibilité Zéro Favelas — 30% Population Exclu Transports", composite_score: 53.25, risk_level: "élevé", estimated_disability_rights_index: 5.33 },
    { id: "DBR-006", name: "Nigeria/Witchcraft Accusations Handicap Mental — Exorcismes Forcés", composite_score: 50.25, risk_level: "élevé", estimated_disability_rights_index: 5.03 },
    { id: "DBR-007", name: "UE/CRPD Ratification Partielle — 12 États Réserves, Progrès Modéré", composite_score: 29.75, risk_level: "modéré", estimated_disability_rights_index: 2.98 },
    { id: "DBR-008", name: "Japon/Universal Design Pioneer — Accessibilité Systémique", composite_score: 13.9, risk_level: "faible", estimated_disability_rights_index: 1.39 },
  ],
  avg_composite: 60.26,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/disability-rights-inclusive-development-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
