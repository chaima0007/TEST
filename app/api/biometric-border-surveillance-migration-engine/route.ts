import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[biometric-border-surveillance-migration-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "biometric-border-surveillance-migration-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "BBM-001",
      name: "Libye / Gardes-Côtes — Interceptions EU-Financées, Torture Centres Détention, 15 000 Migrants/an, ONU Crimes Contre Humanité",
      composite_score: 90.7,
      risk_level: "critique",
      estimated_border_rights_index: 9.07,
    },
    {
      id: "BBM-002",
      name: "Grèce / Pushbacks Égée — Opérations Frontex Illégales, Noyades Documentées, Condamnation CEDH, Rapport ONU 2023",
      composite_score: 81.9,
      risk_level: "critique",
      estimated_border_rights_index: 8.19,
    },
    {
      id: "BBM-003",
      name: "USA / CBP Frontière Sud — Séparation Familles, Biométrie HART, Cages Enfants, Température Létale Désert Arizona",
      composite_score: 77.95,
      risk_level: "critique",
      estimated_border_rights_index: 7.80,
    },
    {
      id: "BBM-004",
      name: "Turquie / Frontière Syrie-Iran — Refoulements Violents, Tirs Gardes-Frontière, 500 000 Expulsés, Murs Financés EU",
      composite_score: 73.6,
      risk_level: "critique",
      estimated_border_rights_index: 7.36,
    },
    {
      id: "BBM-005",
      name: "Hongrie / Clôture Serbie — Transit Zones Illégales CJUE, Détention Systématique, Orbán Anti-Migration",
      composite_score: 52.9,
      risk_level: "élevé",
      estimated_border_rights_index: 5.29,
    },
    {
      id: "BBM-006",
      name: "Australie / Offshore Processing — Manus Island, Nauru, Détention Indéfinie, Suicides, Coût 400k$/Personne/an",
      composite_score: 46.8,
      risk_level: "élevé",
      estimated_border_rights_index: 4.68,
    },
    {
      id: "BBM-007",
      name: "Canada / Safe Third Country USA — Accord STCA, Refoulements Vers USA, Critiques UNHCR, Réforme 2023 Partielle",
      composite_score: 26.85,
      risk_level: "modéré",
      estimated_border_rights_index: 2.69,
    },
    {
      id: "BBM-008",
      name: "Allemagne / Système EUAA — Procédures Asile Rapides, BAMF Critiqué Qualité, Réforme EU Pacte Asile 2024",
      composite_score: 8.0,
      risk_level: "faible",
      estimated_border_rights_index: 0.80,
    },
  ],
  avg_composite: 57.34,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/biometric-border-surveillance-migration-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
