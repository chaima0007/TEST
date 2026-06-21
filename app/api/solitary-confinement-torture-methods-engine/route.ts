import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[solitary-confinement-torture-methods-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "solitary-confinement-torture-methods-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "SCT-001", name: "USA/ADX Florence — Supermax Isolement Total 23h/Jour 400+ Détenus Suicide Taux Élevé HRW Torture Psychologique", composite_score: 91.30, risk_level: "critique", estimated_torture_solitary_index: 9.13 },
    { id: "SCT-002", name: "Chine/Laojiao Réforme — Éducation Forcée Ouïghours Falun Gong Privation Sommeil Torture Mentale Aveux Contraints", composite_score: 89.30, risk_level: "critique", estimated_torture_solitary_index: 8.93 },
    { id: "SCT-003", name: "Russie/SHIZO Punition — Cellules Punitives Isolement Absolu Navalny Décès Conditions Inhumaines CPT Rapport", composite_score: 84.30, risk_level: "critique", estimated_torture_solitary_index: 8.43 },
    { id: "SCT-004", name: "Turquie/Type F Prison — Isolement Cellulaire Individuel Réservé Politiques Kurdes Longue Durée CPT Critique", composite_score: 77.30, risk_level: "critique", estimated_torture_solitary_index: 7.73 },
    { id: "SCT-005", name: "Israël/Incommunicado — Détention Prolongée Sans Contact Gazaouis 2023 Installations Sde Teiman Témoignages Abus", composite_score: 58.90, risk_level: "élevé", estimated_torture_solitary_index: 5.89 },
    { id: "SCT-006", name: "Égypte/Disparitions Forcées — Détention Incommunicado Opposants Politique 60 000+ Prisonniers Politiques Estimés AI", composite_score: 52.90, risk_level: "élevé", estimated_torture_solitary_index: 5.29 },
    { id: "SCT-007", name: "Danemark/Réforme Isolement — Interdiction Isolement Préventif -18 Ans Limite 4 Semaines Adultes Modèle Nordic", composite_score: 25.50, risk_level: "modéré", estimated_torture_solitary_index: 2.55 },
    { id: "SCT-008", name: "Règles Nelson Mandela ONU — Standard Minimum Traitement Détenus 2015 Révisées Isolement Max 15 Jours Consécutifs", composite_score: 9.90, risk_level: "faible", estimated_torture_solitary_index: 0.99 },
  ],
  avg_composite: 61.17,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/solitary-confinement-torture-methods-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
