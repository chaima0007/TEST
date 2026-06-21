import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-testing-radiation-victims-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "nuclear-testing-radiation-victims-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "NRV-001",
      name: "Marshall Islands/Bikini Atoll — 67 Tests USA, Population Déplacée, Contamination Perpétuelle",
      composite_score: 93.5,
      risk_level: "critique",
      estimated_nuclear_radiation_victims_index: 9.35,
    },
    {
      id: "NRV-002",
      name: "Kazakhstan/Semipalatinsk — 456 Tests URSS, 1.5M Victimes, Pathologies Héréditaires",
      composite_score: 91.25,
      risk_level: "critique",
      estimated_nuclear_radiation_victims_index: 9.12,
    },
    {
      id: "NRV-003",
      name: "Algérie/Reggane Sahara — 17 Tests France Coloniale, Victimes Touareg Sans Reconnaissance",
      composite_score: 88.1,
      risk_level: "critique",
      estimated_nuclear_radiation_victims_index: 8.81,
    },
    {
      id: "NRV-004",
      name: "Polynésie Française/Mururoa — 193 Tests France, Cancers Vétérans, Dissimulation État",
      composite_score: 84.4,
      risk_level: "critique",
      estimated_nuclear_radiation_victims_index: 8.44,
    },
    {
      id: "NRV-005",
      name: "Nevada/Downwinders — Autochtones Shoshone Exposés, Cancer Thyroïde, Justice Partielle",
      composite_score: 54.15,
      risk_level: "élevé",
      estimated_nuclear_radiation_victims_index: 5.42,
    },
    {
      id: "NRV-006",
      name: "Australie/Maralinga — Tests Britanniques, Aborigènes Anangu Exposés, Nettoyage Incomplet",
      composite_score: 53.45,
      risk_level: "élevé",
      estimated_nuclear_radiation_victims_index: 5.34,
    },
    {
      id: "NRV-007",
      name: "Japan/Hibakusha Hiroshima Nagasaki — Survivants Atomiques, Soutien Médical, Témoignage TPNW",
      composite_score: 24.0,
      risk_level: "modéré",
      estimated_nuclear_radiation_victims_index: 2.4,
    },
    {
      id: "NRV-008",
      name: "Treaty on Prohibition Nuclear Weapons TPNW 2021 — Modèle Réparation & Assistance Victimes",
      composite_score: 7.0,
      risk_level: "faible",
      estimated_nuclear_radiation_victims_index: 0.7,
    },
  ],
  avg_composite: 61.98,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-testing-radiation-victims-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
