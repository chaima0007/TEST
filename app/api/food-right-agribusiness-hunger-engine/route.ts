import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[food-right-agribusiness-hunger-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "food-right-agribusiness-hunger-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "FRA-001", name: "Yemen/Famine Guerre — 21M Insécurité Alimentaire Blocus Ports Hodeida ONU Dénonce Armes Saoudiennes", composite_score: 94.20, risk_level: "critique", estimated_food_rights_index: 9.42 },
    { id: "FRA-002", name: "RD Congo/Faim Chroni — 27M Famine Acute Phase 3+ Conflit Est Déplacement MSF Accès Impossible", composite_score: 87.30, risk_level: "critique", estimated_food_rights_index: 8.73 },
    { id: "FRA-003", name: "Éthiopie/Tigré Famine Arme — ONU 900 000 Famine 2021 Aide Bloquée Gouvernement Violation Droit International", composite_score: 79.90, risk_level: "critique", estimated_food_rights_index: 7.99 },
    { id: "FRA-004", name: "Inde/Green Revolution Paradoxe — 189M Sous-Alimentés 3e Rang Mondial GM Corps Brevets Monopoles Semences", composite_score: 72.40, risk_level: "critique", estimated_food_rights_index: 7.24 },
    { id: "FRA-005", name: "Brésil/Deforestation Soja — 69% Soja Export UE Déforestation Amazonie Peuples Autochtones Déplacés", composite_score: 55.90, risk_level: "élevé", estimated_food_rights_index: 5.59 },
    { id: "FRA-006", name: "USA/Farm Subsidies Big Ag — $20Mds/An Subventions Grandes Firmes Petits Agriculteurs Faillites Semences OGM", composite_score: 47.90, risk_level: "élevé", estimated_food_rights_index: 4.79 },
    { id: "FRA-007", name: "Kenya/Agroécologie — Transition Semences Locales Kounkuey Design Initiative Petits Paysans Résilience", composite_score: 29.50, risk_level: "modéré", estimated_food_rights_index: 2.95 },
    { id: "FRA-008", name: "Via Campesina/Droits Paysans — ONU Déclaration 2018 Semences Autonomie Alimentaire 200M Membres Mondial", composite_score: 13.90, risk_level: "faible", estimated_food_rights_index: 1.39 },
  ],
  avg_composite: 60.12,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-right-agribusiness-hunger-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
