import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[access-water-sanitation-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "access-water-sanitation-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { entity_id: "WSR-001", name: "Somalie — <30% Accès Eau Potable, Sécheresse Chronique, Conflits Ressources & Déplacements Massifs Liés Eau", composite_score: 81.65, risk_level: "critique", estimated_water_rights_index: 8.16 },
    { entity_id: "WSR-002", name: "RDC — Choléra Endémique, Conflits Armés Contaminent Sources, 60% Pop Sans Eau Potable & Infrastructure Coloniale Délabrée", composite_score: 77.25, risk_level: "critique", estimated_water_rights_index: 7.72 },
    { entity_id: "WSR-003", name: "Yémen — Infrastructure Eau Détruite Coalition 2015-2024, Épidémie Choléra 2.5M Cas, Eau Arme Guerre & Humanitaire Bloqué", composite_score: 77.40, risk_level: "critique", estimated_water_rights_index: 7.74 },
    { entity_id: "WSR-004", name: "Niger — Zone Sahel Désertification, 45% Accès Eau, Changement Climatique Aggrave Pénurie & Conflits Pastoralisme", composite_score: 72.10, risk_level: "critique", estimated_water_rights_index: 7.21 },
    { entity_id: "WSR-005", name: "Pakistan — Inondations 2022 Contamination Arsenic, 21M Sans Eau Saine Post-Catastrophe, Privatisation Pénalisante & Corruption", composite_score: 49.60, risk_level: "élevé", estimated_water_rights_index: 4.96 },
    { entity_id: "WSR-006", name: "Inde rurale — Assainissement Défaillant Zones Tribales, Défécation Ouverte Persistante, Contamination Arsenic-Fluorure & ODD6 Retard", composite_score: 46.60, risk_level: "élevé", estimated_water_rights_index: 4.66 },
    { entity_id: "WSR-007", name: "Pérou — Zones Rurales Andines 25% Sans Eau, Mines Contaminent Sources, Progrès Urbains Mais Inégalités Rurales Persistantes", composite_score: 29.60, risk_level: "modéré", estimated_water_rights_index: 2.96 },
    { entity_id: "WSR-008", name: "Pays-Bas — Eau Publique Universelle, Tarif Social Garanti, Traités Internationaux Actifs & Modèle Coopération Eau Mondiale", composite_score: 2.60, risk_level: "faible", estimated_water_rights_index: 0.26 },
  ],
  avg_composite: 54.60,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/access-water-sanitation-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
