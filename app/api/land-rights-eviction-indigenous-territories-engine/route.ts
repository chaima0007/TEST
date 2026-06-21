import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[land-rights-eviction-indigenous-territories-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "land_rights_eviction_indigenous_territories",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "LRE-001", name: "Brésil Amazonie — Déforestation + garimpo, territoires Yanomami envahis, Lula action tardive", composite_score: 88.20, risk_level: "critique", estimated_land_rights_index: 8.82 },
    { entity_id: "LRE-002", name: "RDC — Grandes plantations agro, déplacements communautés, impunité entreprises", composite_score: 82.40, risk_level: "critique", estimated_land_rights_index: 8.24 },
    { entity_id: "LRE-003", name: "Indonésie — Palmier huile Kalimantan/Sumatra, Dayak/Orang Rimba expulsés", composite_score: 80.70, risk_level: "critique", estimated_land_rights_index: 8.07 },
    { entity_id: "LRE-004", name: "Éthiopie — Villagisation Gambella, grandes fermes Dubai/Saoudiens, displacement", composite_score: 71.90, risk_level: "critique", estimated_land_rights_index: 7.19 },
    { entity_id: "LRE-005", name: "Cambodge — Concessionnaires sucre EBA, 400K déplacés, UE sanctions partielles", composite_score: 53.50, risk_level: "élevé", estimated_land_rights_index: 5.35 },
    { entity_id: "LRE-006", name: "Kenya Maasai — Expulsions safari/tourisme, Ngorongoro héritage", composite_score: 45.70, risk_level: "élevé", estimated_land_rights_index: 4.57 },
    { entity_id: "LRE-007", name: "Philippines — FPIC bafoué, mines Mindanao, Lumad expulsions", composite_score: 27.20, risk_level: "modéré", estimated_land_rights_index: 2.72 },
    { entity_id: "LRE-008", name: "Bolivie — Consultation préalable FPIC respectée, autonomie territoriale TIPNIS", composite_score: 7.65, risk_level: "faible", estimated_land_rights_index: 0.77 },
  ],
  avg_composite: 57.16,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-rights-eviction-indigenous-territories-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
