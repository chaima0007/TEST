import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[forced-marriage-honor-violence-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "forced-marriage-honor-violence-engine",
  generated_at: new Date().toISOString(),
  avg_composite: 57.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    {
      id: "FMH-001",
      name: "Pakistan/Khyber-Pakhtunkhwa Crimes Honneur — 1000+ Féminicides/An Jirga Tribunaux Coutumiers Karo-Kari Impunité Policière",
      composite_score: 92.4,
      risk_level: "critique",
      estimated_forced_marriage_honor_violence_index: 9.24,
    },
    {
      id: "FMH-002",
      name: "Bangladesh/Mariage Enfants 59% Filles — Plus Haut Taux Asie Dot Violence Économique Violence Conjugale Fatwa",
      composite_score: 86.7,
      risk_level: "critique",
      estimated_forced_marriage_honor_violence_index: 8.67,
    },
    {
      id: "FMH-003",
      name: "Yémen/Conflit Mariage Précoce 66% — Filles Mariées Avant 18 Ans Pauvreté Déplacement Violence Domestique",
      composite_score: 79.3,
      risk_level: "critique",
      estimated_forced_marriage_honor_violence_index: 7.93,
    },
    {
      id: "FMH-004",
      name: "Irak/Kurdistan Crimes Honneur Légalisés — Article 409 Code Pénal Peine Réduite Brûlures Acide Mutilations",
      composite_score: 71.8,
      risk_level: "critique",
      estimated_forced_marriage_honor_violence_index: 7.18,
    },
    {
      id: "FMH-005",
      name: "Jordanie/Article 98 Défense Honneur — Réforme 2017 Partielle Persistance Impunité Familles Complices Justice",
      composite_score: 52.6,
      risk_level: "élevé",
      estimated_forced_marriage_honor_violence_index: 5.26,
    },
    {
      id: "FMH-006",
      name: "Maroc/Mariage Mineur Article 20 Réforme — Exceptions Judiciaires Persistantes 13% Mariages Précoces",
      composite_score: 47.3,
      risk_level: "élevé",
      estimated_forced_marriage_honor_violence_index: 4.73,
    },
    {
      id: "FMH-007",
      name: "Turquie/Mariage Enfants 15% Rural — Loi Interdiction 2021 Application Inégale Régions Conservatrices",
      composite_score: 28.4,
      risk_level: "modéré",
      estimated_forced_marriage_honor_violence_index: 2.84,
    },
    {
      id: "FMH-008",
      name: "Islande/Modèle Égalité Genre — Zéro Mariage Forcé Légal Plan Action National Violence Basée Genre Egalité",
      composite_score: 4.5,
      risk_level: "faible",
      estimated_forced_marriage_honor_violence_index: 0.45,
    },
  ],
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-marriage-honor-violence-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
