import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[stateless-persons-documentation-crisis-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "stateless-persons-documentation-crisis-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "SDC-001",
      name: "Birmanie/Rohingya — 1M Apatrides, Refus Citoyenneté Loi 1982, Génocide Documenté ONU",
      composite_score: 93.75,
      risk_level: "critique",
      estimated_stateless_documentation_index: 9.38,
    },
    {
      id: "SDC-002",
      name: "Kuwait/Bidoon — 100 000 Résidents Sans Papiers, Droits Fondamentaux Refusés Depuis 1961",
      composite_score: 86.2,
      risk_level: "critique",
      estimated_stateless_documentation_index: 8.62,
    },
    {
      id: "SDC-003",
      name: "Côte d&apos;Ivoire/Dioula — Apatridie Post-Guerre Civile, Actes Naissance Refusés, 700 000 Cas",
      composite_score: 79.55,
      risk_level: "critique",
      estimated_stateless_documentation_index: 7.96,
    },
    {
      id: "SDC-004",
      name: "République Dominicaine/Haïtiens — Arrêt 168-13, Dénationalisation Rétroactive 200 000 Personnes",
      composite_score: 78.75,
      risk_level: "critique",
      estimated_stateless_documentation_index: 7.88,
    },
    {
      id: "SDC-005",
      name: "Lettonie/Non-Citoyens Soviétiques — 200 000 Passeports Gris, Droits Limités UE",
      composite_score: 48.85,
      risk_level: "élevé",
      estimated_stateless_documentation_index: 4.88,
    },
    {
      id: "SDC-006",
      name: "Thaïlande/Highlanders Montagnards — 500K Sans Acte Naissance, Mobilité & Éducation Bloquées",
      composite_score: 46.3,
      risk_level: "élevé",
      estimated_stateless_documentation_index: 4.63,
    },
    {
      id: "SDC-007",
      name: "UNHCR/IBelong Campaign 2024 — Objectif Réduction Apatridie, Progrès Mesuré 10 Pays",
      composite_score: 24.15,
      risk_level: "modéré",
      estimated_stateless_documentation_index: 2.42,
    },
    {
      id: "SDC-008",
      name: "Estonie/Intégration Naturalisation — Modèle Réussite, Non-Citoyens Intégrés, UE Standards",
      composite_score: 7.45,
      risk_level: "faible",
      estimated_stateless_documentation_index: 0.74,
    },
  ],
  avg_composite: 58.12,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/stateless-persons-documentation-crisis-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
