import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[peasant-rights-small-farmer-displacement-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "peasant-rights-small-farmer-displacement-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "PRF-001", name: "Inde/Suicides Agriculteurs — 300 000 Depuis 1995, Dettes Monsanto, Lois Farm Acts Abrogées", composite_score: 92.85, risk_level: "critique", estimated_peasant_rights_index: 9.29 },
    { id: "PRF-002", name: "Brésil/Amazonie Agribusiness — MST Paysans Tués, Déforestation Droits Territoriaux", composite_score: 86.65, risk_level: "critique", estimated_peasant_rights_index: 8.67 },
    { id: "PRF-003", name: "Honduras/Paysans Palmier Huile — Berta Cáceres Assassinée, Défenseurs Terres Criminalisés", composite_score: 83.65, risk_level: "critique", estimated_peasant_rights_index: 8.37 },
    { id: "PRF-004", name: "Éthiopie/Villagisation Forcée — 1.5M Déplacés Agro-Industrie Étrangère", composite_score: 79.65, risk_level: "critique", estimated_peasant_rights_index: 7.97 },
    { id: "PRF-005", name: "Philippines/CARP Non-Appliqué — Réforme Agraire 1988 Bloquée, Landlordisme Persistant", composite_score: 52.65, risk_level: "élevé", estimated_peasant_rights_index: 5.26 },
    { id: "PRF-006", name: "France/Accaparement Terres Agricoles — Foncier Spéculatif, Jeunes Agriculteurs Exclus", composite_score: 44.65, risk_level: "élevé", estimated_peasant_rights_index: 4.46 },
    { id: "PRF-007", name: "ONU/UNDROP 2018 — Déclaration Droits Paysans, 121 États Votes Pour, Application Partielle", composite_score: 24.65, risk_level: "modéré", estimated_peasant_rights_index: 2.46 },
    { id: "PRF-008", name: "Bolivia/Révolution Agraire Evo Morales — Redistribution 6M Ha, Droits Constitutionnels", composite_score: 8.65, risk_level: "faible", estimated_peasant_rights_index: 0.87 },
  ],
  avg_composite: 59.17,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/peasant-rights-small-farmer-displacement-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
