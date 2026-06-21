import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[toxic-waste-environmental-racism-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "toxic-waste-environmental-racism-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "TWR-001",
      name: "Inde/Bhopal Union Carbide 40 Ans Impunité — 15 000 Morts 500 000 Intoxiqués Site Non-Décontaminé Dow Chemical Fuit",
      composite_score: 94.45,
      risk_level: "critique",
      estimated_environmental_racism_index: 9.45,
    },
    {
      id: "TWR-002",
      name: "Nigeria/Delta Niger Shell-Eni 50 Ans Déversements — 1.5M Barils Pétrole Ogoni Terres Détruites Ken Saro-Wiwa Exécuté",
      composite_score: 91.0,
      risk_level: "critique",
      estimated_environmental_racism_index: 9.10,
    },
    {
      id: "TWR-003",
      name: "USA/Cancer Alley Louisiane Majorité Noire — 150 Usines Pétrochimiques Air Cancérigène 50x Normes EJ Mapping EPA",
      composite_score: 83.3,
      risk_level: "critique",
      estimated_environmental_racism_index: 8.33,
    },
    {
      id: "TWR-004",
      name: "Zambie/Kabwe Plomb Enfants Vedanta — Mine Fermée 1994 Plombémie Enfants 10x OMS Procès UK Vedanta 2021",
      composite_score: 82.8,
      risk_level: "critique",
      estimated_environmental_racism_index: 8.28,
    },
    {
      id: "TWR-005",
      name: "Ghana/Agbogbloshie E-Waste 40 000 Travailleurs — Déchets Électroniques Europe USA Cancer Plomb Cadmium Sans Protection",
      composite_score: 53.6,
      risk_level: "élevé",
      estimated_environmental_racism_index: 5.36,
    },
    {
      id: "TWR-006",
      name: "Chili/Quintero Ventanas Zone Sacrifice Communautés Pauvres — 26 Industries Intoxications Scolaires Protestas 2018",
      composite_score: 51.6,
      risk_level: "élevé",
      estimated_environmental_racism_index: 5.16,
    },
    {
      id: "TWR-007",
      name: "Philippines/Mindanao Mines Or Cyanure — Communautés Lumad Déplacées Rivières Contaminées Militarisation Zones Minières",
      composite_score: 28.9,
      risk_level: "modéré",
      estimated_environmental_racism_index: 2.89,
    },
    {
      id: "TWR-008",
      name: "Danemark/Green Transition Déchets Zéro Modèle — Waste-to-Energy 99% Recyclage Objectif 2030 Responsabilité Étendue",
      composite_score: 3.55,
      risk_level: "faible",
      estimated_environmental_racism_index: 0.36,
    },
  ],
  avg_composite: 61.15,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/toxic-waste-environmental-racism-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
