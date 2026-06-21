import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[icc-universal-jurisdiction-impunity-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "icc-universal-jurisdiction-impunity-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "IUJ-001",
      name: "Russie / Ukraine — 30 Mandats CPI Putin-Lvova-Belova, Crimes Guerre Documentés, Tribunal Spécial Crime Agression Requis",
      composite_score: 92.35,
      risk_level: "critique",
      estimated_impunity_accountability_index: 9.24,
    },
    {
      id: "IUJ-002",
      name: "Myanmar / Tatmadaw Junta — Génocide Rohingya ICJ, Crimes Contre Humanité CPI, Coup 2021 Min Aung Hlaing",
      composite_score: 88.2,
      risk_level: "critique",
      estimated_impunity_accountability_index: 8.82,
    },
    {
      id: "IUJ-003",
      name: "Israël-Palestine — Mandat CPI Netanyahu-Gallant, Ordonnance ICJ Génocide Provisoire, 40 000 Morts Gaza",
      composite_score: 84.25,
      risk_level: "critique",
      estimated_impunity_accountability_index: 8.43,
    },
    {
      id: "IUJ-004",
      name: "Soudan / El-Béchir — 1er Mandat CPI Chef État, RSF Darfour Génocide 2023, 25 Ans Impunité, Khalifa Haftar",
      composite_score: 76.05,
      risk_level: "critique",
      estimated_impunity_accountability_index: 7.61,
    },
    {
      id: "IUJ-005",
      name: "Syrie / Assad — Rapport IIIM Preuves Crimes Guerre, Hors CPI Pas Membre, Tribunaux Nationaux Partiels",
      composite_score: 53.95,
      risk_level: "élevé",
      estimated_impunity_accountability_index: 5.40,
    },
    {
      id: "IUJ-006",
      name: "Venezuela / Maduro — Enquête CPI Préliminaire Art. 53, Crimes Contre Humanité SEBIN, Guaidó Limites",
      composite_score: 47.0,
      risk_level: "élevé",
      estimated_impunity_accountability_index: 4.70,
    },
    {
      id: "IUJ-007",
      name: "Espagne / UJ Pinochet-Ruanda — Garzón Précédent, Réforme 2009 Réduction Portée, Modèle Limité Par Pression Diplomatique",
      composite_score: 27.6,
      risk_level: "modéré",
      estimated_impunity_accountability_index: 2.76,
    },
    {
      id: "IUJ-008",
      name: "Allemagne / UJ Syriens — Procès Anwar Raslan Condamné Torture, Code Crimes Internationaux VStGB, Modèle Mondial",
      composite_score: 9.95,
      risk_level: "faible",
      estimated_impunity_accountability_index: 1.00,
    },
  ],
  avg_composite: 59.92,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/icc-universal-jurisdiction-impunity-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
