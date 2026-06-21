import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-defenders-killings-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "environmental-defenders-killings-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "EDK-001", name: "Honduras — Taux Meurtres Défenseurs Env. le Plus Élevé/Habitant, Berta Cáceres, Impunité ZEDE & Minières", composite_score: 84.55, risk_level: "critique", estimated_environmental_defenders_index: 8.45 },
    { id: "EDK-002", name: "Philippines — Global Witness Rank 1 Meurtres, EJK Anti-Drogue Touche Militants, Impunité Totale & Loi Contre-Terrorisme", composite_score: 81.10, risk_level: "critique", estimated_environmental_defenders_index: 8.11 },
    { id: "EDK-003", name: "Brésil — Amazonie Garimpo Armé, Yanomami Menacés, Défenseurs Ruraux Assassinés & Recul Législatif FUNAI", composite_score: 77.05, risk_level: "critique", estimated_environmental_defenders_index: 7.71 },
    { id: "EDK-004", name: "Colombie — FARC Dissidents vs Défenseurs Territoriaux, 200+ Meurtres/An, Accord Paix Non Appliqué & Protection État Absente", composite_score: 73.55, risk_level: "critique", estimated_environmental_defenders_index: 7.35 },
    { id: "EDK-005", name: "Mexique — Cartels vs Militants Eau-Forêt, 54 Meurtres 2023, Journalistes Environnement Ciblés & Impunité 98%", composite_score: 56.05, risk_level: "élevé", estimated_environmental_defenders_index: 5.61 },
    { id: "EDK-006", name: "Inde — Militants Anti-Mines Tribaux Criminalisés, Loi UAPA Misuse, Défenseurs Adivasi Détenus & ONG Étrangers Bloqués", composite_score: 50.85, risk_level: "élevé", estimated_environmental_defenders_index: 5.09 },
    { id: "EDK-007", name: "Kenya — Ogiek Droits Fonciers, Défenseurs Safari Menacés, Protection Partielle Tribunaux & Avancées Constitutionnelles", composite_score: 31.90, risk_level: "modéré", estimated_environmental_defenders_index: 3.19 },
    { id: "EDK-008", name: "Costa Rica — Protection Constitutionnelle Forte, Loi Défenseurs Droits Humains, Zéro Meurtre Militant Env. & Modèle PNUE", composite_score: 9.10, risk_level: "faible", estimated_environmental_defenders_index: 0.91 },
  ],
  avg_composite: 58.02,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-defenders-killings-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
