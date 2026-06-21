import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[whistleblower-protection-corporate-accountability-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "whistleblower-protection-corporate-accountability-engine",
  generated_at: new Date().toISOString(),
  entities: [
    {
      id: "WPC-001",
      name: "Edward Snowden/NSA — Exil Permanent Russie, Espionage Act 1917, Pardon Obama Refusé, Révélations PRISM-XKeyscore Mondiales",
      composite_score: 87.35,
      risk_level: "critique",
      estimated_whistleblower_protection_index: 8.74,
    },
    {
      id: "WPC-002",
      name: "Julian Assange/WikiLeaks — 14 Ans Détention Diplomatie/Prison, Accord Plaider Coupable 2024, Liberté Conditionnelle Australie",
      composite_score: 83.15,
      risk_level: "critique",
      estimated_whistleblower_protection_index: 8.32,
    },
    {
      id: "WPC-003",
      name: "Daniel Ellsberg/Pentagon Papers 1971 — Poursuites Abandonnées, Héros Civil, Espionage Act Menace Perpétuelle USA, Décédé 2023",
      composite_score: 77.25,
      risk_level: "critique",
      estimated_whistleblower_protection_index: 7.73,
    },
    {
      id: "WPC-004",
      name: "Frances Haugen/Facebook — Sénat USA 2021, Facebook Files WSJ, Protégée SEC Whistleblower Program, Modèle Corporate Disclosure",
      composite_score: 62.6,
      risk_level: "critique",
      estimated_whistleblower_protection_index: 6.26,
    },
    {
      id: "WPC-005",
      name: "Hervé Falciani/HSBC SwissLeaks — Condamné Suisse 5 Ans, Extradition Refusée Espagne, 130 000 Comptes Offshore Révélés",
      composite_score: 55.6,
      risk_level: "élevé",
      estimated_whistleblower_protection_index: 5.56,
    },
    {
      id: "WPC-006",
      name: "Sherron Watkins/Enron — Mémo Lay 2001, Protection Sarbanes-Oxley Section 806, Modèle Corporate Whistleblowing USA",
      composite_score: 43.95,
      risk_level: "élevé",
      estimated_whistleblower_protection_index: 4.40,
    },
    {
      id: "WPC-007",
      name: "Antoine Deltour/LuxLeaks — Condamné Luxembourg 2016, Amnistie Partielle, EU Directive 2019 Conséquence Directe de son Cas",
      composite_score: 36.85,
      risk_level: "modéré",
      estimated_whistleblower_protection_index: 3.69,
    },
    {
      id: "WPC-008",
      name: "EU Directive 2019/1937 Modèle — Protection Harmonisée 27 États, Canal Signalement Interne-Externe, Anti-Représailles, Référence",
      composite_score: 8.65,
      risk_level: "faible",
      estimated_whistleblower_protection_index: 0.87,
    },
  ],
  avg_composite: 56.93,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/whistleblower-protection-corporate-accountability-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
